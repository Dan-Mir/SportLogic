from __future__ import annotations

from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from sportlogic.db import get_db
from sportlogic.modules.abbonamenti.models import (
    Installment,
    Payment,
    Receipt,
    Subscription,
    SubscriptionPlan,
)
from sportlogic.modules.abbonamenti.schemas import (
    InstallmentRead,
    PaymentCreate,
    PaymentRead,
    PlanCreate,
    PlanRead,
    PlanUpdate,
    ReceiptRead,
    RenewalCreate,
    SubscriptionCreate,
    SubscriptionRead,
)
from sportlogic.modules.anagrafica.models import Member
from sportlogic.modules.core.deps import get_client_ip, log_action, require_role
from sportlogic.modules.core.models import User

router = APIRouter(prefix="/api/abbonamenti", tags=["abbonamenti"])
DbSession = Annotated[Session, Depends(get_db)]
StaffUser = Annotated[User, Depends(require_role("admin", "gestore", "reception"))]


def _not_found(entity: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{entity} non trovato/a")


def _subscription_query():
    return select(Subscription).options(
        selectinload(Subscription.plan),
        selectinload(Subscription.payments).selectinload(Payment.receipt),
        selectinload(Subscription.installments),
    )


def _split_amount(total: Decimal, count: int) -> list[Decimal]:
    unit = (total / count).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    amounts = [unit] * count
    amounts[-1] = total - sum(amounts[:-1], Decimal("0.00"))
    return amounts


def _add_installments(
    subscription: Subscription, plan: SubscriptionPlan, count: int, db: Session
) -> None:
    for number, amount in enumerate(_split_amount(plan.price, count), start=1):
        due_on = subscription.starts_on + timedelta(
            days=((subscription.ends_on - subscription.starts_on).days * (number - 1)) // count
        )
        db.add(
            Installment(
                subscription=subscription,
                number=number,
                due_on=due_on,
                amount=amount,
            )
        )


@router.get("/plans", response_model=list[PlanRead])
def list_plans(db: DbSession, _: StaffUser) -> list[SubscriptionPlan]:
    return list(db.scalars(select(SubscriptionPlan).order_by(SubscriptionPlan.name)))


@router.post("/plans", response_model=PlanRead, status_code=status.HTTP_201_CREATED)
def create_plan(payload: PlanCreate, request: Request, db: DbSession, user: StaffUser) -> SubscriptionPlan:
    plan = SubscriptionPlan(**payload.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    log_action(db, user, "subscription_plan.create", "subscription_plan", str(plan.id),
               detail=plan.name, ip_address=get_client_ip(request))
    return plan


@router.put("/plans/{plan_id}", response_model=PlanRead)
def update_plan(
    plan_id: int, payload: PlanUpdate, request: Request, db: DbSession, user: StaffUser
) -> SubscriptionPlan:
    plan = db.get(SubscriptionPlan, plan_id)
    if plan is None:
        raise _not_found("Piano")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    log_action(db, user, "subscription_plan.update", "subscription_plan", str(plan_id),
               ip_address=get_client_ip(request))
    return plan


@router.get("/subscriptions", response_model=list[SubscriptionRead])
def list_subscriptions(
    db: DbSession,
    _: StaffUser,
    member_id: int | None = Query(default=None),
    subscription_status: str | None = Query(default=None, alias="status"),
) -> list[Subscription]:
    stmt = _subscription_query().order_by(Subscription.ends_on.desc())
    if member_id is not None:
        stmt = stmt.where(Subscription.member_id == member_id)
    if subscription_status:
        stmt = stmt.where(Subscription.status == subscription_status)
    return list(db.scalars(stmt))


@router.post("/subscriptions", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
def create_subscription(
    payload: SubscriptionCreate, request: Request, db: DbSession, user: StaffUser
) -> Subscription:
    if payload.ends_on < payload.starts_on:
        raise HTTPException(status_code=422, detail="La fine deve seguire l'inizio")
    if db.get(Member, payload.member_id) is None:
        raise _not_found("Socio")
    plan = db.get(SubscriptionPlan, payload.plan_id)
    if plan is None:
        raise _not_found("Piano")
    values = payload.model_dump(exclude={"installments_count"})
    subscription = Subscription(**values)
    db.add(subscription)
    db.flush()
    _add_installments(subscription, plan, payload.installments_count, db)
    db.commit()
    db.refresh(subscription)
    log_action(db, user, "subscription.create", "subscription", str(subscription.id),
               detail=f"member_id={subscription.member_id}", ip_address=get_client_ip(request))
    return db.scalar(_subscription_query().where(Subscription.id == subscription.id))


@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionRead)
def get_subscription(subscription_id: int, db: DbSession, _: StaffUser) -> Subscription:
    subscription = db.scalar(_subscription_query().where(Subscription.id == subscription_id))
    if subscription is None:
        raise _not_found("Abbonamento")
    return subscription


@router.get("/installments", response_model=list[InstallmentRead])
def list_installments(
    db: DbSession,
    _: StaffUser,
    subscription_id: int | None = Query(default=None),
) -> list[Installment]:
    stmt = select(Installment).order_by(Installment.due_on, Installment.number)
    if subscription_id is not None:
        stmt = stmt.where(Installment.subscription_id == subscription_id)
    return list(db.scalars(stmt))


@router.post(
    "/subscriptions/{subscription_id}/renew",
    response_model=SubscriptionRead,
    status_code=status.HTTP_201_CREATED,
)
def renew_subscription(
    subscription_id: int,
    payload: RenewalCreate,
    request: Request,
    db: DbSession,
    user: StaffUser,
) -> Subscription:
    current = db.scalar(_subscription_query().where(Subscription.id == subscription_id))
    if current is None:
        raise _not_found("Abbonamento")
    plan = db.get(SubscriptionPlan, payload.plan_id or current.plan_id)
    if plan is None:
        raise _not_found("Piano")
    starts_on = payload.starts_on or (current.ends_on + timedelta(days=1))
    ends_on = starts_on + timedelta(days=plan.duration_days - 1)
    renewed = Subscription(
        member_id=current.member_id,
        plan_id=plan.id,
        starts_on=starts_on,
        ends_on=ends_on,
        status="active",
        auto_renew=plan.auto_renew,
        notes=payload.notes,
    )
    db.add(renewed)
    db.flush()
    _add_installments(renewed, plan, 1, db)
    db.commit()
    db.refresh(renewed)
    log_action(
        db,
        user,
        "subscription.renew",
        "subscription",
        str(renewed.id),
        detail=f"previous_subscription_id={subscription_id}",
        ip_address=get_client_ip(request),
    )
    return db.scalar(_subscription_query().where(Subscription.id == renewed.id))


@router.post("/subscriptions/{subscription_id}/payments", response_model=PaymentRead,
             status_code=status.HTTP_201_CREATED)
def create_payment(
    subscription_id: int, payload: PaymentCreate, request: Request, db: DbSession, user: StaffUser
) -> Payment:
    subscription = db.get(Subscription, subscription_id)
    if subscription is None:
        raise _not_found("Abbonamento")
    values = payload.model_dump(exclude_none=True)
    installment_id = values.pop("installment_id", None)
    installment = None
    if installment_id is not None:
        installment = db.get(Installment, installment_id)
        if installment is None or installment.subscription_id != subscription_id:
            raise HTTPException(status_code=422, detail="La rata non appartiene all'abbonamento")
    else:
        installment = db.scalar(
            select(Installment)
            .where(
                Installment.subscription_id == subscription_id,
                Installment.status.in_(["pending", "partial", "overdue"]),
            )
            .order_by(Installment.number)
        )
    if installment is not None:
        remaining = installment.amount - installment.paid_amount
        if values["amount"] > remaining:
            raise HTTPException(status_code=422, detail="Il pagamento supera il residuo della rata")
        installment.paid_amount += values["amount"]
        installment.status = "paid" if installment.paid_amount == installment.amount else "partial"
    payment = Payment(subscription_id=subscription_id, installment_id=installment.id if installment else None, **values)
    db.add(payment)
    db.flush()
    db.add(
        Receipt(
            payment_id=payment.id,
            receipt_number=f"R-{date.today().year}-{payment.id:06d}",
            amount=payment.amount,
        )
    )
    db.commit()
    payment = db.scalar(
        select(Payment).options(selectinload(Payment.receipt)).where(Payment.id == payment.id)
    )
    log_action(db, user, "payment.create", "payment", str(payment.id),
               detail=f"subscription_id={subscription_id}; amount={payment.amount}",
               ip_address=get_client_ip(request))
    return payment


@router.get("/payments", response_model=list[PaymentRead])
def list_payments(db: DbSession, _: StaffUser) -> list[Payment]:
    stmt = select(Payment).options(selectinload(Payment.receipt)).order_by(Payment.paid_at.desc())
    return list(db.scalars(stmt))


@router.get("/receipts", response_model=list[ReceiptRead])
def list_receipts(db: DbSession, _: StaffUser) -> list[Receipt]:
    return list(db.scalars(select(Receipt).order_by(Receipt.issued_at.desc())))

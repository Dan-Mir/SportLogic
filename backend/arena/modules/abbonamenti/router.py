from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from arena.db import get_db
from arena.modules.abbonamenti.models import Payment, Subscription, SubscriptionPlan
from arena.modules.abbonamenti.schemas import (
    PaymentCreate,
    PaymentRead,
    PlanCreate,
    PlanRead,
    PlanUpdate,
    SubscriptionCreate,
    SubscriptionRead,
)
from arena.modules.anagrafica.models import Member
from arena.modules.core.deps import get_client_ip, log_action, require_role
from arena.modules.core.models import User

router = APIRouter(prefix="/api/abbonamenti", tags=["abbonamenti"])
DbSession = Annotated[Session, Depends(get_db)]
StaffUser = Annotated[User, Depends(require_role("admin", "gestore", "reception"))]


def _not_found(entity: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{entity} non trovato/a")


def _subscription_query():
    return select(Subscription).options(
        selectinload(Subscription.plan), selectinload(Subscription.payments)
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
    if db.get(SubscriptionPlan, payload.plan_id) is None:
        raise _not_found("Piano")
    subscription = Subscription(**payload.model_dump())
    db.add(subscription)
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


@router.post("/subscriptions/{subscription_id}/payments", response_model=PaymentRead,
             status_code=status.HTTP_201_CREATED)
def create_payment(
    subscription_id: int, payload: PaymentCreate, request: Request, db: DbSession, user: StaffUser
) -> Payment:
    subscription = db.get(Subscription, subscription_id)
    if subscription is None:
        raise _not_found("Abbonamento")
    payment = Payment(subscription_id=subscription_id, **payload.model_dump(exclude_none=True))
    db.add(payment)
    db.commit()
    db.refresh(payment)
    log_action(db, user, "payment.create", "payment", str(payment.id),
               detail=f"subscription_id={subscription_id}; amount={payment.amount}",
               ip_address=get_client_ip(request))
    return payment


@router.get("/payments", response_model=list[PaymentRead])
def list_payments(db: DbSession, _: StaffUser) -> list[Payment]:
    return list(db.scalars(select(Payment).order_by(Payment.paid_at.desc())))

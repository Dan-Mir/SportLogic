from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from arena.db import Base, TimestampMixin
from arena.modules.anagrafica.models import Member


class SubscriptionPlan(Base, TimestampMixin):
    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    billing_type: Mapped[str] = mapped_column(String(32), default="monthly")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    duration_days: Mapped[int] = mapped_column(default=30)
    included_entries: Mapped[int | None] = mapped_column(nullable=True)
    auto_renew: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    notes: Mapped[str | None] = mapped_column(Text)

    subscriptions: Mapped[list[Subscription]] = relationship(back_populates="plan")


class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("subscription_plans.id"), index=True)
    starts_on: Mapped[date] = mapped_column(Date)
    ends_on: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(24), default="active", index=True)
    auto_renew: Mapped[bool] = mapped_column(default=False)
    notes: Mapped[str | None] = mapped_column(Text)

    member: Mapped[Member] = relationship()
    plan: Mapped[SubscriptionPlan] = relationship(back_populates="subscriptions")
    payments: Mapped[list[Payment]] = relationship(
        back_populates="subscription", cascade="all, delete-orphan"
    )


class Payment(Base):
    __tablename__ = "subscription_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id", ondelete="CASCADE"), index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    method: Mapped[str] = mapped_column(String(32), default="cash")
    reference: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(24), default="completed")
    notes: Mapped[str | None] = mapped_column(Text)

    subscription: Mapped[Subscription] = relationship(back_populates="payments")

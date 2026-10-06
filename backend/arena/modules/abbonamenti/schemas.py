from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

BillingType = Literal["monthly", "seasonal", "entries", "custom"]
PaymentMethod = Literal["cash", "pos", "bank_transfer", "check", "other"]


class PlanBase(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    billing_type: BillingType = "monthly"
    price: Decimal = Field(ge=0, decimal_places=2)
    duration_days: int = Field(default=30, ge=1, le=3660)
    included_entries: int | None = Field(default=None, ge=1)
    auto_renew: bool = False
    is_active: bool = True
    notes: str | None = None


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    billing_type: BillingType | None = None
    price: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    duration_days: int | None = Field(default=None, ge=1, le=3660)
    included_entries: int | None = Field(default=None, ge=1)
    auto_renew: bool | None = None
    is_active: bool | None = None
    notes: str | None = None


class PlanRead(PlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class SubscriptionCreate(BaseModel):
    member_id: int
    plan_id: int
    starts_on: date
    ends_on: date
    status: Literal["active", "paused", "expired", "cancelled"] = "active"
    auto_renew: bool = False
    notes: str | None = None


class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2)
    paid_at: datetime | None = None
    method: PaymentMethod = "cash"
    reference: str | None = Field(default=None, max_length=120)
    notes: str | None = None


class PaymentRead(PaymentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subscription_id: int
    status: str


class SubscriptionRead(SubscriptionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plan: PlanRead
    payments: list[PaymentRead] = []

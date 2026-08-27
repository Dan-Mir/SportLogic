from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    fiscal_code: str | None = None
    birth_date: date | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    province: str | None = None
    postal_code: str | None = None
    gdpr_consent: bool = False
    notes: str | None = None
    is_active: bool = True


class MemberCreate(MemberBase):
    pass


class MemberRead(MemberBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class StaffBase(BaseModel):
    first_name: str
    last_name: str
    role: str = "istruttore"
    qualifications: str | None = None
    certifications: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    is_active: bool = True


class StaffCreate(StaffBase):
    pass


class StaffRead(StaffBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class FamilyBase(BaseModel):
    name: str
    notes: str | None = None


class FamilyCreate(FamilyBase):
    pass


class FamilyRead(FamilyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

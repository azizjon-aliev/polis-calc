from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, EmailStr, constr

from app.schemas.auth_schema import UserResponseSchema


class TariffEnum(StrEnum):
    standard = "standard"
    premium = "premium"


class CarTypeEnum(StrEnum):
    sedan = "sedan"
    suv = "suv"
    truck = "truck"


class ApplicationStatusEnum(StrEnum):
    new = "new"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class BaseQuoteSchema(BaseModel):
    tariff: TariffEnum
    age: int
    experience: int
    car_type: CarTypeEnum


class BaseApplicationSchema(BaseModel):
    full_name: constr(
        min_length=3,
        max_length=200,
    )
    phone: constr(
        min_length=9,
        max_length=15,
        pattern="^\+?1?\d{9,15}$",
    )
    email: EmailStr
    tariff: TariffEnum


class QuoteCreateRequestSchema(BaseQuoteSchema): ...


class QuoteCreateResponseSchema(BaseQuoteSchema):
    id: UUID
    price: Decimal
    created_at: datetime
    updated_at: datetime | None


class ApplicationCreateRequestSchema(BaseApplicationSchema):
    quote_id: UUID


class ApplicationCreateResponseSchema(BaseApplicationSchema):
    id: UUID
    quote: QuoteCreateResponseSchema
    owner: UserResponseSchema
    status: ApplicationStatusEnum
    created_at: datetime
    updated_at: datetime | None

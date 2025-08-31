import uuid
from sqlalchemy.types import UUID
from sqlalchemy import Column, Integer, Numeric, Enum as PgEnum, DateTime, func
from app.db.session import Base
from app.schemas.polis_schema import CarTypeEnum, TariffEnum


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    tariff = Column(PgEnum(TariffEnum, name="tariff_enum"), nullable=False)
    age = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    car_type = Column(PgEnum(CarTypeEnum, name="car_type_enum"), nullable=False)
    price = Column(Numeric(precision=12, scale=2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

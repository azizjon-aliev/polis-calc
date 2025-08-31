from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import uuid

from app.db.session import Base
from app.schemas.polis_schema import ApplicationStatusEnum, TariffEnum


class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tariff = Column(
        Enum(TariffEnum, name="application_tariff_enum"),
        nullable=False,
        default=TariffEnum.standard,
    )

    quote_id = Column(UUID(as_uuid=True), ForeignKey("quotes.id"), nullable=False)
    quote = relationship("Quote")

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User")

    status = Column(
        Enum(ApplicationStatusEnum, name="application_status_enum"),
        nullable=False,
        default=ApplicationStatusEnum.new,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

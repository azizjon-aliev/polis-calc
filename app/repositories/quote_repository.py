from decimal import Decimal
from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.quote_model import Quote
from app.schemas.polis_schema import TariffEnum, CarTypeEnum


class QuoteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_quote(
        self, tariff: TariffEnum, age: int, experience: int, car_type: CarTypeEnum, price: Decimal
    ) -> Quote:
        """Create a new quote in the database."""
        logger.debug(f"Creating new quote: {tariff}, {age}, {experience}, {car_type}")
        quote = Quote(
            tariff=tariff,
            age=age,
            experience=experience,
            car_type=car_type,
            price=price,
        )
        self.session.add(quote)
        await self.session.commit()
        await self.session.refresh(quote)
        return quote

    async def get_quote_by_id(self, quote_id: UUID) -> Quote | None:
        """Retrieve a quote by its ID."""
        logger.debug(f"Fetching quote by ID: {quote_id}")
        result = await self.session.execute(select(Quote).where(Quote.id == quote_id))
        return result.scalars().first()

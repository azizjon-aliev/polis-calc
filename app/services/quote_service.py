from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from loguru import logger

from app.core.config import settings
from app.repositories.quote_repository import QuoteRepository
from app.schemas.polis_schema import QuoteCreateRequestSchema, QuoteCreateResponseSchema
from app.schemas.polis_schema import TariffEnum, CarTypeEnum


class QuoteService:
    """Service for managing quotes."""

    def __init__(self, quote_repository: QuoteRepository):
        self._repository = quote_repository

    @staticmethod
    async def calculate_quote_price(data: QuoteCreateRequestSchema) -> Decimal:
        """Calculate the price of a quote based on the provided data."""
        price = settings.quote_base_price

        # Coefficients
        TARIFF_COEFF = {
            TariffEnum.standard: Decimal("1.0"),
            TariffEnum.premium: Decimal("1.5"),
        }

        def age_coeff(age: int) -> Decimal:
            if age < 25:
                return Decimal("1.2")

            elif age > 60:
                return Decimal("1.1")

            return Decimal("1.0")

        def experience_coeff(exp: int) -> Decimal:
            if exp < 2:
                return Decimal("1.3")

            elif exp < 5:
                return Decimal("1.1")

            return Decimal("1.0")

        CAR_COEFF = {
            CarTypeEnum.sedan: Decimal("1.0"),
            CarTypeEnum.suv: Decimal("1.2"),
            CarTypeEnum.truck: Decimal("1.3"),
        }

        logger.info(f"Calculating quote price for: {data.dict()}")

        # Calculation
        price *= TARIFF_COEFF[data.tariff]
        price *= age_coeff(data.age)
        price *= experience_coeff(data.experience)
        price *= CAR_COEFF[data.car_type]

        # Rounding to 2 decimal places
        final_price = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        logger.info(f"Calculated price: {final_price}")

        return final_price

    async def create_quote(self, data: QuoteCreateRequestSchema) -> QuoteCreateResponseSchema:
        """Create a new quote."""
        logger.info(f"Creating quote for: {data.dict()}")
        quote_price = await self.calculate_quote_price(data)

        quote = await self._repository.create_quote(
            tariff=data.tariff,
            age=data.age,
            experience=data.experience,
            car_type=data.car_type,
            price=quote_price,
        )

        logger.success(f"Quote created with ID: {quote.id} and price: {quote_price}")

        return QuoteCreateResponseSchema(
            id=quote.id,
            tariff=quote.tariff,
            age=quote.age,
            experience=quote.experience,
            car_type=quote.car_type,
            price=quote.price,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
        )

    async def get_quote_by_id(self, quote_id: UUID) -> QuoteCreateResponseSchema | None:
        """Retrieve a quote by ID. Returns None if not found."""
        logger.info(f"Fetching quote with ID: {quote_id}")
        quote = await self._repository.get_quote_by_id(quote_id)

        if not quote:
            logger.warning(f"Quote with ID {quote_id} not found")
            return None

        logger.success(f"Quote fetched with ID: {quote.id}")
        return QuoteCreateResponseSchema(
            id=quote.id,
            tariff=quote.tariff,
            age=quote.age,
            experience=quote.experience,
            car_type=quote.car_type,
            price=quote.price,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
        )

from uuid import UUID
from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.application_model import Application
from app.db.models.quote_model import Quote
from app.db.models.user_model import User
from app.schemas.polis_schema import ApplicationStatusEnum


class ApplicationRepository:
    """Repository for managing Application DB operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_application(
        self,
        full_name: str,
        phone: str,
        email: str,
        tariff: str,
        quote_id: UUID,
        owner: User,
    ) -> Application:
        """
        Create a new application in the database.

        Raises:
            ValueError: If user or quote not found.
        """
        logger.debug(f"Creating application for user {owner} with quote {quote_id}")

        await self._get_entity(Quote, quote_id, "Quote")

        application = Application(
            full_name=full_name,
            phone=phone,
            email=email,
            tariff=tariff,
            quote_id=quote_id,
            status=ApplicationStatusEnum.new,
            owner_id=owner.id,
        )
        self.session.add(application)
        await self.session.commit()
        await self.session.refresh(application)

        logger.info(f"Application {application.id} created for user {owner.id}")
        return application

    async def get_application(self, application_id: UUID, owner: User) -> Optional[Application]:
        """Retrieve an application by its ID."""
        logger.debug(f"Fetching application by ID: {application_id}")
        result = await self.session.execute(
            select(Application).where(
                Application.id == application_id, Application.owner_id == owner.id
            )
        )
        app = result.scalars().first()
        if app:
            logger.debug(f"Found application {app.id}")
        else:
            logger.warning(f"Application {application_id} not found")
        return app

    # --- helper method ---
    async def _get_entity(self, model, entity_id: UUID, name: str):
        entity = await self.session.get(model, entity_id)
        if not entity:
            logger.error(f"{name} with ID {entity_id} not found.")
            raise ValueError(f"{name} not found")
        return entity

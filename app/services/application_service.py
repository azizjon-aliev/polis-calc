from uuid import UUID

from loguru import logger

from app.db.models.application_model import Application
from app.db.models.user_model import User
from app.repositories.application_repository import ApplicationRepository
from app.schemas.polis_schema import (
    ApplicationCreateRequestSchema,
    ApplicationCreateResponseSchema,
)


class ApplicationService:
    def __init__(self, application_repository: ApplicationRepository):
        self._repository = application_repository

    async def create_application(
        self,
        data: ApplicationCreateRequestSchema,
        owner: User,
    ) -> ApplicationCreateResponseSchema:
        """Create a new application."""
        logger.info(f"Creating application: {data}")

        application = await self._repository.create_application(*data, owner=owner)

        logger.success(f"Application created with ID: {application.id}")
        return ApplicationCreateResponseSchema(
            id=application.id,
            full_name=application.full_name,
            phone=application.phone,
            email=application.email,
            tariff=application.tariff,
            quote=application.quote,
            owner=application.owner,
            status=application.status,
            created_at=application.created_at,
            updated_at=application.updated_at,
        )

    async def get_application(self, application_id: UUID, owner: User) -> Application | None:
        """Retrieve an application by quote ID."""
        logger.info(f"Retrieving application: {application_id}, owner ID: {owner.id}")

        application = await self._repository.get_application(
            application_id=application_id, owner=owner
        )

        if application:
            logger.success(f"Application found with ID: {application.id}")
        else:
            logger.warning(f"No application found: {application_id}")

        return application

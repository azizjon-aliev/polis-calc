from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.models.user_model import User
from app.db.session import get_session
from app.repositories.application_repository import ApplicationRepository
from app.repositories.quote_repository import QuoteRepository
from app.repositories.user_repository import UserRepository
from app.services.application_service import ApplicationService
from app.services.auth_service import AuthService
from app.services.quote_service import QuoteService
from app.services.security_service import SecurityService

bearer_scheme = HTTPBearer()


# Repositories
async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    """Factory function to get UserRepository with a database session."""
    logger.debug("Getting user repository")
    return UserRepository(session=session)


async def get_quote_repository(
    session: AsyncSession = Depends(get_session),
) -> QuoteRepository:
    """Factory function to get QuoteRepository with a database session."""
    logger.debug("Getting quote repository")
    return QuoteRepository(session=session)


async def get_application_repository(
    session: AsyncSession = Depends(get_session),
) -> ApplicationRepository:
    """Factory function to get ApplicationRepository with a database session."""
    logger.debug("Getting application repository")
    return ApplicationRepository(session=session)


# Services
async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Factory function to get AuthService with UserRepository."""
    logger.debug("Getting auth service")
    return AuthService(user_repository=user_repository)


async def get_security_service() -> SecurityService:
    """Factory function to get SecurityService."""
    logger.debug("Getting security service")
    return SecurityService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    security_service: SecurityService = Depends(get_security_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    """Dependency to get the current authenticated user."""
    logger.debug("Getting current user")
    username = security_service.verify_token(token=credentials.credentials)

    if username is None:
        logger.info("Refreshing tokens failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = await user_repo.get_user_by_username(username=username)

    if user is None:
        logger.info("User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def get_quote_service(
    quote_repository: QuoteRepository = Depends(get_quote_repository),
) -> QuoteService:
    """Factory function to get QuoteService with QuoteRepository."""
    logger.debug("Getting quote service")
    return QuoteService(quote_repository=quote_repository)


async def get_application_service(
    application_repository: ApplicationRepository = Depends(get_application_repository),
) -> ApplicationService:
    """Factory function to get ApplicationService with ApplicationRepository."""
    logger.debug("Getting application service")

    return ApplicationService(application_repository=application_repository)

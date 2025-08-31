from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db.models.user_model import User
from app.endpoints.dependencies import get_quote_service, get_application_service, get_current_user
from app.schemas.polis_schema import (
    QuoteCreateRequestSchema,
    QuoteCreateResponseSchema,
    ApplicationCreateRequestSchema,
    ApplicationCreateResponseSchema,
)
from app.services.application_service import ApplicationService
from app.services.quote_service import QuoteService
from app.utils import rate_limit

router = APIRouter(tags=["Polis"])


@router.post("/quotes")
@rate_limit(max_requests=5, time_window=60)
async def create_quote(
    request: Request,
    data: QuoteCreateRequestSchema,
    quote_service: Annotated[QuoteService, Depends(get_quote_service)],
) -> QuoteCreateResponseSchema:
    """Create a new quote with the provided data."""
    logger.info(f"Creating new quote with data: {data.model_dump()}")

    response = await quote_service.create_quote(data)

    logger.info(f"Created quote with ID: {response.id}")

    return response


@router.get("/quotes/{quote_id}")
@rate_limit(max_requests=5, time_window=60)
async def get_quote(
    request: Request,
    quote_id: UUID,
    quote_service: Annotated[QuoteService, Depends(get_quote_service)],
) -> QuoteCreateResponseSchema:
    """Retrieve a quote by its ID."""
    logger.info(f"Getting quote with ID: {quote_id}")

    response = await quote_service.get_quote_by_id(quote_id)

    if response is None:
        logger.info(f"No quote with ID: {quote_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Quote not found"}
        )

    logger.info("Successfully retrieved quote")
    return response


@router.post("/applications")
async def create_application(
    data: ApplicationCreateRequestSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    application_service: Annotated[ApplicationService, Depends(get_application_service)],
) -> ApplicationCreateResponseSchema:
    """Create a new application with the provided data."""
    logger.info(f"Creating new application with data: {data.model_dump()}")

    try:
        response = await application_service.create_application(data, owner=current_user)
        logger.info(f"Created application with ID: {response.id}")
        return response
    except ValueError as e:
        logger.error(f"Error creating application: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)})


@router.get("/applications/{application_id}")
async def get_application(
    application_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    application_service: Annotated[ApplicationService, Depends(get_application_service)],
) -> ApplicationCreateResponseSchema:
    """Retrieve an application by its ID."""
    logger.info(f"Getting application with ID: {application_id}")

    response = await application_service.get_application(
        application_id=application_id, owner=current_user
    )

    if response is None:
        logger.info(f"No application with ID: {application_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Application not found"}
        )

    logger.info("Successfully retrieved application")
    return response

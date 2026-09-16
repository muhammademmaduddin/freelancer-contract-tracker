from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import DomainError


async def domain_error_handler(
    request: Request,
    exc: DomainError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc),
        },
    )
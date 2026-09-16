from fastapi import FastAPI

from app.api.contracts import router as contracts_router
from app.api.disputes import router as disputes_router
from app.api.exception_handlers import domain_error_handler
from app.api.milestones import router as milestones_router
from app.api.payments import router as payments_router
from app.core.exceptions import DomainError
from app.db import create_db_and_tables


app = FastAPI(
    title="Freelancer Contract & Milestone Payment Tracker",
    version="1.0.0",
    description=(
        "Backend API for freelance contracts, milestone lifecycle "
        "management, partial payments, deadlines, and disputes."
    ),
)


@app.on_event("startup")
def startup() -> None:
    create_db_and_tables()


app.add_exception_handler(
    DomainError,
    domain_error_handler,
)

app.include_router(contracts_router)
app.include_router(milestones_router)
app.include_router(payments_router)
app.include_router(disputes_router)


@app.get(
    "/health",
    tags=["health"],
)
def health_check():
    return {
        "status": "ok",
    }
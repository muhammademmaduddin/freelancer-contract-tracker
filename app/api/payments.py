from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentSummaryResponse,
)
from app.services.milestone_service import get_milestone_by_id
from app.services.payment_service import (
    get_amount_paid,
    get_outstanding_amount,
    record_payment,
)

router = APIRouter(
    prefix="/milestones",
    tags=["payments"],
)


@router.post(
    "/{milestone_id}/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def record_payment_endpoint(
    milestone_id: int,
    payload: PaymentCreate,
    db: Session = Depends(get_db),
):
    milestone = get_milestone_by_id(
        db,
        milestone_id,
    )

    if milestone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milestone not found.",
        )

    return record_payment(
        db,
        milestone,
        payload,
    )


@router.get(
    "/{milestone_id}/payments/summary",
    response_model=PaymentSummaryResponse,
)
def get_payment_summary_endpoint(
    milestone_id: int,
    db: Session = Depends(get_db),
):
    milestone = get_milestone_by_id(
        db,
        milestone_id,
    )

    if milestone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milestone not found.",
        )

    amount_paid = get_amount_paid(
        db,
        milestone.id,
    )

    outstanding_amount = get_outstanding_amount(
        db,
        milestone,
    )

    return PaymentSummaryResponse(
        milestone_id=milestone.id,
        milestone_amount=milestone.amount,
        amount_paid=amount_paid,
        outstanding_amount=outstanding_amount,
    )
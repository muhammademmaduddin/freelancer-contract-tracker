from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.dispute import (
    DisputeCreate,
    DisputeResponse,
)
from app.services.dispute_service import create_dispute
from app.services.milestone_service import get_milestone_by_id

router = APIRouter(
    prefix="/milestones",
    tags=["disputes"],
)


@router.post(
    "/{milestone_id}/disputes",
    response_model=DisputeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_dispute_endpoint(
    milestone_id: int,
    payload: DisputeCreate,
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

    return create_dispute(
        db,
        milestone,
        payload,
    )
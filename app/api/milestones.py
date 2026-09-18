from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.milestone import (
    MilestoneResponse,
    MilestoneStatusUpdate,
    OverdueMilestoneResponse,
)
from app.services.milestone_service import (
    get_milestone_by_id,
    get_overdue_milestones,
    update_milestone_status,
)

router = APIRouter(
    prefix="/milestones",
    tags=["milestones"],
)


@router.patch(
    "/{milestone_id}/status",
    response_model=MilestoneResponse,
)
def update_milestone_status_endpoint(
    milestone_id: int,
    payload: MilestoneStatusUpdate,
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

    return update_milestone_status(
        db,
        milestone,
        payload.status,
    )


@router.get(
    "/overdue",
    response_model=list[OverdueMilestoneResponse],
)
def get_overdue_milestones_endpoint(
    db: Session = Depends(get_db),
):
    milestones = get_overdue_milestones(db)

    return [
        OverdueMilestoneResponse(
            id=milestone.id,
            title=milestone.title,
            amount=milestone.amount,
            deadline=milestone.deadline,
            status=milestone.status,
            contract_id=milestone.contract_id,
            days_overdue=(
                date.today() - milestone.deadline
            ).days,
        )
        for milestone in milestones
    ]


@router.get(
    "/{milestone_id}",
    response_model=MilestoneResponse,
)
def get_milestone_endpoint(
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

    return milestone

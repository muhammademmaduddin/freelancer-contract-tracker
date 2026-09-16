from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.contract import (
    ContractCreate,
    ContractResponse,
    ContractSummaryResponse,
)
from app.schemas.milestone import (
    MilestoneCreate,
    MilestoneResponse,
)
from app.services.contract_service import (
    add_milestone,
    create_contract,
    get_contract_by_id,
    get_contract_summary,
)

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
)


@router.post(
    "",
    response_model=ContractResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contract_endpoint(
    payload: ContractCreate,
    db: Session = Depends(get_db),
):
    return create_contract(
        db,
        payload,
    )


@router.post(
    "/{contract_id}/milestones",
    response_model=MilestoneResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_milestone_endpoint(
    contract_id: int,
    payload: MilestoneCreate,
    db: Session = Depends(get_db),
):
    contract = get_contract_by_id(
        db,
        contract_id,
    )

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found.",
        )

    return add_milestone(
        db,
        contract,
        payload,
    )


@router.get(
    "/{contract_id}/summary",
    response_model=ContractSummaryResponse,
)
def get_contract_summary_endpoint(
    contract_id: int,
    db: Session = Depends(get_db),
):
    contract = get_contract_by_id(
        db,
        contract_id,
    )

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found.",
        )

    return get_contract_summary(
        db,
        contract,
    )
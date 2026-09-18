from datetime import date, timedelta
from decimal import Decimal

import pytest
from fastapi import HTTPException

from app.api.milestones import get_milestone_endpoint
from app.core.enums import MilestoneStatus
from app.schemas.contract import ContractCreate
from app.schemas.milestone import MilestoneCreate, MilestoneResponse
from app.services.contract_service import add_milestone, create_contract


def create_test_milestone(db_session):
    contract = create_contract(
        db_session,
        ContractCreate(
            title="Milestone Read Contract",
            total_value=Decimal("1500.00"),
            start_date=date.today(),
            client={
                "name": "Read Client",
                "email": "read-client@example.com",
            },
            freelancer={
                "name": "Read Freelancer",
                "email": "read-freelancer@example.com",
            },
        ),
    )

    return add_milestone(
        db_session,
        contract,
        MilestoneCreate(
            title="Deployment and Handover",
            amount=Decimal("1500.00"),
            deadline=date.today() + timedelta(days=30),
        ),
    )


def test_get_milestone_endpoint_returns_current_milestone(db_session):
    milestone = create_test_milestone(db_session)

    result = get_milestone_endpoint(
        milestone.id,
        db_session,
    )

    response = MilestoneResponse.model_validate(result)

    assert response.id == milestone.id
    assert response.contract_id == milestone.contract_id
    assert response.title == "Deployment and Handover"
    assert response.amount == Decimal("1500.00")
    assert response.deadline == milestone.deadline
    assert response.status == MilestoneStatus.PENDING


def test_get_milestone_endpoint_returns_404_for_missing_milestone(db_session):
    with pytest.raises(HTTPException) as exc_info:
        get_milestone_endpoint(
            9999,
            db_session,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Milestone not found."

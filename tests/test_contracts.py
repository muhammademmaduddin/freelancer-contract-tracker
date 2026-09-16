from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.core.exceptions import (
    ContractValueExceeded,
)
from app.schemas.contract import ContractCreate
from app.schemas.milestone import MilestoneCreate
from app.services.contract_service import (
    add_milestone,
    create_contract,
    get_contract_summary,
)


def create_test_contract(
    db_session,
    total_value: str = "1000.00",
):
    return create_contract(
        db_session,
        ContractCreate(
            title="Contract Reconciliation Test",
            total_value=Decimal(
                total_value
            ),
            start_date=date.today(),
            client={
                "name": "Contract Client",
                "email": "contract-client@example.com",
            },
            freelancer={
                "name": "Contract Freelancer",
                "email": "contract-freelancer@example.com",
            },
        ),
    )


def test_milestones_can_exactly_reconcile_contract(
    db_session,
):
    contract = create_test_contract(
        db_session
    )

    add_milestone(
        db_session,
        contract,
        MilestoneCreate(
            title="Phase One",
            amount=Decimal("600.00"),
            deadline=(
                date.today()
                + timedelta(days=7)
            ),
        ),
    )

    add_milestone(
        db_session,
        contract,
        MilestoneCreate(
            title="Phase Two",
            amount=Decimal("400.00"),
            deadline=(
                date.today()
                + timedelta(days=14)
            ),
        ),
    )

    summary = get_contract_summary(
        db_session,
        contract,
    )

    assert (
        summary["allocated_amount"]
        == Decimal("1000.00")
    )

    assert (
        summary["unallocated_amount"]
        == Decimal("0.00")
    )


def test_milestone_allocation_cannot_exceed_contract(
    db_session,
):
    contract = create_test_contract(
        db_session
    )

    add_milestone(
        db_session,
        contract,
        MilestoneCreate(
            title="Phase One",
            amount=Decimal("700.00"),
            deadline=(
                date.today()
                + timedelta(days=7)
            ),
        ),
    )

    with pytest.raises(
        ContractValueExceeded
    ):
        add_milestone(
            db_session,
            contract,
            MilestoneCreate(
                title="Phase Two",
                amount=Decimal("400.00"),
                deadline=(
                    date.today()
                    + timedelta(days=14)
                ),
            ),
        )

    summary = get_contract_summary(
        db_session,
        contract,
    )

    assert (
        summary["allocated_amount"]
        == Decimal("700.00")
    )

    assert (
        summary["unallocated_amount"]
        == Decimal("300.00")
    )


def test_partial_allocation_is_valid(
    db_session,
):
    contract = create_test_contract(
        db_session
    )

    add_milestone(
        db_session,
        contract,
        MilestoneCreate(
            title="Initial Phase",
            amount=Decimal("250.00"),
            deadline=(
                date.today()
                + timedelta(days=7)
            ),
        ),
    )

    summary = get_contract_summary(
        db_session,
        contract,
    )

    assert (
        summary["allocated_amount"]
        == Decimal("250.00")
    )

    assert (
        summary["unallocated_amount"]
        == Decimal("750.00")
    )
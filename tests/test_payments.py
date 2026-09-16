from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.core.enums import MilestoneStatus
from app.core.exceptions import (
    MilestoneNotFullyPaid,
    PaymentExceedsBalance,
)
from app.schemas.contract import ContractCreate
from app.schemas.milestone import MilestoneCreate
from app.schemas.payment import PaymentCreate
from app.services.contract_service import (
    add_milestone,
    create_contract,
)
from app.services.milestone_service import (
    update_milestone_status,
)
from app.services.payment_service import (
    get_amount_paid,
    get_outstanding_amount,
    record_payment,
)


def create_test_milestone(
    db_session,
    amount: str = "1000.00",
):
    contract = create_contract(
        db_session,
        ContractCreate(
            title="Payment Test Contract",
            total_value=Decimal(amount),
            start_date=date.today(),
            client={
                "name": "Test Client",
                "email": "payments-client@example.com",
            },
            freelancer={
                "name": "Test Freelancer",
                "email": "payments-freelancer@example.com",
            },
        ),
    )

    milestone = add_milestone(
        db_session,
        contract,
        MilestoneCreate(
            title="Backend Delivery",
            amount=Decimal(amount),
            deadline=(
                date.today()
                + timedelta(days=7)
            ),
        ),
    )

    return milestone


def approve_milestone(
    db_session,
    milestone,
):
    milestone = update_milestone_status(
        db_session,
        milestone,
        MilestoneStatus.IN_PROGRESS,
    )

    milestone = update_milestone_status(
        db_session,
        milestone,
        MilestoneStatus.SUBMITTED,
    )

    milestone = update_milestone_status(
        db_session,
        milestone,
        MilestoneStatus.APPROVED,
    )

    return milestone


def test_partial_payments_sum_correctly(
    db_session,
):
    milestone = create_test_milestone(
        db_session
    )

    record_payment(
        db_session,
        milestone,
        PaymentCreate(
            amount=Decimal("400.00"),
            reference="PAY-001",
        ),
    )

    record_payment(
        db_session,
        milestone,
        PaymentCreate(
            amount=Decimal("250.00"),
            reference="PAY-002",
        ),
    )

    amount_paid = get_amount_paid(
        db_session,
        milestone.id,
    )

    outstanding = get_outstanding_amount(
        db_session,
        milestone,
    )

    assert amount_paid == Decimal("650.00")
    assert outstanding == Decimal("350.00")


def test_overpayment_is_rejected(
    db_session,
):
    milestone = create_test_milestone(
        db_session
    )

    record_payment(
        db_session,
        milestone,
        PaymentCreate(
            amount=Decimal("800.00"),
            reference="PAY-001",
        ),
    )

    with pytest.raises(
        PaymentExceedsBalance
    ):
        record_payment(
            db_session,
            milestone,
            PaymentCreate(
                amount=Decimal("250.00"),
                reference="PAY-002",
            ),
        )

    assert (
        get_amount_paid(
            db_session,
            milestone.id,
        )
        == Decimal("800.00")
    )


def test_final_payment_marks_approved_milestone_paid(
    db_session,
):
    milestone = create_test_milestone(
        db_session
    )

    milestone = approve_milestone(
        db_session,
        milestone,
    )

    assert (
        milestone.status
        == MilestoneStatus.APPROVED
    )

    record_payment(
        db_session,
        milestone,
        PaymentCreate(
            amount=Decimal("500.00"),
            reference="FIRST-HALF",
        ),
    )

    assert (
        milestone.status
        == MilestoneStatus.APPROVED
    )

    record_payment(
        db_session,
        milestone,
        PaymentCreate(
            amount=Decimal("500.00"),
            reference="FINAL-HALF",
        ),
    )

    db_session.refresh(milestone)

    assert (
        milestone.status
        == MilestoneStatus.PAID
    )

    assert (
        get_amount_paid(
            db_session,
            milestone.id,
        )
        == Decimal("1000.00")
    )


def test_full_prepayment_becomes_paid_on_approval(
    db_session,
):
    milestone = create_test_milestone(
        db_session
    )

    record_payment(
        db_session,
        milestone,
        PaymentCreate(
            amount=Decimal("1000.00"),
            reference="FULL-UPFRONT",
        ),
    )

    assert (
        milestone.status
        == MilestoneStatus.PENDING
    )

    milestone = update_milestone_status(
        db_session,
        milestone,
        MilestoneStatus.IN_PROGRESS,
    )

    milestone = update_milestone_status(
        db_session,
        milestone,
        MilestoneStatus.SUBMITTED,
    )

    milestone = update_milestone_status(
        db_session,
        milestone,
        MilestoneStatus.APPROVED,
    )

    assert (
        milestone.status
        == MilestoneStatus.PAID
    )


def test_partially_paid_approved_milestone_cannot_be_manually_paid(
    db_session,
):
    milestone = create_test_milestone(
        db_session
    )

    milestone = approve_milestone(
        db_session,
        milestone,
    )

    record_payment(
        db_session,
        milestone,
        PaymentCreate(
            amount=Decimal("500.00"),
            reference="PARTIAL",
        ),
    )

    with pytest.raises(
        MilestoneNotFullyPaid
    ):
        update_milestone_status(
            db_session,
            milestone,
            MilestoneStatus.PAID,
        )
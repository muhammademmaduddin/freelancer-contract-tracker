from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import MilestoneStatus
from app.core.exceptions import (
    InvalidPaymentAmount,
    PaymentExceedsBalance,
)
from app.models.milestone import Milestone
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


def get_amount_paid(
    db: Session,
    milestone_id: int,
) -> Decimal:
    amount_paid = db.scalar(
        select(
            func.coalesce(
                func.sum(Payment.amount),
                Decimal("0.00"),
            )
        ).where(Payment.milestone_id == milestone_id)
    )

    return Decimal(amount_paid)


def get_outstanding_amount(
    db: Session,
    milestone: Milestone,
) -> Decimal:
    amount_paid = get_amount_paid(
        db,
        milestone.id,
    )

    return milestone.amount - amount_paid


def record_payment(
    db: Session,
    milestone: Milestone,
    payload: PaymentCreate,
) -> Payment:
    if payload.amount <= 0:
        raise InvalidPaymentAmount(
            "Payment amount must be greater than zero."
        )

    amount_paid = get_amount_paid(
        db,
        milestone.id,
    )

    outstanding_amount = (
        milestone.amount - amount_paid
    )

    if payload.amount > outstanding_amount:
        raise PaymentExceedsBalance(
            f"Payment exceeds outstanding balance. "
            f"Outstanding amount is {outstanding_amount}."
        )

    payment = Payment(
        amount=payload.amount,
        reference=payload.reference,
        milestone_id=milestone.id,
    )

    db.add(payment)
    db.flush()

    new_total_paid = amount_paid + payload.amount

    if (
        new_total_paid == milestone.amount
        and milestone.status == MilestoneStatus.APPROVED
    ):
        milestone.status = MilestoneStatus.PAID

    db.commit()
    db.refresh(payment)

    return payment
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import MilestoneStatus
from app.core.exceptions import MilestoneNotFullyPaid
from app.core.state_machine import validate_transition
from app.models.milestone import Milestone
from app.models.payment import Payment


def get_milestone_by_id(
    db: Session,
    milestone_id: int,
) -> Milestone | None:
    return db.get(
        Milestone,
        milestone_id,
    )


def update_milestone_status(
    db: Session,
    milestone: Milestone,
    new_status: MilestoneStatus,
) -> Milestone:
    validate_transition(
        milestone.status,
        new_status,
    )

    amount_paid = Decimal(
        db.scalar(
            select(
                func.coalesce(
                    func.sum(Payment.amount),
                    Decimal("0.00"),
                )
            ).where(
                Payment.milestone_id == milestone.id
            )
        )
    )

    if (
        new_status == MilestoneStatus.PAID
        and amount_paid != milestone.amount
    ):
        raise MilestoneNotFullyPaid(
            f"Milestone cannot be marked paid until full payment "
            f"is received. Paid {amount_paid} of {milestone.amount}."
        )

    milestone.status = new_status

    if (
        new_status == MilestoneStatus.APPROVED
        and amount_paid == milestone.amount
    ):
        milestone.status = MilestoneStatus.PAID

    db.commit()
    db.refresh(milestone)

    return milestone


def get_overdue_milestones(
    db: Session,
) -> list[Milestone]:
    excluded_statuses = [
        MilestoneStatus.APPROVED,
        MilestoneStatus.PAID,
    ]

    statement = (
        select(Milestone)
        .where(Milestone.deadline < date.today())
        .where(
            Milestone.status.not_in(
                excluded_statuses
            )
        )
        .order_by(Milestone.deadline.asc())
    )

    return list(
        db.scalars(statement).all()
    )


def is_overdue(
    milestone: Milestone,
) -> bool:
    return (
        milestone.deadline < date.today()
        and milestone.status
        not in {
            MilestoneStatus.APPROVED,
            MilestoneStatus.PAID,
        }
    )
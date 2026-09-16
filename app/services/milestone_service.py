from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import MilestoneStatus
from app.core.state_machine import validate_transition
from app.models.milestone import Milestone
from app.models.payment import Payment


def update_milestone_status(
    db: Session,
    milestone: Milestone,
    new_status: MilestoneStatus,
) -> Milestone:
    validate_transition(
        milestone.status,
        new_status,
    )

    milestone.status = new_status

    if new_status == MilestoneStatus.APPROVED:
        amount_paid = db.scalar(
            select(
                func.coalesce(
                    func.sum(Payment.amount),
                    Decimal("0.00"),
                )
            ).where(
                Payment.milestone_id == milestone.id
            )
        )

        amount_paid = Decimal(amount_paid)

        if amount_paid == milestone.amount:
            milestone.status = MilestoneStatus.PAID

    db.commit()
    db.refresh(milestone)

    return milestone
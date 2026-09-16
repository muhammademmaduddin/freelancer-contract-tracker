from sqlalchemy.orm import Session

from app.core.enums import MilestoneStatus
from app.core.state_machine import validate_transition
from app.models.dispute import Dispute
from app.models.milestone import Milestone
from app.schemas.dispute import DisputeCreate


def create_dispute(
    db: Session,
    milestone: Milestone,
    payload: DisputeCreate,
) -> Dispute:
    validate_transition(
        milestone.status,
        MilestoneStatus.DISPUTED,
    )

    dispute = Dispute(
        reason=payload.reason,
        milestone_id=milestone.id,
    )

    milestone.status = MilestoneStatus.DISPUTED

    db.add(dispute)
    db.commit()
    db.refresh(dispute)

    return dispute
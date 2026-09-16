from app.core.enums import MilestoneStatus
from app.core.exceptions import InvalidStateTransition


ALLOWED_TRANSITIONS: dict[
    MilestoneStatus,
    set[MilestoneStatus],
] = {
    MilestoneStatus.PENDING: {
        MilestoneStatus.IN_PROGRESS,
    },

    MilestoneStatus.IN_PROGRESS: {
        MilestoneStatus.SUBMITTED,
    },

    MilestoneStatus.SUBMITTED: {
        MilestoneStatus.APPROVED,
        MilestoneStatus.DISPUTED,
    },

    MilestoneStatus.DISPUTED: {
        MilestoneStatus.IN_PROGRESS,
        MilestoneStatus.SUBMITTED,
    },

    MilestoneStatus.APPROVED: {
        MilestoneStatus.PAID,
    },

    MilestoneStatus.PAID: set(),
}


def can_transition(
    current_status: MilestoneStatus,
    new_status: MilestoneStatus,
) -> bool:
    """
    Return True when the requested milestone status transition is allowed.
    """
    return new_status in ALLOWED_TRANSITIONS[current_status]


def validate_transition(
    current_status: MilestoneStatus,
    new_status: MilestoneStatus,
) -> None:
    """
    Validate a milestone status transition.

    Raises:
        InvalidStateTransition:
            If the requested transition is not permitted.
    """

    if current_status == new_status:
        raise InvalidStateTransition(
            f"Milestone is already '{current_status.value}'."
        )

    if not can_transition(current_status, new_status):
        raise InvalidStateTransition(
            f"Cannot transition milestone from "
            f"'{current_status.value}' to '{new_status.value}'."
        )
import pytest

from app.core.enums import MilestoneStatus
from app.core.exceptions import InvalidStateTransition
from app.core.state_machine import (
    can_transition,
    validate_transition,
)


@pytest.mark.parametrize(
    ("current_status", "new_status"),
    [
        (
            MilestoneStatus.PENDING,
            MilestoneStatus.IN_PROGRESS,
        ),
        (
            MilestoneStatus.IN_PROGRESS,
            MilestoneStatus.SUBMITTED,
        ),
        (
            MilestoneStatus.SUBMITTED,
            MilestoneStatus.APPROVED,
        ),
        (
            MilestoneStatus.SUBMITTED,
            MilestoneStatus.DISPUTED,
        ),
        (
            MilestoneStatus.DISPUTED,
            MilestoneStatus.IN_PROGRESS,
        ),
        (
            MilestoneStatus.DISPUTED,
            MilestoneStatus.SUBMITTED,
        ),
        (
            MilestoneStatus.APPROVED,
            MilestoneStatus.PAID,
        ),
    ],
)
def test_valid_transitions_are_allowed(
    current_status,
    new_status,
):
    assert (
        can_transition(
            current_status,
            new_status,
        )
        is True
    )

    validate_transition(
        current_status,
        new_status,
    )


@pytest.mark.parametrize(
    ("current_status", "new_status"),
    [
        (
            MilestoneStatus.PENDING,
            MilestoneStatus.PAID,
        ),
        (
            MilestoneStatus.PENDING,
            MilestoneStatus.APPROVED,
        ),
        (
            MilestoneStatus.IN_PROGRESS,
            MilestoneStatus.PAID,
        ),
        (
            MilestoneStatus.SUBMITTED,
            MilestoneStatus.PAID,
        ),
        (
            MilestoneStatus.PAID,
            MilestoneStatus.APPROVED,
        ),
        (
            MilestoneStatus.PENDING,
            MilestoneStatus.PENDING,
        ),
    ],
)
def test_invalid_transitions_are_rejected(
    current_status,
    new_status,
):
    with pytest.raises(
        InvalidStateTransition
    ):
        validate_transition(
            current_status,
            new_status,
        )
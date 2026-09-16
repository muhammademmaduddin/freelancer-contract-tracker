class DomainError(Exception):
    """Base exception for business-rule violations."""


class InvalidStateTransition(DomainError):
    """Raised when a milestone status transition is not allowed."""


class ContractValueExceeded(DomainError):
    """Raised when milestone allocation exceeds the contract total."""


class PaymentExceedsBalance(DomainError):
    """Raised when a payment exceeds the milestone's outstanding balance."""


class InvalidPaymentAmount(DomainError):
    """Raised when a payment amount is zero or negative."""


class MilestoneNotApproved(DomainError):
    """Raised when an operation requires an approved milestone."""


class MilestoneNotFullyPaid(DomainError):
    """Raised when a milestone is marked paid before full payment is received."""
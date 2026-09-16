from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    reference: str | None = Field(
        default=None,
        max_length=120,
    )


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    reference: str | None
    paid_at: datetime
    milestone_id: int


class PaymentSummaryResponse(BaseModel):
    milestone_id: int
    milestone_amount: Decimal

    amount_paid: Decimal
    outstanding_amount: Decimal
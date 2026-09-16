from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import MilestoneStatus


class MilestoneCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    deadline: date


class MilestoneStatusUpdate(BaseModel):
    status: MilestoneStatus


class MilestoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    amount: Decimal
    deadline: date
    status: MilestoneStatus
    contract_id: int


class OverdueMilestoneResponse(MilestoneResponse):
    days_overdue: int
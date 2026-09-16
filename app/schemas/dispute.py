from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DisputeCreate(BaseModel):
    reason: str = Field(
        min_length=3,
        max_length=2000,
    )


class DisputeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reason: str
    created_at: datetime
    milestone_id: int
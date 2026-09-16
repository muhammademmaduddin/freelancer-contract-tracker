from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: str = Field(min_length=3, max_length=255)


class FreelancerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: str = Field(min_length=3, max_length=255)


class ContractCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    total_value: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    start_date: date

    client: ClientCreate
    freelancer: FreelancerCreate


class ContractResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    total_value: Decimal
    start_date: date
    client_id: int
    freelancer_id: int


class ContractSummaryResponse(BaseModel):
    contract_id: int
    title: str

    total_value: Decimal
    allocated_amount: Decimal
    unallocated_amount: Decimal

    total_paid: Decimal
    outstanding_amount: Decimal

    pending_amount: Decimal
    overdue_milestones: int
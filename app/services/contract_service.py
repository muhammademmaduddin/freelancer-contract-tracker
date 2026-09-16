from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import MilestoneStatus
from app.core.exceptions import ContractValueExceeded
from app.models.client import Client
from app.models.contract import Contract
from app.models.freelancer import Freelancer
from app.models.milestone import Milestone
from app.models.payment import Payment
from app.schemas.contract import ContractCreate
from app.schemas.milestone import MilestoneCreate


def get_contract_by_id(
    db: Session,
    contract_id: int,
) -> Contract | None:
    return db.get(
        Contract,
        contract_id,
    )


def create_contract(
    db: Session,
    payload: ContractCreate,
) -> Contract:
    client = db.scalar(
        select(Client).where(
            Client.email == payload.client.email
        )
    )

    if client is None:
        client = Client(
            name=payload.client.name,
            email=payload.client.email,
        )
        db.add(client)

    freelancer = db.scalar(
        select(Freelancer).where(
            Freelancer.email == payload.freelancer.email
        )
    )

    if freelancer is None:
        freelancer = Freelancer(
            name=payload.freelancer.name,
            email=payload.freelancer.email,
        )
        db.add(freelancer)

    db.flush()

    contract = Contract(
        title=payload.title,
        total_value=payload.total_value,
        start_date=payload.start_date,
        client_id=client.id,
        freelancer_id=freelancer.id,
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)

    return contract


def add_milestone(
    db: Session,
    contract: Contract,
    payload: MilestoneCreate,
) -> Milestone:
    allocated_amount = db.scalar(
        select(
            func.coalesce(
                func.sum(Milestone.amount),
                Decimal("0.00"),
            )
        ).where(
            Milestone.contract_id == contract.id
        )
    )

    allocated_amount = Decimal(allocated_amount)

    new_total = allocated_amount + payload.amount

    if new_total > contract.total_value:
        remaining_amount = (
            contract.total_value - allocated_amount
        )

        raise ContractValueExceeded(
            f"Milestone amount exceeds remaining contract value. "
            f"Remaining amount is {remaining_amount}."
        )

    milestone = Milestone(
        title=payload.title,
        amount=payload.amount,
        deadline=payload.deadline,
        contract_id=contract.id,
    )

    db.add(milestone)
    db.commit()
    db.refresh(milestone)

    return milestone


def get_contract_summary(
    db: Session,
    contract: Contract,
) -> dict:
    allocated_amount = db.scalar(
        select(
            func.coalesce(
                func.sum(Milestone.amount),
                Decimal("0.00"),
            )
        ).where(
            Milestone.contract_id == contract.id
        )
    )

    total_paid = db.scalar(
        select(
            func.coalesce(
                func.sum(Payment.amount),
                Decimal("0.00"),
            )
        )
        .join(Milestone)
        .where(
            Milestone.contract_id == contract.id
        )
    )

    overdue_count = db.scalar(
        select(
            func.count(Milestone.id)
        )
        .where(
            Milestone.contract_id == contract.id
        )
        .where(
            Milestone.deadline < date.today()
        )
        .where(
            Milestone.status.not_in(
                [
                    MilestoneStatus.APPROVED,
                    MilestoneStatus.PAID,
                ]
            )
        )
    )

    allocated_amount = Decimal(allocated_amount)
    total_paid = Decimal(total_paid)

    unallocated_amount = (
        contract.total_value - allocated_amount
    )

    outstanding_amount = (
        contract.total_value - total_paid
    )

    pending_amount = (
        allocated_amount - total_paid
    )

    return {
        "contract_id": contract.id,
        "title": contract.title,
        "total_value": contract.total_value,
        "allocated_amount": allocated_amount,
        "unallocated_amount": unallocated_amount,
        "total_paid": total_paid,
        "outstanding_amount": outstanding_amount,
        "pending_amount": pending_amount,
        "overdue_milestones": overdue_count,
    }
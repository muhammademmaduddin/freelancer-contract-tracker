from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import MilestoneStatus
from app.db.base import Base


class Milestone(Base):
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    deadline: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[MilestoneStatus] = mapped_column(
        Enum(
            MilestoneStatus,
            native_enum=False,
        ),
        default=MilestoneStatus.PENDING,
        nullable=False,
    )

    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
    )

    contract: Mapped["Contract"] = relationship(
        back_populates="milestones"
    )

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="milestone",
        cascade="all, delete-orphan",
    )

    disputes: Mapped[list["Dispute"]] = relationship(
        back_populates="milestone",
        cascade="all, delete-orphan",
    )
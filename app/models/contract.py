from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    total_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
    )

    freelancer_id: Mapped[int] = mapped_column(
        ForeignKey("freelancers.id", ondelete="CASCADE"),
        nullable=False,
    )

    client: Mapped["Client"] = relationship(
        back_populates="contracts"
    )

    freelancer: Mapped["Freelancer"] = relationship(
        back_populates="contracts"
    )

    milestones: Mapped[list["Milestone"]] = relationship(
        back_populates="contract",
        cascade="all, delete-orphan",
    )
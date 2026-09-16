from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Dispute(Base):
    __tablename__ = "disputes"

    id: Mapped[int] = mapped_column(primary_key=True)

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    milestone_id: Mapped[int] = mapped_column(
        ForeignKey("milestones.id", ondelete="CASCADE"),
        nullable=False,
    )

    milestone: Mapped["Milestone"] = relationship(
        back_populates="disputes"
    )
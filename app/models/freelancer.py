from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Freelancer(Base):
    __tablename__ = "freelancers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    contracts: Mapped[list["Contract"]] = relationship(
        back_populates="freelancer",
        cascade="all, delete-orphan",
    )
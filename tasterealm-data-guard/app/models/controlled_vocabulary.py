from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ControlledVocabularies(Base):
    __tablename__ = "controlled_vocabularies"
    __table_args__ = {"schema": "validation"}

    vocab_set: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String, primary_key=True)
    display_label: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    parent_value: Mapped[str | None] = mapped_column(String, nullable=True)

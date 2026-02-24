from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import DateTime, Integer, String, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Batches(Base):
    __tablename__ = "batches"
    __table_args__ = {"schema": "staging"}

    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    batch_name: Mapped[str] = mapped_column(String)
    imported_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"))
    imported_by: Mapped[str] = mapped_column(String)
    batch_status: Mapped[str] = mapped_column(String, default="pending")
    total_records: Mapped[int] = mapped_column(Integer)
    runs: Mapped[list["ValidationRuns"]] = relationship(back_populates="batch")

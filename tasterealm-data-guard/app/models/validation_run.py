from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, String, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ValidationRuns(Base):
    __tablename__ = "validation_runs"
    __table_args__ = {"schema": "validation"}

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staging.batches.batch_id"),
    )
    started_at: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String)
    records_passed: Mapped[int] = mapped_column(Integer)
    records_failed: Mapped[int] = mapped_column(Integer)

    batch: Mapped["Batches"] = relationship(back_populates="runs")
    results: Mapped[list["ValidationResults"]] = relationship(back_populates="run")

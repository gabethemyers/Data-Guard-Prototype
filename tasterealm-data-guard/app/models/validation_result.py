from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ValidationResults(Base):
    __tablename__ = "validation_results"
    __table_args__ = {"schema": "validation"}

    result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("validation.validation_runs.run_id"),
    )
    staged_dish_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staging.staged_dishes.dish_id"),
    )
    overall_status: Mapped[str] = mapped_column(String)

    run: Mapped["ValidationRuns"] = relationship(back_populates="results")

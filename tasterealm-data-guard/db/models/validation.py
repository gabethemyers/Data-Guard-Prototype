from db.models.base import Base
from db.models.enums import Severity, severity_enum

# fix to stop circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from db.models.staging import Batches

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UUID, text
from datetime import datetime
import uuid




class RuleDefinitions(Base):
    __tablename__ = "rule_definitions"
    __table_args__ = {"schema": "validation"}

    rule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    invariant_id: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    scope: Mapped[str | None] = mapped_column(String, nullable=True)
    fields_involved: Mapped[str | None] = mapped_column(String, nullable=True)
    condition_logic: Mapped[str | None] = mapped_column(String, nullable=True)
    rule_logic: Mapped[str | None] = mapped_column(String, nullable=True)
    severity: Mapped[Severity] = mapped_column(severity_enum)
    error_code: Mapped[str] = mapped_column(String)
    error_message_template: Mapped[str] = mapped_column(String)
    autofix_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    autofix_logic: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class ValidationRuns(Base):
    __tablename__ = "validation_runs"
    __table_args__ = {"schema": "validation"}

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
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

class ValidationResults(Base):
    __tablename__ = "validation_results"
    __table_args__ = {"schema": "validation"}

    result_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
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


class Issues(Base):
    __tablename__ = "issues"
    __table_args__ = {"schema": "validation"}

    issue_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("validation.validation_results.result_id"),
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("validation.rule_definitions.rule_id"),
    )
    field_name: Mapped[str] = mapped_column(String)
    field_value: Mapped[str | None] = mapped_column(String, nullable=True)
    error_code: Mapped[str] = mapped_column(String)
    error_message: Mapped[str] = mapped_column(String)
    severity: Mapped[Severity] = mapped_column(severity_enum)


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

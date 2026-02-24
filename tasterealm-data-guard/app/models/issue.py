import uuid

from sqlalchemy import ForeignKey, String, UUID, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import Severity, severity_enum


class Issues(Base):
    __tablename__ = "issues"
    __table_args__ = {"schema": "validation"}

    issue_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
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

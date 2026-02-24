import uuid

from sqlalchemy import Boolean, String, UUID, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import Severity, severity_enum


class RuleDefinitions(Base):
    __tablename__ = "rule_definitions"
    __table_args__ = {"schema": "validation"}

    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
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

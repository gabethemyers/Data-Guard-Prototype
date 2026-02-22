from db.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, UUID, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import text
from datetime import datetime
import uuid

class Batches(Base):
    __tablename__ = "batches"
    __table_args__ = {"schema": "staging"}
    
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    batch_name: Mapped[str] = mapped_column(String)
    imported_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"))
    imported_by: Mapped[str] = mapped_column(String)
    batch_status: Mapped[str] = mapped_column(String, default="pending")
    total_records: Mapped[int] = mapped_column(Integer)


class StagedDish(Base):
    __tablename__ = "staged_dishes"
    __table_args__ = {"schema": "staging"}

    dish_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    dish_name: Mapped[str | None] = mapped_column(String, nullable=True)
    dish_name_local: Mapped[str | None] = mapped_column(String, nullable=True)
    canonical_slug: Mapped[str | None] = mapped_column(String, nullable=True)
    primary_cuisine: Mapped[str | None] = mapped_column(String, nullable=True, default="unknown")
    course_type: Mapped[str | None] = mapped_column(String, nullable=True)
    dish_category: Mapped[str | None] = mapped_column(String, nullable=True)
    meal_timing: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True, server_default=text("'{}'"))    
    description_short: Mapped[str | None] = mapped_column(String, nullable=True)
    taste_active_sweet: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    taste_active_salty: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    taste_active_sour: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    taste_active_spicy: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    taste_active_umami: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    taste_active_bitter: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    taste_active_overall_confidence: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True, default=0)
    allergen_confidence: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True, default=0)
    allergen_contains_milk: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_egg: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_wheat: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_soy: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_peanut: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_tree_nut: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_fish: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_shellfish: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_sesame: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    allergen_contains_gluten: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    diet_vegan: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    diet_vegetarian: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    diet_gluten_free: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    diet_dairy_free: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    is_pork_present: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    is_alcohol_present: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    validation_status: Mapped[str | None] = mapped_column(String, nullable=True, default="pending")
    qa_status: Mapped[str | None] = mapped_column(String, nullable=True)
    requires_manual_review: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    data_source: Mapped[str | None] = mapped_column(String, nullable=True)
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("staging.batches.batch_id"), nullable=False)
    

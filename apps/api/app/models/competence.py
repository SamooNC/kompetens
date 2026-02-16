"""Competence model -- skills extracted from voice inventory or entered manually."""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Competence(TimestampMixin, Base):
    """Competence rattachee a un profil.

    Chaque competence peut etre liee a un code ROME et dispose d'un niveau
    et d'une source indiquant son origine (vocale, manuelle, inferee par le LLM).
    """

    __tablename__ = "competences"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Intitule de la competence",
    )
    code_rome: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        comment="Code ROME associe (ex: F1702)",
    )
    niveau: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        comment="debutant | intermediaire | confirme | expert",
    )
    source: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="voice | manual | inferred",
    )

    # --- relationship ---
    profile: Mapped["Profile"] = relationship(  # noqa: F821
        back_populates="competences",
    )

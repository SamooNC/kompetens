"""Experience model -- professional experiences declared by candidates."""

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Experience(TimestampMixin, Base):
    """Experience professionnelle rattachee a un profil.

    Peut provenir de l'inventaire vocal (transcription LLM) ou d'une saisie
    manuelle / assistee par un aidant.
    """

    __tablename__ = "experiences"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    intitule: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Intitule du poste ou de l'activite",
    )
    contexte: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Description libre du contexte de l'experience",
    )
    duree_estimee: Mapped[str | None] = mapped_column(
        String(60),
        nullable=True,
        comment="Ex: 3 ans, 6 mois, 2 saisons",
    )

    # --- relationship ---
    profile: Mapped["Profile"] = relationship(  # noqa: F821
        back_populates="experiences",
    )

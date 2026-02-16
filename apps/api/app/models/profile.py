"""Profile model -- candidate/recruiter profile with embedding vector."""

import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Profile(TimestampMixin, Base):
    """Profil d'un utilisateur.

    Contient les informations metier : zone geographique, disponibilite,
    resume genere par le LLM et vecteur d'embedding pour le matching semantique.
    """

    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    zone_geographique: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
        comment="Ex: Noumea, Kone, Lifou",
    )
    disponibilite: Mapped[str | None] = mapped_column(
        String(60),
        nullable=True,
        comment="Ex: immediate, 1 mois, 3 mois",
    )
    resume_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Resume genere par le LLM a partir de l'inventaire vocal",
    )
    embedding = mapped_column(
        Vector(1024),
        nullable=True,
        comment="Vecteur d'embedding (e5-multilingual, dim 1024)",
    )

    # --- relationships ---
    user: Mapped["User"] = relationship(  # noqa: F821
        back_populates="profiles",
    )
    competences: Mapped[list["Competence"]] = relationship(  # noqa: F821
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    experiences: Mapped[list["Experience"]] = relationship(  # noqa: F821
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    badges: Mapped[list["Badge"]] = relationship(  # noqa: F821
        back_populates="recipient",
        cascade="all, delete-orphan",
    )

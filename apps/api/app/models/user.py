"""User model -- authentication and role management."""

import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    """Utilisateur de la plateforme Kompetens.

    Roles:
        - candidat: chercheur d'emploi (Celine, Steeve, ...)
        - recruteur: employeur (Didier)
        - aidant: accompagnateur (Nadia)
        - admin: administrateur systeme
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str | None] = mapped_column(
        String(320),
        unique=True,
        nullable=True,
    )
    hashed_password: Mapped[str | None] = mapped_column(
        String(256),
        nullable=True,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="candidat | recruteur | aidant | admin",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # --- relationships ---
    profiles: Mapped[list["Profile"]] = relationship(  # noqa: F821
        back_populates="user",
        cascade="all, delete-orphan",
    )
    consents: Mapped[list["Consent"]] = relationship(  # noqa: F821
        back_populates="user",
        cascade="all, delete-orphan",
    )

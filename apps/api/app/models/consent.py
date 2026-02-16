"""Consent model -- RGPD consent records with optional audio proof."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Consent(Base):
    """Consentement RGPD enregistre pour un utilisateur.

    Le consentement peut etre oral (avec hash audio SHA-256 comme preuve)
    ou ecrit. Chaque type de traitement requiert un consentement distinct.

    Types:
        - data_collection: collecte de donnees personnelles
        - voice_recording: enregistrement audio
        - matching: mise en relation candidat/recruteur
        - badge_issuance: emission de badges
    """

    __tablename__ = "consents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        comment="data_collection | voice_recording | matching | badge_issuance",
    )
    audio_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment="SHA-256 du fichier audio de consentement oral",
    )
    audio_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Chemin vers le fichier audio de consentement",
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # --- relationship ---
    user: Mapped["User"] = relationship(  # noqa: F821
        back_populates="consents",
    )

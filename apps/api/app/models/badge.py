"""Badge model -- Open Badges v3 credentials for verified competences."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Badge(TimestampMixin, Base):
    """Credential Open Badges v3.

    Un badge atteste d'une competence verifiee. Il est signe avec Ed25519
    et peut etre endosse par un tiers (aidant, employeur, formateur).

    Lifecycle: pending -> issued -> (revoked)
    """

    __tablename__ = "badges"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    achievement_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        comment="Code interne de l'achievement (ex: COMP-F1702-001)",
    )
    achievement_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Libelle lisible de l'achievement",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="pending | issued | revoked",
    )
    credential_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        comment="Full Open Badge v3 credential (JSON-LD)",
    )
    signature: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Ed25519 signature of the credential",
    )
    endorser_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="Utilisateur ayant endosse le badge",
    )
    issued_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # --- relationships ---
    recipient: Mapped["Profile"] = relationship(  # noqa: F821
        back_populates="badges",
    )
    endorser: Mapped["User | None"] = relationship(  # noqa: F821
        foreign_keys=[endorser_id],
    )

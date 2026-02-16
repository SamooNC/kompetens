"""Initial schema -- all core tables for the Kompetens POC.

Revision ID: 001
Revises: None
Create Date: 2026-02-16

Creates extensions: pgvector, pg_trgm
Creates tables: users, profiles, competences, experiences, badges,
    consents, rome_metiers, rome_competences, rome_appellations
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # -- Extensions --
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # -- users --
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(320), unique=True, nullable=True),
        sa.Column("hashed_password", sa.String(256), nullable=True),
        sa.Column(
            "role",
            sa.String(20),
            nullable=False,
            comment="candidat | recruteur | aidant | admin",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # -- profiles --
    op.create_table(
        "profiles",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "zone_geographique",
            sa.String(120),
            nullable=True,
            comment="Ex: Noumea, Kone, Lifou",
        ),
        sa.Column(
            "disponibilite",
            sa.String(60),
            nullable=True,
            comment="Ex: immediate, 1 mois, 3 mois",
        ),
        sa.Column(
            "resume_text",
            sa.Text(),
            nullable=True,
            comment="Resume genere par le LLM a partir de l'inventaire vocal",
        ),
        sa.Column(
            "embedding",
            Vector(1024),
            nullable=True,
            comment="Vecteur d'embedding (e5-multilingual, dim 1024)",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # -- competences --
    op.create_table(
        "competences",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "profile_id",
            sa.Uuid(),
            sa.ForeignKey("profiles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "label",
            sa.String(255),
            nullable=False,
            comment="Intitule de la competence",
        ),
        sa.Column(
            "code_rome",
            sa.String(10),
            nullable=True,
            comment="Code ROME associe (ex: F1702)",
        ),
        sa.Column(
            "niveau",
            sa.String(30),
            nullable=True,
            comment="debutant | intermediaire | confirme | expert",
        ),
        sa.Column(
            "source",
            sa.String(20),
            nullable=False,
            comment="voice | manual | inferred",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # -- experiences --
    op.create_table(
        "experiences",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "profile_id",
            sa.Uuid(),
            sa.ForeignKey("profiles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "intitule",
            sa.String(255),
            nullable=False,
            comment="Intitule du poste ou de l'activite",
        ),
        sa.Column(
            "contexte",
            sa.Text(),
            nullable=True,
            comment="Description libre du contexte de l'experience",
        ),
        sa.Column(
            "duree_estimee",
            sa.String(60),
            nullable=True,
            comment="Ex: 3 ans, 6 mois, 2 saisons",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # -- badges --
    op.create_table(
        "badges",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "recipient_id",
            sa.Uuid(),
            sa.ForeignKey("profiles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "achievement_code",
            sa.String(30),
            nullable=False,
            comment="Code interne de l'achievement (ex: COMP-F1702-001)",
        ),
        sa.Column(
            "achievement_name",
            sa.String(255),
            nullable=False,
            comment="Libelle lisible de l'achievement",
        ),
        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default=sa.text("'pending'"),
            comment="pending | issued | revoked",
        ),
        sa.Column(
            "credential_json",
            sa.JSON(),
            nullable=True,
            comment="Full Open Badge v3 credential (JSON-LD)",
        ),
        sa.Column(
            "signature",
            sa.Text(),
            nullable=True,
            comment="Ed25519 signature of the credential",
        ),
        sa.Column(
            "endorser_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
            comment="Utilisateur ayant endosse le badge",
        ),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # -- consents --
    op.create_table(
        "consents",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "type",
            sa.String(30),
            nullable=False,
            comment="data_collection | voice_recording | matching | badge_issuance",
        ),
        sa.Column(
            "audio_hash",
            sa.String(64),
            nullable=True,
            comment="SHA-256 du fichier audio de consentement oral",
        ),
        sa.Column(
            "audio_path",
            sa.String(500),
            nullable=True,
            comment="Chemin vers le fichier audio de consentement",
        ),
        sa.Column(
            "granted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )

    # -- rome_metiers --
    op.create_table(
        "rome_metiers",
        sa.Column(
            "code_rome",
            sa.String(10),
            primary_key=True,
            comment="Code ROME (ex: F1702)",
        ),
        sa.Column(
            "libelle",
            sa.String(255),
            nullable=False,
            comment="Libelle du metier",
        ),
        sa.Column(
            "definition",
            sa.Text(),
            nullable=True,
            comment="Definition detaillee du metier",
        ),
    )
    op.execute(
        "CREATE INDEX ix_rome_metiers_libelle_trgm "
        "ON rome_metiers USING gin (libelle gin_trgm_ops)"
    )

    # -- rome_competences --
    op.create_table(
        "rome_competences",
        sa.Column(
            "code",
            sa.String(20),
            primary_key=True,
            comment="Code competence ROME",
        ),
        sa.Column(
            "libelle",
            sa.String(255),
            nullable=False,
            comment="Libelle de la competence",
        ),
        sa.Column(
            "type_competence",
            sa.String(30),
            nullable=False,
            comment="savoir-faire | savoir-etre | savoir",
        ),
    )

    # -- rome_appellations --
    op.create_table(
        "rome_appellations",
        sa.Column(
            "code",
            sa.String(20),
            primary_key=True,
            comment="Code appellation ROME",
        ),
        sa.Column(
            "libelle",
            sa.String(255),
            nullable=False,
            comment="Intitule de l'appellation",
        ),
        sa.Column(
            "code_rome",
            sa.String(10),
            sa.ForeignKey("rome_metiers.code_rome", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.execute(
        "CREATE INDEX ix_rome_appellations_libelle_trgm "
        "ON rome_appellations USING gin (libelle gin_trgm_ops)"
    )


def downgrade() -> None:
    op.drop_table("rome_appellations")
    op.drop_table("rome_competences")
    op.drop_table("rome_metiers")
    op.drop_table("consents")
    op.drop_table("badges")
    op.drop_table("experiences")
    op.drop_table("competences")
    op.drop_table("profiles")
    op.drop_table("users")
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
    op.execute("DROP EXTENSION IF EXISTS vector")

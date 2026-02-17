"""Add emergent referential tables (raw_offers, extracted_skills, emergent_skills).

Revision ID: 002
Revises: 001
Create Date: 2026-02-18

Adds the three tables for the emergent competency referential pipeline (E-10b):
- raw_offers: raw job offers collected from NC sources
- extracted_skills: skills extracted from offers by LLM
- emergent_skills: canonical skills after clustering (the referential)

Also adds emergent_skill_id FK on the existing competences table.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: str = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # -- raw_offers --
    op.create_table(
        "raw_offers",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "source",
            sa.String(50),
            nullable=False,
            comment="emploi_nc | dtefp_csv | facebook | aidant",
        ),
        sa.Column("source_url", sa.String(1000), nullable=True),
        sa.Column(
            "text",
            sa.Text(),
            nullable=False,
            comment="Texte brut de l'offre",
        ),
        sa.Column(
            "zone",
            sa.String(120),
            nullable=True,
            comment="Zone geographique (Noumea, Kone, Lifou...)",
        ),
        sa.Column(
            "sector",
            sa.String(120),
            nullable=True,
            comment="Secteur d'activite si identifie",
        ),
        sa.Column(
            "collected_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "processed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
            comment="True si l'offre a ete traitee par le LLM",
        ),
    )

    # -- emergent_skills (created before extracted_skills for FK) --
    op.create_table(
        "emergent_skills",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "canonical_label",
            sa.String(255),
            nullable=False,
            comment="Label canonique de la competence emergente",
        ),
        sa.Column(
            "variant_labels",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
            comment="Labels variantes issus du clustering",
        ),
        sa.Column(
            "frequency",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
            comment="Nombre d'offres mentionnant cette competence",
        ),
        sa.Column(
            "sectors",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
            comment="Secteurs d'activite associes",
        ),
        sa.Column(
            "zones",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
            comment="Zones geographiques associees",
        ),
        sa.Column(
            "embedding",
            Vector(1024),
            nullable=True,
            comment="Vecteur d'embedding (e5-multilingual, dim 1024)",
        ),
        sa.Column(
            "rome_code",
            sa.String(10),
            nullable=True,
            comment="Code ROME v4 associe si similarite > 0.8 (arriere-plan)",
        ),
        sa.Column(
            "rome_label",
            sa.String(255),
            nullable=True,
            comment="Libelle ROME associe",
        ),
        sa.Column(
            "first_seen",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "last_seen",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # -- extracted_skills --
    op.create_table(
        "extracted_skills",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "offer_id",
            sa.Uuid(),
            sa.ForeignKey("raw_offers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "label",
            sa.String(255),
            nullable=False,
            comment="Competence extraite par le LLM (mots de l'offre)",
        ),
        sa.Column(
            "level",
            sa.String(30),
            nullable=True,
            comment="debutant | intermediaire | confirme | expert",
        ),
        sa.Column(
            "context",
            sa.String(255),
            nullable=True,
            comment="Contexte d'extraction (chantier, mine, service...)",
        ),
        sa.Column(
            "emergent_skill_id",
            sa.Uuid(),
            sa.ForeignKey("emergent_skills.id", ondelete="SET NULL"),
            nullable=True,
            comment="Competence canonique apres clustering",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # -- Add emergent_skill_id to existing competences table --
    op.add_column(
        "competences",
        sa.Column(
            "emergent_skill_id",
            sa.Uuid(),
            sa.ForeignKey("emergent_skills.id", ondelete="SET NULL"),
            nullable=True,
            comment="Lien vers la competence emergente (referentiel prioritaire)",
        ),
    )


def downgrade() -> None:
    op.drop_column("competences", "emergent_skill_id")
    op.drop_table("extracted_skills")
    op.drop_table("emergent_skills")
    op.drop_table("raw_offers")

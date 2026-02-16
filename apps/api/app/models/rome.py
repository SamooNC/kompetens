"""ROME v4 taxonomy models -- metiers, competences, and appellations.

The ROME (Repertoire Operationnel des Metiers et des Emplois) is the French
national job taxonomy maintained by Pole Emploi / France Travail. Kompetens
uses it as the backbone for competence mapping and matching.
"""

from sqlalchemy import ForeignKey, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class RomeMetier(Base):
    """Fiche metier ROME (ex: F1702 - Installation electrique).

    Le code ROME est compose d'une lettre (domaine) + 4 chiffres.
    """

    __tablename__ = "rome_metiers"

    code_rome: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
        comment="Code ROME (ex: F1702)",
    )
    libelle: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Libelle du metier",
    )
    definition: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Definition detaillee du metier",
    )

    # --- relationships ---
    appellations: Mapped[list["RomeAppellation"]] = relationship(
        back_populates="metier",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "ix_rome_metiers_libelle_trgm",
            text("libelle gin_trgm_ops"),
            postgresql_using="gin",
        ),
    )


class RomeCompetence(Base):
    """Competence du referentiel ROME.

    Types:
        - savoir-faire: competences techniques et operationnelles
        - savoir-etre: competences comportementales
        - savoir: connaissances theoriques
    """

    __tablename__ = "rome_competences"

    code: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
        comment="Code competence ROME",
    )
    libelle: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Libelle de la competence",
    )
    type_competence: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        comment="savoir-faire | savoir-etre | savoir",
    )


class RomeAppellation(Base):
    """Appellation d'emploi rattachee a une fiche metier ROME.

    Les appellations sont les intitules de poste concrets lies a un metier.
    Ex: pour F1702 (Installation electrique) -> "Electricien du batiment",
    "Monteur electricien", etc.
    """

    __tablename__ = "rome_appellations"

    code: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
        comment="Code appellation ROME",
    )
    libelle: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Intitule de l'appellation",
    )
    code_rome: Mapped[str] = mapped_column(
        ForeignKey("rome_metiers.code_rome", ondelete="CASCADE"),
        nullable=False,
    )

    # --- relationship ---
    metier: Mapped["RomeMetier"] = relationship(
        back_populates="appellations",
    )

    __table_args__ = (
        Index(
            "ix_rome_appellations_libelle_trgm",
            text("libelle gin_trgm_ops"),
            postgresql_using="gin",
        ),
    )

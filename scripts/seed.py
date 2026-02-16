#!/usr/bin/env python3
"""Seed script -- populate Kompetens database with realistic test data.

Creates 10 users with profiles, competences, and experiences based on
the project personas (Celine, Steeve, Marie, Jean, Paul, Lea, Thomas,
Sophie, Nadia, Didier).

Usage:
    python scripts/seed.py

Reads DATABASE_URL_SYNC from environment or .env file.
Idempotent: uses INSERT ... ON CONFLICT DO NOTHING.
"""

import os
import sys
import uuid
from pathlib import Path

import psycopg

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Try to load .env from the api directory or project root
for env_path in [
    Path(__file__).resolve().parent.parent / "apps" / "api" / ".env",
    Path(__file__).resolve().parent.parent / ".env",
]:
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
        break

DATABASE_URL = os.environ.get(
    "DATABASE_URL_SYNC",
    "postgresql://kompetens:kompetens_dev@localhost:5432/kompetens",
)

# Strip the +psycopg driver prefix if present -- psycopg uses plain postgresql://
CONNINFO = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")

# ---------------------------------------------------------------------------
# Stable UUIDs for reproducibility (derived from names)
# ---------------------------------------------------------------------------


def stable_uuid(name: str) -> str:
    """Generate a deterministic UUID v5 from a name (DNS namespace)."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"kompetens.nc.{name}"))


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

USERS = [
    # (uuid, email, role, zone, disponibilite, resume_text)
    {
        "id": stable_uuid("celine"),
        "email": "celine@test.kompetens.nc",
        "role": "candidat",
        "zone": "Dumbéa",
        "dispo": "immédiate",
        "resume": (
            "Conductrice d'engin expérimentée, spécialisée dans les chantiers "
            "de terrassement en Nouvelle-Calédonie. Autonome sur pelle et "
            "tombereaux, habituée aux conditions de chantier difficiles."
        ),
    },
    {
        "id": stable_uuid("steeve"),
        "email": "steeve@test.kompetens.nc",
        "role": "candidat",
        "zone": "Nouméa",
        "dispo": "1 mois",
        "resume": (
            "Ancien mineur reconverti, polyvalent en maintenance d'engins "
            "et soudure. Cherche un poste stable après la crise du nickel."
        ),
    },
    {
        "id": stable_uuid("marie"),
        "email": "marie@test.kompetens.nc",
        "role": "candidat",
        "zone": "Koné",
        "dispo": "immédiate",
        "resume": (
            "Aide ménagère rigoureuse, expérimentée dans l'entretien de "
            "maisons et la préparation de repas. Disponible rapidement."
        ),
    },
    {
        "id": stable_uuid("jean"),
        "email": "jean@test.kompetens.nc",
        "role": "candidat",
        "zone": "Bourail",
        "dispo": "immédiate",
        "resume": (
            "Agriculteur polyvalent, maîtrise les cultures maraîchères "
            "tropicales, la taille et la conduite de tracteur. 15 ans "
            "d'expérience en brousse."
        ),
    },
    {
        "id": stable_uuid("paul"),
        "email": "paul@test.kompetens.nc",
        "role": "candidat",
        "zone": "Nouméa",
        "dispo": "immédiate",
        "resume": (
            "Serveur dynamique avec expérience en restauration rapide "
            "et traditionnelle. Bon contact client, ponctuel."
        ),
    },
    {
        "id": stable_uuid("lea"),
        "email": "lea@test.kompetens.nc",
        "role": "candidat",
        "zone": "Mont-Dore",
        "dispo": "1 mois",
        "resume": (
            "Vendeuse conseil en prêt-à-porter et grande distribution. "
            "Sens du service, à l'aise avec l'encaissement."
        ),
    },
    {
        "id": stable_uuid("thomas"),
        "email": "thomas@test.kompetens.nc",
        "role": "candidat",
        "zone": "Pouembout",
        "dispo": "3 mois",
        "resume": (
            "Charpentier qualifié, lecture de plans et pose de charpentes "
            "traditionnelles. Disponible après fin de chantier en cours."
        ),
    },
    {
        "id": stable_uuid("sophie"),
        "email": "sophie@test.kompetens.nc",
        "role": "candidat",
        "zone": "Lifou",
        "dispo": "immédiate",
        "resume": (
            "Pêcheuse côtière expérimentée, connaissance des eaux "
            "calédoniennes, maniement des filets et navigation."
        ),
    },
    {
        "id": stable_uuid("nadia"),
        "email": "nadia@test.kompetens.nc",
        "role": "aidant",
        "zone": "Nouméa",
        "dispo": None,
        "resume": None,
    },
    {
        "id": stable_uuid("didier"),
        "email": "didier@test.kompetens.nc",
        "role": "recruteur",
        "zone": "Nouméa",
        "dispo": None,
        "resume": None,
    },
]

# Competences: (profile_owner_name, label, code_rome, niveau, source)
COMPETENCES = [
    # -- Céline (F1302 - Conduite d'engins) --
    ("celine", "Conduite d'engins lourds", "F1302", "confirmé", "voice"),
    ("celine", "Manoeuvre de chantier", "F1302", "confirmé", "voice"),
    ("celine", "Lecture de plan simple", "F1302", "débutant", "inferred"),
    # -- Steeve (F1402 - Extraction solide) --
    ("steeve", "Forage et extraction", "F1402", "expert", "voice"),
    ("steeve", "Maintenance d'engins miniers", "I1603", "confirmé", "voice"),
    ("steeve", "Soudure basique", "H2913", "intermédiaire", "manual"),
    ("steeve", "Conduite de tombereaux", "F1302", "confirmé", "voice"),
    # -- Marie (K1304 - Services domestiques) --
    ("marie", "Nettoyage et entretien", "K1304", "confirmé", "voice"),
    ("marie", "Repassage", "K1304", "confirmé", "voice"),
    ("marie", "Préparation de repas", "K1304", "intermédiaire", "voice"),
    # -- Jean (A1101 - Cultures spécialisées) --
    ("jean", "Culture maraîchère", "A1101", "expert", "voice"),
    ("jean", "Taille et entretien végétal", "A1101", "confirmé", "voice"),
    ("jean", "Récolte manuelle", "A1101", "expert", "voice"),
    ("jean", "Conduite de tracteur", "A1101", "confirmé", "voice"),
    ("jean", "Irrigation et arrosage", "A1101", "intermédiaire", "inferred"),
    # -- Paul (G1802 - Service en restauration) --
    ("paul", "Service en salle", "G1802", "confirmé", "voice"),
    ("paul", "Encaissement", "G1802", "confirmé", "voice"),
    ("paul", "Relation client", "G1802", "intermédiaire", "voice"),
    # -- Léa (D1106 - Vente en alimentation) --
    ("lea", "Vente et conseil client", "D1106", "confirmé", "voice"),
    ("lea", "Mise en rayon", "D1106", "confirmé", "manual"),
    ("lea", "Encaissement", "D1106", "confirmé", "voice"),
    # -- Thomas (F1501 - Montage de structures) --
    ("thomas", "Lecture de plan de charpente", "F1501", "confirmé", "voice"),
    ("thomas", "Assemblage bois", "F1501", "expert", "voice"),
    ("thomas", "Pose de charpente", "F1501", "confirmé", "voice"),
    ("thomas", "Utilisation d'outils électroportatifs", "F1501", "confirmé", "inferred"),
    # -- Sophie (A1405 - Pêche) --
    ("sophie", "Pêche côtière", "A1405", "confirmé", "voice"),
    ("sophie", "Maniement de filets", "A1405", "confirmé", "voice"),
    ("sophie", "Navigation côtière", "A1405", "intermédiaire", "voice"),
]

# Experiences: (profile_owner_name, intitule, contexte, duree_estimee)
EXPERIENCES = [
    # -- Céline --
    (
        "celine",
        "Conductrice de tombereau",
        "Chantier de terrassement SLN, site de Dumbéa. "
        "Transport de matériaux sur piste non goudronnée.",
        "4 ans",
    ),
    (
        "celine",
        "Aide sur chantier BTP",
        "Petits chantiers de construction résidentielle, manutention et aide aux engins.",
        "1 an",
    ),
    # -- Steeve --
    (
        "steeve",
        "Mineur - opérateur de forage",
        "Mine de nickel SLN Thio. Forage, extraction et maintenance de premier niveau.",
        "8 ans",
    ),
    (
        "steeve",
        "Soudeur polyvalent",
        "Atelier de réparation d'engins miniers, soudure MIG sur châssis et bennes.",
        "2 ans",
    ),
    # -- Marie --
    (
        "marie",
        "Aide ménagère à domicile",
        "Entretien de plusieurs maisons à Koné, ménage, repassage et préparation de repas.",
        "5 ans",
    ),
    # -- Jean --
    (
        "jean",
        "Exploitant maraîcher",
        "Exploitation familiale à Bourail, cultures de "
        "tomates, salades, concombres. Vente au marché.",
        "10 ans",
    ),
    (
        "jean",
        "Ouvrier agricole saisonnier",
        "Récolte de squash pour l'export au Japon, travail en équipe sur grande exploitation.",
        "3 saisons",
    ),
    (
        "jean",
        "Conducteur de tracteur",
        "Labour, semis et transport sur exploitation agricole. Entretien courant du matériel.",
        "5 ans",
    ),
    # -- Paul --
    (
        "paul",
        "Serveur en restauration rapide",
        "Fast-food à Nouméa centre, service au comptoir et en salle, encaissement, nettoyage.",
        "2 ans",
    ),
    (
        "paul",
        "Serveur en restaurant traditionnel",
        "Restaurant calédonien Baie des Citrons, service à l'assiette, carte des vins basique.",
        "1 an",
    ),
    # -- Léa --
    (
        "lea",
        "Vendeuse en prêt-à-porter",
        "Boutique de vêtements au centre commercial, conseil client, mise en rayon, caisse.",
        "3 ans",
    ),
    # -- Thomas --
    (
        "thomas",
        "Charpentier sur chantier neuf",
        "Construction de maisons individuelles en bois, "
        "lecture de plans, taille et pose de charpente.",
        "6 ans",
    ),
    (
        "thomas",
        "Aide charpentier",
        "Apprentissage sur chantier, découpe et assemblage de pièces de bois sous supervision.",
        "2 ans",
    ),
    # -- Sophie --
    (
        "sophie",
        "Pêcheuse artisanale",
        "Pêche côtière à Lifou, filets et lignes. Vente directe au marché communal.",
        "7 ans",
    ),
]


# ---------------------------------------------------------------------------
# Seed execution
# ---------------------------------------------------------------------------


def seed() -> None:
    """Insert seed data into the database. Idempotent."""
    print(f"Connecting to: {CONNINFO.split('@')[1] if '@' in CONNINFO else CONNINFO}")

    with psycopg.connect(CONNINFO) as conn:
        with conn.cursor() as cur:
            # Track profile UUIDs by user name for FK references
            profile_ids: dict[str, str] = {}

            # -- Users and Profiles --
            users_created = 0
            profiles_created = 0

            for u in USERS:
                # Insert user
                cur.execute(
                    """
                    INSERT INTO users (id, email, role, is_active)
                    VALUES (%s, %s, %s, true)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (u["id"], u["email"], u["role"]),
                )
                if cur.rowcount > 0:
                    users_created += 1

                # Extract name from email for profile_ids mapping
                name = u["email"].split("@")[0]

                # Insert profile (for all users, including aidant/recruteur)
                profile_id = stable_uuid(f"profile-{name}")
                profile_ids[name] = profile_id

                cur.execute(
                    """
                    INSERT INTO profiles (id, user_id, zone_geographique,
                                          disponibilite, resume_text)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        profile_id,
                        u["id"],
                        u["zone"],
                        u["dispo"],
                        u["resume"],
                    ),
                )
                if cur.rowcount > 0:
                    profiles_created += 1

            # -- Competences --
            competences_created = 0

            for owner, label, code_rome, niveau, source in COMPETENCES:
                comp_id = stable_uuid(f"comp-{owner}-{label}")
                cur.execute(
                    """
                    INSERT INTO competences (id, profile_id, label, code_rome,
                                             niveau, source)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        comp_id,
                        profile_ids[owner],
                        label,
                        code_rome,
                        niveau,
                        source,
                    ),
                )
                if cur.rowcount > 0:
                    competences_created += 1

            # -- Experiences --
            experiences_created = 0

            for owner, intitule, contexte, duree in EXPERIENCES:
                exp_id = stable_uuid(f"exp-{owner}-{intitule}")
                cur.execute(
                    """
                    INSERT INTO experiences (id, profile_id, intitule,
                                             contexte, duree_estimee)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        exp_id,
                        profile_ids[owner],
                        intitule,
                        contexte,
                        duree,
                    ),
                )
                if cur.rowcount > 0:
                    experiences_created += 1

        conn.commit()

    # -- Summary --
    print("\n--- Seed Summary ---")
    print(f"Users created:        {users_created}")
    print(f"Profiles created:     {profiles_created}")
    print(f"Competences created:  {competences_created}")
    print(f"Experiences created:  {experiences_created}")
    print("Done.")


if __name__ == "__main__":
    try:
        seed()
    except psycopg.OperationalError as exc:
        print(f"ERROR: Cannot connect to database: {exc}", file=sys.stderr)
        print(
            "Make sure PostgreSQL is running and DATABASE_URL_SYNC is set.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

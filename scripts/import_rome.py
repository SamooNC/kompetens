#!/usr/bin/env python3
"""Import ROME v4 taxonomy from France Travail open data into PostgreSQL.

Downloads the ROME bulk files (JSON) from the France Travail open data portal,
parses them, and upserts into the rome_metiers, rome_competences, and
rome_appellations tables.

Falls back to local files in data/rome/ if the API is unavailable.

Usage:
    python scripts/import_rome.py
    python scripts/import_rome.py --local data/rome/rome_export.zip
    python scripts/import_rome.py --dry-run

Reads DATABASE_URL_SYNC from environment or .env file.
"""

import argparse
import io
import json
import os
import sys
import zipfile
from pathlib import Path

import httpx
import psycopg

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# France Travail open data endpoints for ROME v4
# These are the bulk download endpoints (no OAuth needed)
ROME_BASE_URL = "https://api.francetravail.io/partenaire/rome/v1/fichemetier"
ROME_APPELLATION_URL = "https://api.francetravail.io/partenaire/rome/v1/appellation"

# Alternative: France Travail open data flat files
ROME_OPENDATA_METIERS_URL = (
    "https://www.data.gouv.fr/fr/datasets/r/8bf01cb5-b405-4f36-8e16-1395573a3a93"
)

# Local fallback paths
LOCAL_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "rome"

# .env loading (same logic as seed.py)
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
CONNINFO = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------


def download_rome_json(url: str, label: str) -> list[dict] | None:
    """Download a JSON array from the given URL, with error handling."""
    print(f"  Downloading {label} from {url} ...")
    try:
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()

            content_type = resp.headers.get("content-type", "")

            # Handle ZIP archives
            if "zip" in content_type or url.endswith(".zip"):
                return extract_json_from_zip(resp.content)

            # Handle direct JSON
            return resp.json()
    except httpx.HTTPStatusError as exc:
        print(f"  HTTP error {exc.response.status_code} fetching {label}")
        return None
    except httpx.ConnectError:
        print(f"  Connection error fetching {label} — API may be down")
        return None
    except Exception as exc:
        print(f"  Error fetching {label}: {exc}")
        return None


def extract_json_from_zip(content: bytes) -> list[dict] | None:
    """Extract the first JSON file from a ZIP archive."""
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            json_files = [n for n in zf.namelist() if n.endswith(".json")]
            if not json_files:
                print("  No JSON files found in ZIP archive")
                return None
            with zf.open(json_files[0]) as f:
                return json.load(f)
    except (zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"  Error extracting ZIP: {exc}")
        return None


def load_local_file(filename: str) -> list[dict] | None:
    """Load a JSON file from the local data/rome/ directory."""
    filepath = LOCAL_DATA_DIR / filename
    if not filepath.exists():
        return None
    print(f"  Loading local file: {filepath}")
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def fetch_rome_data(local_path: str | None = None) -> dict[str, list[dict]]:
    """Fetch ROME data from API or local files.

    Returns dict with keys: metiers, competences, appellations.
    Each value is a list of dicts ready for DB insertion.
    """
    result: dict[str, list[dict]] = {
        "metiers": [],
        "competences": [],
        "appellations": [],
    }

    # If user specified a local ZIP/JSON
    if local_path:
        path = Path(local_path)
        if path.suffix == ".zip":
            with open(path, "rb") as f:
                data = extract_json_from_zip(f.read())
            if data:
                result = parse_rome_bulk(data)
                return result
        elif path.suffix == ".json":
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                result = parse_rome_bulk(data)
                return result

    # Try API download
    print("Fetching ROME data from France Travail API...")
    metiers_raw = download_rome_json(ROME_BASE_URL, "fiches métier")

    if metiers_raw:
        for fiche in metiers_raw:
            code = fiche.get("code", fiche.get("codeRome", ""))
            libelle = fiche.get("libelle", fiche.get("intitule", ""))
            definition = fiche.get("definition", "")

            if code and libelle:
                result["metiers"].append({
                    "code_rome": code,
                    "libelle": libelle,
                    "definition": definition,
                })

            # Extract competences from fiche
            for comp_block in fiche.get("competencesDeBase", []):
                comp_code = comp_block.get("code", "")
                comp_libelle = comp_block.get("libelle", "")
                if comp_code and comp_libelle:
                    result["competences"].append({
                        "code": comp_code,
                        "libelle": comp_libelle,
                        "type_competence": "savoir-faire",
                    })

            for comp_block in fiche.get("competencesSpecifiques", []):
                comp_code = comp_block.get("code", "")
                comp_libelle = comp_block.get("libelle", "")
                if comp_code and comp_libelle:
                    result["competences"].append({
                        "code": comp_code,
                        "libelle": comp_libelle,
                        "type_competence": "savoir-faire",
                    })

            for savoir in fiche.get("savoirs", []):
                s_code = savoir.get("code", "")
                s_libelle = savoir.get("libelle", "")
                if s_code and s_libelle:
                    result["competences"].append({
                        "code": s_code,
                        "libelle": s_libelle,
                        "type_competence": "savoir",
                    })

            for savoir_etre in fiche.get("savoirEtre", []):
                se_code = savoir_etre.get("code", "")
                se_libelle = savoir_etre.get("libelle", "")
                if se_code and se_libelle:
                    result["competences"].append({
                        "code": se_code,
                        "libelle": se_libelle,
                        "type_competence": "savoir-être",
                    })

            # Extract appellations from fiche
            for appellation in fiche.get("appellations", []):
                app_code = appellation.get("code", "")
                app_libelle = appellation.get("libelle", "")
                if app_code and app_libelle and code:
                    result["appellations"].append({
                        "code": app_code,
                        "libelle": app_libelle,
                        "code_rome": code,
                    })

        return result

    # Fallback: try local files
    print("API unavailable, trying local files...")
    for filename in ["rome_metiers.json", "rome_fiches.json", "rome_export.json"]:
        data = load_local_file(filename)
        if data:
            result = parse_rome_bulk(data)
            if result["metiers"]:
                return result

    return result


def parse_rome_bulk(data: list[dict]) -> dict[str, list[dict]]:
    """Parse a bulk ROME JSON export into metiers, competences, appellations."""
    result: dict[str, list[dict]] = {
        "metiers": [],
        "competences": [],
        "appellations": [],
    }

    for item in data:
        code = item.get("code", item.get("codeRome", ""))
        libelle = item.get("libelle", item.get("intitule", ""))
        definition = item.get("definition", "")

        if code and libelle:
            result["metiers"].append({
                "code_rome": code,
                "libelle": libelle,
                "definition": definition,
            })

        # Nested competences
        for key, comp_type in [
            ("competencesDeBase", "savoir-faire"),
            ("competencesSpecifiques", "savoir-faire"),
            ("savoirs", "savoir"),
            ("savoirEtre", "savoir-être"),
        ]:
            for comp in item.get(key, []):
                c_code = comp.get("code", "")
                c_libelle = comp.get("libelle", "")
                if c_code and c_libelle:
                    result["competences"].append({
                        "code": c_code,
                        "libelle": c_libelle,
                        "type_competence": comp_type,
                    })

        # Nested appellations
        for appellation in item.get("appellations", []):
            app_code = appellation.get("code", "")
            app_libelle = appellation.get("libelle", "")
            if app_code and app_libelle and code:
                result["appellations"].append({
                    "code": app_code,
                    "libelle": app_libelle,
                    "code_rome": code,
                })

    return result


# ---------------------------------------------------------------------------
# Database upsert
# ---------------------------------------------------------------------------


def upsert_rome_data(data: dict[str, list[dict]], dry_run: bool = False) -> None:
    """Upsert ROME data into PostgreSQL tables."""
    metiers = data["metiers"]
    competences = data["competences"]
    appellations = data["appellations"]

    # Deduplicate by primary key
    metiers_map = {m["code_rome"]: m for m in metiers}
    competences_map = {c["code"]: c for c in competences}
    appellations_map = {a["code"]: a for a in appellations}

    metiers = list(metiers_map.values())
    competences = list(competences_map.values())
    appellations = list(appellations_map.values())

    print(f"\nData to upsert:")
    print(f"  Métiers:       {len(metiers)}")
    print(f"  Compétences:   {len(competences)}")
    print(f"  Appellations:  {len(appellations)}")

    if dry_run:
        print("\n[DRY RUN] No data written to database.")
        if metiers:
            print(f"\nSample métier: {metiers[0]}")
        if competences:
            print(f"Sample compétence: {competences[0]}")
        if appellations:
            print(f"Sample appellation: {appellations[0]}")
        return

    print(f"\nConnecting to: {CONNINFO.split('@')[1] if '@' in CONNINFO else CONNINFO}")

    with psycopg.connect(CONNINFO) as conn:
        with conn.cursor() as cur:
            # Upsert métiers
            metiers_count = 0
            for m in metiers:
                cur.execute(
                    """
                    INSERT INTO rome_metiers (code_rome, libelle, definition)
                    VALUES (%(code_rome)s, %(libelle)s, %(definition)s)
                    ON CONFLICT (code_rome) DO UPDATE SET
                        libelle = EXCLUDED.libelle,
                        definition = EXCLUDED.definition
                    """,
                    m,
                )
                metiers_count += 1

            # Upsert compétences
            competences_count = 0
            for c in competences:
                cur.execute(
                    """
                    INSERT INTO rome_competences (code, libelle, type_competence)
                    VALUES (%(code)s, %(libelle)s, %(type_competence)s)
                    ON CONFLICT (code) DO UPDATE SET
                        libelle = EXCLUDED.libelle,
                        type_competence = EXCLUDED.type_competence
                    """,
                    c,
                )
                competences_count += 1

            # Upsert appellations (only those with valid code_rome FK)
            appellations_count = 0
            appellations_skipped = 0
            valid_codes = {m["code_rome"] for m in metiers}

            for a in appellations:
                if a["code_rome"] not in valid_codes:
                    appellations_skipped += 1
                    continue
                cur.execute(
                    """
                    INSERT INTO rome_appellations (code, libelle, code_rome)
                    VALUES (%(code)s, %(libelle)s, %(code_rome)s)
                    ON CONFLICT (code) DO UPDATE SET
                        libelle = EXCLUDED.libelle,
                        code_rome = EXCLUDED.code_rome
                    """,
                    a,
                )
                appellations_count += 1

        conn.commit()

    print(f"\n--- Import Summary ---")
    print(f"Métiers upserted:       {metiers_count}")
    print(f"Compétences upserted:   {competences_count}")
    print(f"Appellations upserted:  {appellations_count}")
    if appellations_skipped:
        print(f"Appellations skipped:   {appellations_skipped} (missing code_rome FK)")
    print("Done.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import ROME v4 taxonomy from France Travail into PostgreSQL",
    )
    parser.add_argument(
        "--local",
        type=str,
        default=None,
        help="Path to a local ROME ZIP or JSON file (skips API download)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse data but do not write to database",
    )
    args = parser.parse_args()

    data = fetch_rome_data(local_path=args.local)

    if not data["metiers"]:
        print(
            "\nNo ROME data found. Either:\n"
            "  1. The France Travail API is unavailable\n"
            "  2. No local files in data/rome/\n"
            "\nTo use local files, download the ROME export and place it in data/rome/\n"
            "or use: python scripts/import_rome.py --local path/to/rome_export.json",
            file=sys.stderr,
        )
        sys.exit(1)

    upsert_rome_data(data, dry_run=args.dry_run)


if __name__ == "__main__":
    try:
        main()
    except psycopg.OperationalError as exc:
        print(f"ERROR: Cannot connect to database: {exc}", file=sys.stderr)
        print(
            "Make sure PostgreSQL is running and DATABASE_URL_SYNC is set.",
            file=sys.stderr,
        )
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)

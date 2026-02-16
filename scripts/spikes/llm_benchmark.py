"""
vLLM / Mistral LLM Benchmark Script for Kompetens
====================================================

Benchmarks the local vLLM instance (OpenAI-compatible API) for competence
extraction from simulated French voice transcriptions.

Measures:
- Time-to-first-token (TTFT)
- Total generation time
- Tokens per second
- Quality of competence extraction at different temperatures

Prerequisites:
    - vLLM running locally:
        python -m vllm.entrypoints.openai.api_server \\
            --model mistralai/Mistral-7B-Instruct-v0.3 --port 8001
    - pip install openai tabulate

Usage:
    python scripts/spikes/llm_benchmark.py
    python scripts/spikes/llm_benchmark.py --base-url http://gpu-server:8001/v1
    python scripts/spikes/llm_benchmark.py --model mistralai/Mixtral-8x7B-Instruct-v0.1
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Graceful imports
# ---------------------------------------------------------------------------
try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Test data
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "Tu es un assistant specialise dans l'extraction de competences professionnelles. "
    "A partir de la transcription vocale d'un candidat, extrais les competences sous forme "
    "de liste JSON avec les champs: label, code_rome (si identifiable), niveau_estime."
)

TEST_TRANSCRIPTIONS: list[dict[str, str]] = [
    {
        "id": "T1",
        "persona": "Celine (conductrice engins)",
        "text": (
            "Moi je conduis les gros camions sur les chantiers depuis cinq ans, "
            "les dumpers tout ca, et aussi les pelleteuses."
        ),
    },
    {
        "id": "T2",
        "persona": "Steeve (ex-mine)",
        "text": (
            "J'ai travaille trois ans dans la mine a Thio, je faisais le forage "
            "et l'extraction du minerai."
        ),
    },
    {
        "id": "T3",
        "persona": "Agent entretien",
        "text": (
            "Je fais le menage dans les bureaux et les maisons, ca fait dix ans "
            "que je fais ca a Noumea."
        ),
    },
    {
        "id": "T4",
        "persona": "Serveur restaurant",
        "text": (
            "Je suis serveur au restaurant depuis deux ans, je m'occupe de la salle "
            "et de l'encaissement."
        ),
    },
    {
        "id": "T5",
        "persona": "Agriculteur Bourail",
        "text": (
            "J'ai ma propre exploitation agricole a Bourail, je fais du maraichage "
            "et de l'elevage de betail."
        ),
    },
]


# ---------------------------------------------------------------------------
# Benchmark logic
# ---------------------------------------------------------------------------

def call_llm_streaming(
    client: "openai.OpenAI",
    model: str,
    transcription: str,
    temperature: float,
) -> dict:
    """Send a prompt to vLLM and measure timing via streaming."""
    user_message = (
        f"Voici la transcription vocale d'un candidat :\n\n"
        f"\"{transcription}\"\n\n"
        f"Extrais les competences au format JSON."
    )

    t_start = time.perf_counter()
    ttft: Optional[float] = None
    full_response = ""
    completion_tokens = 0

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
            max_tokens=1024,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                if ttft is None:
                    ttft = time.perf_counter() - t_start
                content = chunk.choices[0].delta.content
                full_response += content
                completion_tokens += 1  # approximation per-chunk

        t_end = time.perf_counter()

    except Exception as exc:
        return {
            "error": str(exc),
            "ttft_s": None,
            "total_time_s": None,
            "tokens_per_s": None,
            "response": None,
        }

    total_time = t_end - t_start
    tokens_per_s = completion_tokens / total_time if total_time > 0 else 0.0

    return {
        "error": None,
        "ttft_s": round(ttft, 4) if ttft is not None else None,
        "total_time_s": round(total_time, 3),
        "tokens_per_s": round(tokens_per_s, 1),
        "completion_tokens": completion_tokens,
        "response": full_response,
    }


def call_llm_non_streaming(
    client: "openai.OpenAI",
    model: str,
    transcription: str,
    temperature: float,
) -> dict:
    """Non-streaming fallback for TTFT estimation."""
    user_message = (
        f"Voici la transcription vocale d'un candidat :\n\n"
        f"\"{transcription}\"\n\n"
        f"Extrais les competences au format JSON."
    )

    t_start = time.perf_counter()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
            max_tokens=1024,
            stream=False,
        )
        t_end = time.perf_counter()

        total_time = t_end - t_start
        content = response.choices[0].message.content or ""
        usage = response.usage
        completion_tokens = usage.completion_tokens if usage else len(content.split())
        tokens_per_s = completion_tokens / total_time if total_time > 0 else 0.0

        return {
            "error": None,
            "ttft_s": None,
            "total_time_s": round(total_time, 3),
            "tokens_per_s": round(tokens_per_s, 1),
            "completion_tokens": completion_tokens,
            "response": content,
        }

    except Exception as exc:
        return {
            "error": str(exc),
            "ttft_s": None,
            "total_time_s": None,
            "tokens_per_s": None,
            "response": None,
        }


def run_benchmarks(
    client: "openai.OpenAI",
    model: str,
    temperatures: list[float],
) -> list[dict]:
    """Run all transcription x temperature combinations."""
    results: list[dict] = []

    for temp in temperatures:
        for tx in TEST_TRANSCRIPTIONS:
            logger.info(
                "  [temp=%.1f] %s: %s ...",
                temp,
                tx["id"],
                tx["text"][:50],
            )

            # Try streaming first (for TTFT)
            result = call_llm_streaming(client, model, tx["text"], temp)

            if result["error"] is not None:
                logger.warning("Streaming failed, trying non-streaming: %s", result["error"])
                result = call_llm_non_streaming(client, model, tx["text"], temp)

            results.append(
                {
                    "id": tx["id"],
                    "persona": tx["persona"],
                    "temperature": temp,
                    "ttft_s": result["ttft_s"],
                    "total_time_s": result["total_time_s"],
                    "tokens_per_s": result["tokens_per_s"],
                    "completion_tokens": result.get("completion_tokens"),
                    "error": result["error"],
                    "response_preview": (
                        result["response"][:200] if result["response"] else "N/A"
                    ),
                }
            )

    return results


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    results: list[dict],
    model: str,
    base_url: str,
    output_dir: Path,
) -> str:
    """Build a markdown report and save it."""
    today = datetime.now().strftime("%Y%m%d")
    report_path = output_dir / f"llm_benchmark_{today}.md"

    lines: list[str] = []
    lines.append("# vLLM / Mistral Competence Extraction Benchmark")
    lines.append("")
    lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Model**: `{model}`")
    lines.append(f"**Endpoint**: `{base_url}`")
    lines.append(f"**Transcriptions tested**: {len(TEST_TRANSCRIPTIONS)}")
    lines.append("")

    # Performance table
    headers = [
        "ID",
        "Persona",
        "Temp",
        "TTFT (s)",
        "Total (s)",
        "Tok/s",
        "Tokens",
        "Error",
    ]
    table_rows = [
        [
            r["id"],
            r["persona"],
            r["temperature"],
            r["ttft_s"] if r["ttft_s"] is not None else "N/A",
            r["total_time_s"] if r["total_time_s"] is not None else "N/A",
            r["tokens_per_s"] if r["tokens_per_s"] is not None else "N/A",
            r["completion_tokens"] if r["completion_tokens"] is not None else "N/A",
            r["error"] if r["error"] else "-",
        ]
        for r in results
    ]

    if tabulate is not None:
        table_str = tabulate(table_rows, headers=headers, tablefmt="github")
    else:
        table_str = "| " + " | ".join(headers) + " |\n"
        table_str += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        for row in table_rows:
            table_str += "| " + " | ".join(str(c) for c in row) + " |\n"

    lines.append("## Performance Results")
    lines.append("")
    lines.append(table_str)
    lines.append("")

    # Extraction quality samples
    lines.append("## Extraction Quality Samples")
    lines.append("")
    for r in results:
        lines.append(f"### {r['id']} - {r['persona']} (temp={r['temperature']})")
        lines.append("")
        lines.append("```json")
        lines.append(r["response_preview"])
        lines.append("```")
        lines.append("")

    # Summary
    successful = [r for r in results if r["error"] is None]
    if successful:
        ttfts = [r["ttft_s"] for r in successful if r["ttft_s"] is not None]
        totals = [r["total_time_s"] for r in successful if r["total_time_s"] is not None]
        tps = [r["tokens_per_s"] for r in successful if r["tokens_per_s"] is not None]

        lines.append("## Summary")
        lines.append("")
        if ttfts:
            lines.append(f"- **Mean TTFT**: {round(sum(ttfts) / len(ttfts), 3)}s")
            lines.append(f"- **Best TTFT**: {min(ttfts)}s")
        if totals:
            lines.append(f"- **Mean total generation**: {round(sum(totals) / len(totals), 3)}s")
        if tps:
            lines.append(f"- **Mean tokens/s**: {round(sum(tps) / len(tps), 1)}")
        lines.append(f"- **Successful runs**: {len(successful)}/{len(results)}")
        lines.append("")

    lines.append("## Kompetens Constraints Check")
    lines.append("")
    lines.append("- [ ] TTFT < 2s (acceptable for voice-first UX)")
    lines.append("- [ ] Total generation < 10s (user patience threshold)")
    lines.append("- [ ] JSON extraction is parseable")
    lines.append("- [ ] ROME codes are plausible")
    lines.append("")

    report_content = "\n".join(lines)

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_content, encoding="utf-8")
    logger.info("Report saved to %s", report_path)

    return report_content


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark vLLM competence extraction for Kompetens"
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8001/v1",
        help="vLLM OpenAI-compatible API base URL (default: http://localhost:8001/v1)",
    )
    parser.add_argument(
        "--model",
        default="mistralai/Mistral-7B-Instruct-v0.3",
        help="Model name as served by vLLM (default: mistralai/Mistral-7B-Instruct-v0.3)",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/spikes/",
        help="Directory for the benchmark report (default: docs/spikes/)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not OPENAI_AVAILABLE:
        logger.error(
            "The 'openai' package is not installed.\n"
            "Install it with:\n"
            "  pip install openai>=1.50.0\n"
            "Or install all spike dependencies:\n"
            "  pip install -r scripts/spikes/requirements-spikes.txt"
        )
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create OpenAI client pointing at vLLM
    client = openai.OpenAI(
        base_url=args.base_url,
        api_key="not-needed",  # vLLM does not require an API key by default
    )

    # Check connectivity
    logger.info("Testing connection to %s ...", args.base_url)
    try:
        models = client.models.list()
        available_models = [m.id for m in models.data]
        logger.info("Available models: %s", available_models)
        if args.model not in available_models:
            logger.warning(
                "Requested model '%s' not in available models %s. "
                "The request may fail or use a different model.",
                args.model,
                available_models,
            )
    except Exception as exc:
        logger.error(
            "Cannot connect to vLLM at %s: %s\n\n"
            "Make sure vLLM is running:\n"
            "  python -m vllm.entrypoints.openai.api_server \\\n"
            "      --model %s --port 8001\n",
            args.base_url,
            exc,
            args.model,
        )
        sys.exit(1)

    # Run benchmarks
    temperatures = [0.0, 0.3]
    logger.info(
        "Starting benchmark: %d transcriptions x %d temperatures = %d runs",
        len(TEST_TRANSCRIPTIONS),
        len(temperatures),
        len(TEST_TRANSCRIPTIONS) * len(temperatures),
    )

    results = run_benchmarks(client, args.model, temperatures)

    # Generate report
    report = generate_report(results, args.model, args.base_url, output_dir)
    print("\n" + report)


if __name__ == "__main__":
    main()

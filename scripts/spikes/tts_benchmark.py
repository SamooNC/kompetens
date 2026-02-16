"""
Piper TTS Benchmark Script for Kompetens
==========================================

Benchmarks Piper TTS for text-to-speech synthesis performance, targeting
the voice-first UX on the NC sovereign server.

Measures:
- Synthesis time per text input
- Audio duration of generated speech
- Real-time factor (RTF = synthesis_time / audio_duration)
- Output quality via generated WAV samples

Prerequisites:
    pip install piper-tts>=1.2.0
    Download a French Piper model (ONNX + JSON config):
        https://github.com/rhasspy/piper/blob/master/VOICES.md

Usage:
    python scripts/spikes/tts_benchmark.py
    python scripts/spikes/tts_benchmark.py --model-path models/fr_FR-siwis-medium.onnx
"""

import argparse
import logging
import struct
import sys
import time
import wave
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
    from piper import PiperVoice

    PIPER_AVAILABLE = True
except ImportError:
    PIPER_AVAILABLE = False

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

TEST_TEXTS: list[dict[str, str]] = [
    {
        "id": "short",
        "label": "Greeting (short)",
        "text": "Bonjour, bienvenue.",
    },
    {
        "id": "sentence",
        "label": "Confirmation (sentence)",
        "text": (
            "Vos competences en conduite d'engins ont bien ete enregistrees."
        ),
    },
    {
        "id": "paragraph",
        "label": "Summary (paragraph)",
        "text": (
            "Merci pour votre inventaire vocal. Nous avons identifie cinq "
            "competences principales liees au secteur du batiment et des "
            "travaux publics. Vous pouvez maintenant consulter votre profil "
            "ou ajouter des experiences supplementaires."
        ),
    },
]


# ---------------------------------------------------------------------------
# Benchmark logic
# ---------------------------------------------------------------------------

def get_wav_duration(wav_path: str) -> float:
    """Return WAV file duration in seconds."""
    with wave.open(wav_path, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / rate if rate > 0 else 0.0


def synthesize_to_wav(
    voice: "PiperVoice",
    text: str,
    wav_path: Path,
    sample_rate: int,
) -> tuple[float, float]:
    """
    Synthesize text to WAV and return (synthesis_time_s, audio_duration_s).
    """
    t_start = time.perf_counter()

    # Piper synthesizes audio as raw PCM int16 samples
    audio_segments: list[bytes] = []
    for audio_bytes in voice.synthesize_stream_raw(text):
        audio_segments.append(audio_bytes)

    t_end = time.perf_counter()
    synthesis_time = t_end - t_start

    # Write WAV
    raw_audio = b"".join(audio_segments)
    num_samples = len(raw_audio) // 2  # int16 = 2 bytes per sample
    audio_duration = num_samples / sample_rate if sample_rate > 0 else 0.0

    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(raw_audio)

    return synthesis_time, audio_duration


def synthesize_to_wav_non_streaming(
    voice: "PiperVoice",
    text: str,
    wav_path: Path,
    sample_rate: int,
) -> tuple[float, float]:
    """
    Fallback synthesis using the non-streaming synthesize method.
    """
    t_start = time.perf_counter()

    with wave.open(str(wav_path), "wb") as wf:
        voice.synthesize(text, wf)

    t_end = time.perf_counter()
    synthesis_time = t_end - t_start

    audio_duration = get_wav_duration(str(wav_path))

    return synthesis_time, audio_duration


def run_benchmarks(
    voice: "PiperVoice",
    sample_rate: int,
    output_dir: Path,
) -> list[dict]:
    """Run TTS benchmark on all test texts."""
    wav_dir = output_dir / "tts_samples"
    wav_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []

    for tx in TEST_TEXTS:
        wav_path = wav_dir / f"tts_{tx['id']}.wav"
        logger.info("  Synthesizing '%s' ...", tx["label"])

        try:
            synthesis_time, audio_duration = synthesize_to_wav(
                voice, tx["text"], wav_path, sample_rate
            )
        except Exception as exc:
            logger.warning(
                "Streaming synthesis failed (%s), trying non-streaming ...", exc
            )
            try:
                synthesis_time, audio_duration = synthesize_to_wav_non_streaming(
                    voice, tx["text"], wav_path, sample_rate
                )
            except Exception as exc2:
                logger.error("Synthesis failed entirely: %s", exc2)
                results.append(
                    {
                        "id": tx["id"],
                        "label": tx["label"],
                        "text_length": len(tx["text"]),
                        "synthesis_time_s": None,
                        "audio_duration_s": None,
                        "rtf": None,
                        "wav_path": None,
                        "error": str(exc2),
                    }
                )
                continue

        rtf = synthesis_time / audio_duration if audio_duration > 0 else float("inf")

        logger.info(
            "    -> synthesis=%.3fs, audio=%.2fs, RTF=%.4f, saved to %s",
            synthesis_time,
            audio_duration,
            rtf,
            wav_path,
        )

        results.append(
            {
                "id": tx["id"],
                "label": tx["label"],
                "text_length": len(tx["text"]),
                "synthesis_time_s": round(synthesis_time, 4),
                "audio_duration_s": round(audio_duration, 2),
                "rtf": round(rtf, 4),
                "wav_path": str(wav_path),
                "error": None,
            }
        )

    return results


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    results: list[dict],
    model_path: Optional[str],
    sample_rate: int,
    output_dir: Path,
) -> str:
    """Build a markdown report and save it."""
    today = datetime.now().strftime("%Y%m%d")
    report_path = output_dir / f"tts_benchmark_{today}.md"

    lines: list[str] = []
    lines.append("# Piper TTS Benchmark Report")
    lines.append("")
    lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Model**: {model_path or 'default'}")
    lines.append(f"**Sample rate**: {sample_rate} Hz")
    lines.append("")

    # Results table
    headers = [
        "ID",
        "Label",
        "Text len",
        "Synthesis (s)",
        "Audio (s)",
        "RTF",
        "Error",
    ]
    table_rows = [
        [
            r["id"],
            r["label"],
            r["text_length"],
            r["synthesis_time_s"] if r["synthesis_time_s"] is not None else "N/A",
            r["audio_duration_s"] if r["audio_duration_s"] is not None else "N/A",
            r["rtf"] if r["rtf"] is not None else "N/A",
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

    lines.append("## Results")
    lines.append("")
    lines.append(table_str)
    lines.append("")

    # Generated samples list
    lines.append("## Generated WAV Samples")
    lines.append("")
    for r in results:
        if r["wav_path"]:
            lines.append(f"- **{r['label']}**: `{r['wav_path']}`")
    lines.append("")

    # Summary
    successful = [r for r in results if r["error"] is None]
    if successful:
        rtfs = [r["rtf"] for r in successful if r["rtf"] is not None]
        synth_times = [r["synthesis_time_s"] for r in successful if r["synthesis_time_s"] is not None]

        lines.append("## Summary")
        lines.append("")
        if rtfs:
            lines.append(f"- **Best RTF**: {min(rtfs)} (lower = faster than real-time)")
            lines.append(f"- **Worst RTF**: {max(rtfs)}")
            lines.append(f"- **Mean RTF**: {round(sum(rtfs) / len(rtfs), 4)}")
        if synth_times:
            lines.append(f"- **Mean synthesis time**: {round(sum(synth_times) / len(synth_times), 4)}s")
        lines.append(f"- **Successful**: {len(successful)}/{len(results)}")
        lines.append("")

    lines.append("## Kompetens UX Constraints")
    lines.append("")
    lines.append("- [ ] RTF < 0.5 (speech should be generated well faster than real-time)")
    lines.append("- [ ] Paragraph synthesis < 3s (user patience on 3G)")
    lines.append("- [ ] Audio quality subjectively acceptable for phone speaker")
    lines.append("- [ ] French pronunciation correct for NC context")
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
        description="Benchmark Piper TTS for Kompetens voice-first UX"
    )
    parser.add_argument(
        "--model-path",
        default=None,
        help=(
            "Path to Piper ONNX model file. If not specified, "
            "Piper will try to use a default model."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="docs/spikes/",
        help="Directory for the benchmark report and WAV samples (default: docs/spikes/)",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=22050,
        help="Audio sample rate in Hz (default: 22050)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not PIPER_AVAILABLE:
        logger.error(
            "Piper TTS is not installed.\n\n"
            "Install it with:\n"
            "  pip install piper-tts>=1.2.0\n\n"
            "Or install all spike dependencies:\n"
            "  pip install -r scripts/spikes/requirements-spikes.txt\n\n"
            "You also need a French voice model. Download from:\n"
            "  https://github.com/rhasspy/piper/blob/master/VOICES.md\n\n"
            "Example:\n"
            "  wget https://huggingface.co/rhasspy/piper-voices/resolve/main/"
            "fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx\n"
            "  wget https://huggingface.co/rhasspy/piper-voices/resolve/main/"
            "fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json\n\n"
            "Then run:\n"
            "  python scripts/spikes/tts_benchmark.py "
            "--model-path fr_FR-siwis-medium.onnx"
        )
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load Piper voice model
    if args.model_path:
        model_path = Path(args.model_path)
        if not model_path.exists():
            logger.error("Model file not found: %s", model_path)
            sys.exit(1)
        logger.info("Loading Piper model from %s ...", model_path)
        voice = PiperVoice.load(str(model_path))
    else:
        logger.error(
            "No --model-path specified.\n\n"
            "Piper requires an ONNX voice model. Download a French model:\n"
            "  https://github.com/rhasspy/piper/blob/master/VOICES.md\n\n"
            "Then run:\n"
            "  python scripts/spikes/tts_benchmark.py "
            "--model-path path/to/fr_FR-siwis-medium.onnx"
        )
        sys.exit(1)

    logger.info("Model loaded. Running TTS benchmark ...")

    # Run benchmarks
    results = run_benchmarks(voice, args.sample_rate, output_dir)

    # Generate report
    report = generate_report(results, args.model_path, args.sample_rate, output_dir)
    print("\n" + report)


if __name__ == "__main__":
    main()

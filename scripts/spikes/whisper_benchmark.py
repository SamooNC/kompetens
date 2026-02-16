"""
Whisper STT Benchmark Script for Kompetens
===========================================

Benchmarks faster-whisper (CTranslate2-based Whisper) for speech-to-text
performance on the NC sovereign server (NVIDIA H100 target).

Measures:
- Model load time
- Transcription time per audio file
- Real-time factor (RTF = transcription_time / audio_duration)
- Impact of beam size and VAD filter settings

Usage:
    python scripts/spikes/whisper_benchmark.py
    python scripts/spikes/whisper_benchmark.py --audio-dir data/test_audio/
    python scripts/spikes/whisper_benchmark.py --model-size large-v3 --device cuda
"""

import argparse
import logging
import math
import struct
import sys
import time
import wave
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Graceful import of faster_whisper
# ---------------------------------------------------------------------------
try:
    from faster_whisper import WhisperModel

    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Synthetic audio generation (numpy-free fallback using struct + math)
# ---------------------------------------------------------------------------


def _generate_sine_wav(path: Path, duration_s: float, sample_rate: int = 16000) -> None:
    """Generate a WAV file with a sine wave + white noise using only stdlib."""
    import random

    num_samples = int(sample_rate * duration_s)
    freq = 440.0  # Hz
    amplitude = 16000
    noise_amplitude = 2000

    random.seed(42)

    samples: list[int] = []
    for i in range(num_samples):
        t = i / sample_rate
        value = amplitude * math.sin(2.0 * math.pi * freq * t)
        noise = random.randint(-noise_amplitude, noise_amplitude)
        sample = max(-32768, min(32767, int(value + noise)))
        samples.append(sample)

    raw = struct.pack(f"<{num_samples}h", *samples)

    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(raw)


def _try_numpy_sine_wav(path: Path, duration_s: float, sample_rate: int = 16000) -> bool:
    """Try generating via numpy (much faster for long durations). Returns True on success."""
    try:
        import numpy as np

        t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)
        freq = 440.0
        signal = (16000 * np.sin(2 * np.pi * freq * t)).astype(np.int16)
        rng = np.random.default_rng(42)
        noise = rng.integers(-2000, 2000, size=signal.shape, dtype=np.int16)
        combined = np.clip(signal.astype(np.int32) + noise.astype(np.int32), -32768, 32767).astype(
            np.int16
        )
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(combined.tobytes())
        return True
    except ImportError:
        return False


def generate_synthetic_audio(output_dir: Path) -> list[dict]:
    """Generate synthetic WAV files at various durations and return metadata."""
    durations = [10, 30, 60, 120]
    audio_dir = output_dir / "synthetic_audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    files: list[dict] = []
    for dur in durations:
        wav_path = audio_dir / f"synthetic_{dur}s.wav"
        if wav_path.exists():
            logger.info("Synthetic audio already exists: %s", wav_path)
        else:
            logger.info("Generating %ds synthetic audio ...", dur)
            if not _try_numpy_sine_wav(wav_path, dur):
                logger.info("numpy not available, falling back to stdlib (slower for long files)")
                _generate_sine_wav(wav_path, dur)
        files.append({"path": str(wav_path), "duration_s": dur, "label": f"synthetic_{dur}s"})
    return files


def get_audio_duration(path: str) -> float:
    """Return WAV duration in seconds."""
    with wave.open(path, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / rate


def collect_audio_files(audio_dir: str) -> list[dict]:
    """Scan a directory for WAV files and return metadata."""
    files: list[dict] = []
    for entry in sorted(Path(audio_dir).iterdir()):
        if entry.suffix.lower() == ".wav":
            dur = get_audio_duration(str(entry))
            files.append({"path": str(entry), "duration_s": dur, "label": entry.stem})
    return files


# ---------------------------------------------------------------------------
# Benchmark logic
# ---------------------------------------------------------------------------


def benchmark_whisper(
    model_size: str,
    device: str,
    compute_type: str,
    audio_files: list[dict],
    beam_sizes: list[int],
    vad_options: list[bool],
) -> list[dict]:
    """Run benchmarks across configurations and return rows of results."""
    # --- Model load ---
    logger.info("Loading model '%s' on %s (%s) ...", model_size, device, compute_type)
    t0 = time.perf_counter()
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
    except Exception as exc:
        if device == "cuda":
            logger.warning("CUDA not available (%s). Falling back to CPU with int8.", exc)
            device = "cpu"
            compute_type = "int8"
            t0 = time.perf_counter()
            model = WhisperModel(model_size, device=device, compute_type=compute_type)
        else:
            raise
    load_time = time.perf_counter() - t0
    logger.info("Model loaded in %.2fs (device=%s, compute=%s)", load_time, device, compute_type)

    results: list[dict] = []

    for af in audio_files:
        for beam in beam_sizes:
            for vad in vad_options:
                label = af["label"]
                duration = af["duration_s"]
                vad_label = "on" if vad else "off"
                logger.info("  Transcribing %s | beam=%d | VAD=%s ...", label, beam, vad_label)

                vad_filter = vad
                t_start = time.perf_counter()
                segments, info = model.transcribe(
                    af["path"],
                    beam_size=beam,
                    language="fr",
                    vad_filter=vad_filter,
                )
                # Drain the generator to capture full transcription time
                text_parts: list[str] = []
                for seg in segments:
                    text_parts.append(seg.text)
                t_end = time.perf_counter()

                transcription_time = t_end - t_start
                rtf = transcription_time / duration if duration > 0 else float("inf")
                transcript_preview = " ".join(text_parts)[:120]

                results.append(
                    {
                        "audio": label,
                        "duration_s": round(duration, 1),
                        "beam_size": beam,
                        "vad": vad_label,
                        "transcription_time_s": round(transcription_time, 3),
                        "rtf": round(rtf, 4),
                        "language_prob": round(info.language_probability, 3),
                        "transcript_preview": transcript_preview,
                    }
                )

    # Prepend model info row
    meta = {
        "model": model_size,
        "device": device,
        "compute_type": compute_type,
        "load_time_s": round(load_time, 3),
    }
    return results, meta  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def generate_report(
    results: list[dict],
    meta: dict,
    output_dir: Path,
) -> str:
    """Build a markdown report and save it."""
    today = datetime.now().strftime("%Y%m%d")
    report_path = output_dir / f"whisper_benchmark_{today}.md"

    lines: list[str] = []
    lines.append("# Whisper STT Benchmark Report")
    lines.append("")
    lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Model**: {meta['model']}")
    lines.append(f"**Device**: {meta['device']} ({meta['compute_type']})")
    lines.append(f"**Model load time**: {meta['load_time_s']}s")
    lines.append("")

    # Results table
    headers = [
        "Audio",
        "Duration (s)",
        "Beam",
        "VAD",
        "Transcription (s)",
        "RTF",
        "Lang prob",
    ]
    table_rows = [
        [
            r["audio"],
            r["duration_s"],
            r["beam_size"],
            r["vad"],
            r["transcription_time_s"],
            r["rtf"],
            r["language_prob"],
        ]
        for r in results
    ]

    if tabulate is not None:
        table_str = tabulate(table_rows, headers=headers, tablefmt="github")
    else:
        # Manual markdown table fallback
        table_str = "| " + " | ".join(headers) + " |\n"
        table_str += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        for row in table_rows:
            table_str += "| " + " | ".join(str(c) for c in row) + " |\n"

    lines.append("## Results")
    lines.append("")
    lines.append(table_str)
    lines.append("")

    # Summary
    if results:
        rtfs = [r["rtf"] for r in results]
        lines.append("## Summary")
        lines.append("")
        lines.append(
            f"- **Best RTF**: {min(rtfs)} (lower is better; < 1.0 = faster than real-time)"
        )
        lines.append(f"- **Worst RTF**: {max(rtfs)}")
        lines.append(f"- **Mean RTF**: {round(sum(rtfs) / len(rtfs), 4)}")
        lines.append(f"- **Total configurations tested**: {len(results)}")
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- **RTF < 1.0**: Transcription faster than real-time (good for production)")
    lines.append("- **RTF > 1.0**: Slower than real-time (may need smaller model or GPU upgrade)")
    lines.append("- **VAD filter**: Reduces silence processing, usually improves RTF")
    lines.append("- **Beam size 1**: Fastest but lower quality; beam 5: best quality, slower")
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
        description="Benchmark faster-whisper STT for Kompetens sovereign deployment"
    )
    parser.add_argument(
        "--model-size",
        default="large-v3",
        help="Whisper model size (default: large-v3)",
    )
    parser.add_argument(
        "--device",
        default="cuda",
        choices=["cuda", "cpu"],
        help="Compute device (default: cuda, auto-fallback to cpu)",
    )
    parser.add_argument(
        "--compute-type",
        default="float16",
        help="CTranslate2 compute type (default: float16)",
    )
    parser.add_argument(
        "--audio-dir",
        default=None,
        help="Directory with WAV test files. If omitted, synthetic audio is generated.",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/spikes/",
        help="Directory for the benchmark report (default: docs/spikes/)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not FASTER_WHISPER_AVAILABLE:
        logger.error(
            "faster-whisper is not installed.\n"
            "Install it with:\n"
            "  pip install faster-whisper>=1.0.0\n"
            "Or install all spike dependencies:\n"
            "  pip install -r scripts/spikes/requirements-spikes.txt"
        )
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect or generate audio
    if args.audio_dir:
        logger.info("Scanning audio directory: %s", args.audio_dir)
        audio_files = collect_audio_files(args.audio_dir)
        if not audio_files:
            logger.error("No .wav files found in %s", args.audio_dir)
            sys.exit(1)
        logger.info("Found %d audio files", len(audio_files))
    else:
        logger.info("No --audio-dir provided. Generating synthetic test audio ...")
        audio_files = generate_synthetic_audio(output_dir)

    # Benchmark configurations
    beam_sizes = [1, 3, 5]
    vad_options = [False, True]

    logger.info(
        "Starting benchmark: %d files x %d beam sizes x %d VAD options = %d runs",
        len(audio_files),
        len(beam_sizes),
        len(vad_options),
        len(audio_files) * len(beam_sizes) * len(vad_options),
    )

    results, meta = benchmark_whisper(
        model_size=args.model_size,
        device=args.device,
        compute_type=args.compute_type,
        audio_files=audio_files,
        beam_sizes=beam_sizes,
        vad_options=vad_options,
    )

    report = generate_report(results, meta, output_dir)
    print("\n" + report)


if __name__ == "__main__":
    main()

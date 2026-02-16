import { useCallback } from "react";
import VocalButton from "../components/VocalButton";
import { useAppStore } from "../stores/appStore";

/** Total number of steps in the vocal inventory flow. */
const TOTAL_STEPS = 5;

/**
 * Vocal inventory page — guided step-by-step competence extraction.
 *
 * Currently a scaffold with a single hardcoded step.  The step
 * labels and progress will later be driven by the backend
 * conversation engine (Sprint S2).
 */
function InventairePage() {
  const setListening = useAppStore((s) => s.setListening);

  const currentStep = 1; // Placeholder — will come from backend state

  const handleStart = useCallback(() => {
    setListening(true);
  }, [setListening]);

  const handleStop = useCallback(() => {
    setListening(false);
  }, [setListening]);

  /** Progress as a percentage (0-100). */
  const progress = Math.round((currentStep / TOTAL_STEPS) * 100);

  return (
    <div className="mx-auto flex max-w-lg flex-col items-center gap-6">
      {/* Step indicator */}
      <p className="text-lg font-semibold text-slate-700">
        Étape {currentStep} / {TOTAL_STEPS}
      </p>

      {/* Progress bar */}
      <div
        className="h-3 w-full overflow-hidden rounded-full bg-slate-200"
        role="progressbar"
        aria-valuenow={progress}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`Progression : ${progress} pourcent`}
      >
        <div
          className="h-full rounded-full bg-blue-600 transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Current step label */}
      <h2 className="text-center text-xl font-bold text-slate-800">
        Parlez-nous de votre expérience
      </h2>

      {/* Vocal button */}
      <VocalButton onStart={handleStart} onStop={handleStop} className="my-4" />

      {/* Transcript area */}
      <section
        className="min-h-[120px] w-full rounded-lg border border-slate-200 bg-white p-4 text-slate-600"
        aria-label="Transcription vocale"
        aria-live="polite"
      >
        <p className="text-center text-sm italic text-slate-400">
          Votre réponse apparaîtra ici...
        </p>
      </section>
    </div>
  );
}

export default InventairePage;

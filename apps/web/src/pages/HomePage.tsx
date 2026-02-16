import { useCallback } from "react";
import VocalButton from "../components/VocalButton";
import { useAppStore } from "../stores/appStore";

/**
 * Landing page — voice-first entry point.
 *
 * Designed for Celine: minimal text, very large button, clear
 * visual cue that this is a voice interface.  All text is at
 * least `text-xl` so it remains readable on small screens.
 */
function HomePage() {
  const setListening = useAppStore((s) => s.setListening);

  const handleStart = useCallback(() => {
    setListening(true);
  }, [setListening]);

  const handleStop = useCallback(() => {
    setListening(false);
  }, [setListening]);

  return (
    <div className="flex flex-col items-center justify-center gap-8 text-center">
      {/* Greeting */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold text-slate-800 sm:text-3xl">
          Bienvenue sur Kompetens
        </h2>
        <p className="mt-2 text-xl text-slate-600">
          Votre assistant emploi vocal
        </p>
      </div>

      {/* Primary action — large vocal button */}
      <VocalButton onStart={handleStart} onStop={handleStop} className="my-6" />

      {/* Instruction */}
      <p className="text-xl text-slate-500">Appuyez sur le micro et parlez</p>
    </div>
  );
}

export default HomePage;

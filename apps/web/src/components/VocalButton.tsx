import { useCallback } from "react";
import { useAppStore } from "../stores/appStore";

interface VocalButtonProps {
  /** Called when the user presses down — start recording. */
  onStart: () => void;
  /** Called when the user releases — stop recording. */
  onStop: () => void;
  /** Additional CSS classes. */
  className?: string;
}

/**
 * Push-to-talk microphone button.
 *
 * Designed for Celine: large touch target (80 px), no text required
 * to understand its purpose, visual + animated feedback while active.
 *
 * Uses pointer events (not click) so it works identically on touch
 * screens and with a mouse.
 */
function VocalButton({ onStart, onStop, className = "" }: VocalButtonProps) {
  const isListening = useAppStore((s) => s.isListening);
  const isProcessing = useAppStore((s) => s.isProcessing);

  const handlePointerDown = useCallback(() => {
    if (isProcessing) return;
    onStart();
  }, [isProcessing, onStart]);

  const handlePointerUp = useCallback(() => {
    if (!isListening) return;
    onStop();
  }, [isListening, onStop]);

  // Also stop on pointer-leave so releasing outside the button still
  // triggers the stop — critical on small screens.
  const handlePointerLeave = useCallback(() => {
    if (isListening) {
      onStop();
    }
  }, [isListening, onStop]);

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      {/* Animated pulse ring when listening */}
      {isListening && (
        <span
          className="animate-pulse-ring absolute h-20 w-20 rounded-full bg-blue-400"
          aria-hidden="true"
        />
      )}

      <button
        type="button"
        role="button"
        tabIndex={0}
        aria-label="Appuyer pour parler"
        aria-pressed={isListening}
        onPointerDown={handlePointerDown}
        onPointerUp={handlePointerUp}
        onPointerLeave={handlePointerLeave}
        disabled={isProcessing}
        className={`relative z-10 flex h-20 w-20 items-center justify-center rounded-full
          transition-transform duration-150 select-none
          focus:outline-none focus-visible:ring-4 focus-visible:ring-blue-300
          ${
            isProcessing
              ? "cursor-wait bg-blue-400"
              : isListening
                ? "scale-110 bg-blue-700"
                : "bg-blue-600 active:scale-110 active:bg-blue-700"
          }`}
        style={{ touchAction: "manipulation" }}
      >
        {isProcessing ? (
          /* Spinner overlay */
          <svg
            className="h-8 w-8 animate-spin text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>
        ) : (
          /* Microphone icon */
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 1a4 4 0 00-4 4v6a4 4 0 008 0V5a4 4 0 00-4-4z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M19 11a7 7 0 01-14 0"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 18v4m-3 0h6"
            />
          </svg>
        )}
      </button>
    </div>
  );
}

export default VocalButton;

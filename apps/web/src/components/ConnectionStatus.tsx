import { useEffect } from "react";
import { useAppStore } from "../stores/appStore";

/**
 * Small connectivity indicator displayed in the header.
 *
 * Listens to the browser's online / offline events and keeps
 * the Zustand store in sync so other components can react to
 * network changes (e.g. disabling the vocal button when offline).
 */
function ConnectionStatus() {
  const isOnline = useAppStore((s) => s.isOnline);
  const setOnline = useAppStore((s) => s.setOnline);

  useEffect(() => {
    const goOnline = () => setOnline(true);
    const goOffline = () => setOnline(false);

    // Sync initial state
    setOnline(navigator.onLine);

    window.addEventListener("online", goOnline);
    window.addEventListener("offline", goOffline);

    return () => {
      window.removeEventListener("online", goOnline);
      window.removeEventListener("offline", goOffline);
    };
  }, [setOnline]);

  return (
    <div
      className="flex items-center gap-1.5 text-xs"
      role="status"
      aria-live="polite"
      aria-label={isOnline ? "En ligne" : "Hors ligne"}
    >
      <span
        className={`inline-block h-2 w-2 rounded-full ${
          isOnline ? "bg-green-500" : "bg-red-500"
        }`}
      />
      <span className={isOnline ? "text-green-700" : "text-red-700"}>
        {isOnline ? "En ligne" : "Hors ligne"}
      </span>
    </div>
  );
}

export default ConnectionStatus;

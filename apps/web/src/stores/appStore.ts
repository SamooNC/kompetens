import { create } from "zustand";

interface AppState {
  /** Whether the device has network connectivity. */
  isOnline: boolean;
  /** Whether the microphone is actively recording audio. */
  isListening: boolean;
  /** Whether recorded audio is being sent / processed by the backend. */
  isProcessing: boolean;

  setOnline: (v: boolean) => void;
  setListening: (v: boolean) => void;
  setProcessing: (v: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isOnline: true,
  isListening: false,
  isProcessing: false,

  setOnline: (v) => set({ isOnline: v }),
  setListening: (v) => set({ isListening: v }),
  setProcessing: (v) => set({ isProcessing: v }),
}));

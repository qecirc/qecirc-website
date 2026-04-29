declare global {
  interface Window {
    showCiteToast?: (msg: string, url?: string) => void;
  }
}

export {};

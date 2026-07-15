declare global {
  interface Window {
    showCiteToast?: (msg: string, url?: string, linkLabel?: string) => void;
  }
}

export {};

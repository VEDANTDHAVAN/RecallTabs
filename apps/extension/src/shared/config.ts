export interface ExtensionConfig {
  apiBaseUrl: string;
  environment: "development" | "production";
}

const isProduction = false;

export const extensionConfig: ExtensionConfig = {
  apiBaseUrl: isProduction ? "https://api.recalltabs.app" : "http://localhost:8000",
  environment: isProduction ? "production" : "development",
};

export const API_BASE_URL = extensionConfig.apiBaseUrl;

export function getApiBaseUrl(): string {
  return extensionConfig.apiBaseUrl;
}

export function shouldIgnoreUrl(url: string): boolean {
  const normalized = url.trim().toLowerCase();

  if (!normalized) {
    return true;
  }

  const ignoredPrefixes = [
    "about:",
    "chrome://",
    "chrome-extension://",
    "devtools://",
    "edge://",
    "moz-extension://",
  ];

  if (ignoredPrefixes.some((prefix) => normalized.startsWith(prefix))) {
    return true;
  }

  if (normalized.includes("localhost") || normalized.includes("127.0.0.1")) {
    return true;
  }

  if (normalized.includes("swagger") || normalized.includes("devtools")) {
    return true;
  }

  return false;
}

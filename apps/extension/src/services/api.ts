import type { CapturePayload } from "../shared/types";
import { API_BASE_URL } from "../shared/config";

interface HealthResponse {
  status: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers || {}),
      },
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`API Error ${response.status}: ${text}`);
    }

    return (await response.json()) as T;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`Request failed for ${path}: ${message}`);
  }
}

export async function captureTab(payload: CapturePayload): Promise<{ id: string; title: string }> {
  return request<{ id: string; title: string }>("/api/v1/tabs/capture", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function health(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

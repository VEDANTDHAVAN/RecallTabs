import { apiFetch } from "./client";

export interface CaptureTabRequest {
    browser_tab_id: number;
    title: string;
    url: string;
}

export async function captureTab(
    payload: CaptureTabRequest
) {
    return apiFetch("/tabs/capture", {
        method: "POST", body: JSON.stringify(payload),
    });
}
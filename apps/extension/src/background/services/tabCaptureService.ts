import { api } from "../../shared/api/client";

import type {
    TabCaptureRequest,
} from "../../shared/types/tab-capture";

export async function captureTab(
    payload: TabCaptureRequest
) {
    await api.post("/tabs/capture", payload)
}
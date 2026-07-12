export interface CapturePayload {
  browser_tab_id: number;
  title: string;
  url: string;
  content: string;
  description: string;
  favicon: string | null;
  word_count: number;
}

export interface CaptureJob {
  id: string;
  payload: CapturePayload;
  retries: number;
  createdAt: number;
  contentHash: string;
  lastError?: string;
}

export type UploadStatus = "idle" | "uploading" | "queued" | "synced" | "failed";

export interface QueueStatus {
  status: UploadStatus;
  queuedCount: number;
  currentUpload: string | null;
  lastError: string | null;
  isOnline: boolean;
}

export interface QueueStatusMessage {
  type: "QUEUE_STATUS_UPDATE";
  status: QueueStatus;
}

export interface RequestCaptureMessage {
  type: "REQUEST_CAPTURE";
  payload: CapturePayload;
}

export interface GetQueueStatusMessage {
  type: "GET_QUEUE_STATUS";
}

export interface CaptureRequestedMessage {
  type: "CAPTURE_REQUESTED";
  payload: CapturePayload;
}

export interface ExtractPageMessage {
  type: "EXTRACT_PAGE";
}

export interface PageExtractionResponse {
  browser_tab_id?: number;
  title: string;
  url: string;
  content: string;
  description: string;
  favicon: string | null;
  wordCount: number;
}

export type BackgroundMessage =
  | RequestCaptureMessage
  | GetQueueStatusMessage
  | CaptureRequestedMessage
  | QueueStatusMessage
  | ExtractPageMessage;


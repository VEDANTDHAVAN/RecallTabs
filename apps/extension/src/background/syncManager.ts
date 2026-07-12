import type { CaptureJob, QueueStatus } from "../shared/types";
import { CaptureQueue } from "./captureQueue";
import { logger } from "../shared/logger";
import { captureTab } from "../services/api";

const MAX_RETRIES = 4;

interface SyncManagerOptions {
  onStatusChange?: (status: QueueStatus) => void;
}

export class SyncManager {
  private isRunning = false;
  private isUploading = false;
  private retryHandle: number | null = null;
  private readonly status: QueueStatus;

  constructor(
    private readonly queue: CaptureQueue,
    private readonly options: SyncManagerOptions = {},
  ) {
    this.status = {
      status: "idle",
      queuedCount: 0,
      currentUpload: null,
      lastError: null,
      isOnline: navigator.onLine,
    };
  }

  async start(): Promise<void> {
    if (this.isRunning) {
      return;
    }

    this.isRunning = true;
    this.publishStatus();
    await this.processQueue();
  }

  async stop(): Promise<void> {
    this.isRunning = false;
    if (this.retryHandle !== null) {
      clearTimeout(this.retryHandle);
      this.retryHandle = null;
    }
    try {
      await chrome.alarms.clear("sync-retry");
    } catch (error) {
      logger.debug("Failed to clear alarm on stop", error);
    }
    this.publishStatus();
  }

  getStatus(): QueueStatus {
    return { ...this.status, queuedCount: this.queue.size() };
  }

  async processQueue(): Promise<void> {
    if (!this.isRunning) {
      this.status.status = this.queue.size() > 0 ? "queued" : "idle";
      this.status.isOnline = navigator.onLine;
      this.publishStatus();
      return;
    }

    if (this.isUploading) {
      return;
    }

    const size = this.queue.size();
    this.status.queuedCount = size;
    this.status.isOnline = navigator.onLine;

    if (size === 0) {
      this.status.status = "synced";
      this.status.currentUpload = null;
      this.publishStatus();
      return;
    }

    if (!navigator.onLine) {
      this.status.status = "queued";
      this.status.currentUpload = null;
      this.status.isOnline = false;
      this.publishStatus();
      return;
    }

    const nextJob = this.queue.peek();
    if (!nextJob) {
      this.status.status = "synced";
      this.status.currentUpload = null;
      this.publishStatus();
      return;
    }

    this.isUploading = true;
    this.status.status = "uploading";
    this.status.currentUpload = nextJob.id;
    this.publishStatus();

    let uploadSuccess = false;
    try {
      await this.uploadJob(nextJob);
      uploadSuccess = true;
      await this.queue.dequeue();
      this.status.lastError = null;
      logger.info("Capture uploaded successfully", { jobId: nextJob.id });
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      nextJob.retries += 1;
      await this.queue.persist();
      this.status.lastError = message;
      this.status.currentUpload = null;

      if (this.shouldRetry(error, nextJob)) {
        const delay = Math.min(30000, 1000 * 2 ** nextJob.retries);
        logger.warn("Capture upload failed; retry scheduled", {
          jobId: nextJob.id,
          attempt: nextJob.retries,
          delay,
          message,
        });
        this.status.status = "queued";
        this.scheduleRetry(delay);
      } else {
        logger.error("Capture upload failed permanently", { jobId: nextJob.id, message });
        await this.queue.dequeue();
        this.status.status = this.queue.size() > 0 ? "queued" : "failed";
      }
    } finally {
      this.isUploading = false;
      this.status.queuedCount = this.queue.size();
      this.status.isOnline = navigator.onLine;

      if (uploadSuccess) {
        this.status.status = this.queue.size() > 0 ? "queued" : "synced";
        this.status.currentUpload = null;
      }

      this.publishStatus();

      // Only schedule immediate next job processing if the previous job succeeded
      if (uploadSuccess && this.queue.size() > 0 && navigator.onLine) {
        setTimeout(() => {
          void this.processQueue();
        }, 250);
      }
    }
  }

  private async uploadJob(job: CaptureJob): Promise<void> {
    await captureTab(job.payload);
  }

  private shouldRetry(error: unknown, job: CaptureJob): boolean {
    if (!navigator.onLine) {
      return true;
    }

    const message = error instanceof Error ? error.message : String(error);
    const recoverable = /5\d\d|429|408|network|fetch|offline|timeout/i.test(message);
    return recoverable && job.retries < MAX_RETRIES;
  }

  private scheduleRetry(delayMs: number): void {
    if (!this.isRunning) {
      return;
    }

    if (this.retryHandle !== null) {
      clearTimeout(this.retryHandle);
      this.retryHandle = null;
    }

    this.retryHandle = setTimeout(() => {
      this.retryHandle = null;
      void this.processQueue();
    }, delayMs) as unknown as number;

    try {
      const delayInMinutes = Math.max(1, delayMs / 60000);
      void chrome.alarms.clear("sync-retry").then(() => {
        chrome.alarms.create("sync-retry", { delayInMinutes });
      }).catch((err) => {
        logger.error("Failed to schedule fallback chrome alarm", err);
      });
    } catch (error) {
      logger.error("Failed to access chrome.alarms", error);
    }
  }

  private publishStatus(): void {
    this.status.queuedCount = this.queue.size();
    this.options.onStatusChange?.({ ...this.status });
  }
}

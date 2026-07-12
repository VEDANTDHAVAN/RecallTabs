import type { CaptureJob, CapturePayload } from "../shared/types";
import { logger } from "../shared/logger";

const STORAGE_KEY = "recalltabs.captureQueue";

export class CaptureQueue {
  private jobs: CaptureJob[] = [];

  constructor(private readonly storageKey = STORAGE_KEY) {}

  async load(): Promise<void> {
    try {
      const stored = await chrome.storage.local.get(this.storageKey);
      const serialized = stored[this.storageKey] as CaptureJob[] | undefined;
      if (Array.isArray(serialized)) {
        this.jobs = this.deserialize(serialized);
      }
    } catch (error) {
      logger.error("Failed to restore capture queue", error);
      this.jobs = [];
    }
  }

  async persist(): Promise<void> {
    try {
      await chrome.storage.local.set({ [this.storageKey]: this.serialize() });
    } catch (error) {
      logger.error("Failed to persist capture queue", error);
    }
  }

  async enqueue(payload: CapturePayload): Promise<CaptureJob | null> {
    const contentHash = await this.createContentHash(payload.url, payload.content);
    if (this.hasDuplicate(payload.url, contentHash)) {
      logger.info("Skipped duplicate capture job", { url: payload.url });
      return null;
    }

    const job: CaptureJob = {
      id: crypto.randomUUID(),
      payload,
      retries: 0,
      createdAt: Date.now(),
      contentHash,
    };

    this.jobs.push(job);
    await this.persist();
    return job;
  }

  async dequeue(): Promise<CaptureJob | null> {
    const job = this.jobs.shift() ?? null;
    if (job) {
      await this.persist();
    }
    return job;
  }

  peek(): CaptureJob | null {
    return this.jobs[0] ?? null;
  }

  async remove(jobId: string): Promise<boolean> {
    const previousLength = this.jobs.length;
    this.jobs = this.jobs.filter((job) => job.id !== jobId);
    if (this.jobs.length !== previousLength) {
      await this.persist();
      return true;
    }
    return false;
  }

  size(): number {
    return this.jobs.length;
  }

  async clear(): Promise<void> {
    this.jobs = [];
    await this.persist();
  }

  serialize(): CaptureJob[] {
    return this.jobs.map((job) => ({ ...job, payload: { ...job.payload } }));
  }

  deserialize(serialized: CaptureJob[]): CaptureJob[] {
    return serialized.map((job) => ({
      ...job,
      payload: { ...job.payload },
    }));
  }

  list(): CaptureJob[] {
    return this.serialize();
  }

  private hasDuplicate(url: string, contentHash: string): boolean {
    return this.jobs.some((job) => job.payload.url === url && job.contentHash === contentHash);
  }

  private async createContentHash(url: string, content: string): Promise<string> {
    const encoder = new TextEncoder();
    const payload = `${url}:${content}`;
    const hashBuffer = await crypto.subtle.digest("SHA-256", encoder.encode(payload));
    return Array.from(new Uint8Array(hashBuffer))
      .map((byte) => byte.toString(16).padStart(2, "0"))
      .join("");
  }
}

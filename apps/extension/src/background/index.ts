import type { BackgroundMessage, CapturePayload, QueueStatus } from "../shared/types";
import { shouldIgnoreUrl } from "../shared/config";
import { logger } from "../shared/logger";
import { CaptureQueue } from "./captureQueue";
import { SyncManager } from "./syncManager";

const queue = new CaptureQueue();
const syncManager = new SyncManager(queue, {
  onStatusChange: (status) => {
    void broadcastStatus(status);
  },
});

let initialized = false;

async function initialize(): Promise<void> {
  if (initialized) {
    return;
  }

  initialized = true;
  await queue.load();
  registerListeners();
  logger.info("Background service initialized");
  await syncManager.start();
  await broadcastStatus(syncManager.getStatus());
}

function registerListeners(): void {
  chrome.runtime.onInstalled.addListener(() => {
    void initialize();
  });

  chrome.runtime.onStartup.addListener(() => {
    void initialize();
  });

  chrome.runtime.onMessage.addListener((message: BackgroundMessage, _sender, sendResponse) => {
    void (async () => {
      if (message.type === "REQUEST_CAPTURE") {
        await enqueueCapture(message.payload);
        sendResponse({ type: "CAPTURE_REQUESTED", payload: message.payload });
        return;
      }

      if (message.type === "GET_QUEUE_STATUS") {
        sendResponse({ type: "QUEUE_STATUS_UPDATE", status: syncManager.getStatus() });
      }
    })();

    return true;
  });

  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status !== "complete") {
      return;
    }

    void handleTabCapture(tabId, tab);
  });

  chrome.tabs.onActivated.addListener(({ tabId }) => {
    void chrome.tabs.get(tabId).then((tab) => {
      void handleTabCapture(tabId, tab);
    }).catch((error) => {
      logger.error("Failed to inspect activated tab", error);
    });
  });

  chrome.windows.onFocusChanged.addListener((windowId) => {
    if (windowId === chrome.windows.WINDOW_ID_NONE) {
      return;
    }

    void chrome.tabs.query({ active: true, windowId }).then((tabs) => {
      const [activeTab] = tabs;
      if (activeTab?.id) {
        void handleTabCapture(activeTab.id, activeTab);
      }
    }).catch((error) => {
      logger.error("Failed to inspect active window tab", error);
    });
  });

  chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === "sync-retry") {
      logger.info("Chrome alarm 'sync-retry' fired; processing queue.");
      void syncManager.processQueue();
    }
  });
}

async function handleTabCapture(tabId: number, tab?: chrome.tabs.Tab): Promise<void> {
  if (!tab?.url || shouldIgnoreUrl(tab.url)) {
    return;
  }

  if (tab.status && tab.status !== "complete") {
    return;
  }

  try {
    const response = await chrome.tabs.sendMessage(tabId, { type: "EXTRACT_PAGE" });
    if (!response?.url) {
      return;
    }

    await enqueueCapture({
      browser_tab_id: tabId,
      title: response.title,
      url: response.url,
      content: response.content,
      description: response.description,
      favicon: response.favicon ?? null,
      word_count: response.wordCount,
    });
  } catch (error) {
    logger.error("Failed to extract tab content", error);
  }
}

async function enqueueCapture(payload: CapturePayload): Promise<void> {
  const job = await queue.enqueue(payload);
  if (job) {
    logger.info("Capture queued", { jobId: job.id, url: payload.url });
  } else {
    logger.info("Capture skipped as duplicate", { url: payload.url });
  }

  await broadcastStatus(syncManager.getStatus());
  await syncManager.processQueue();
}

async function broadcastStatus(status: QueueStatus): Promise<void> {
  try {
    await chrome.runtime.sendMessage({ type: "QUEUE_STATUS_UPDATE", status });
  } catch (error) {
    logger.debug("Status broadcast skipped", error);
  }
}

void initialize();
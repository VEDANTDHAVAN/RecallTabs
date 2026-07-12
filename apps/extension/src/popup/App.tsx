import { useEffect, useState } from "react";
import SearchPanel from "../components/SearchPanel";
import type { QueueStatus } from "../shared/types";

const initialStatus: QueueStatus = {
  status: "idle",
  queuedCount: 0,
  currentUpload: null,
  lastError: null,
  isOnline: navigator.onLine,
};

export default function App() {
  const [status, setStatus] = useState<QueueStatus>(initialStatus);

  useEffect(() => {
    function isQueueStatusUpdate(m: unknown): m is { type: "QUEUE_STATUS_UPDATE"; status: QueueStatus } {
      if (typeof m !== "object" || m === null) {
        return false;
      }
      const msg = m as Record<string, unknown>;
      return msg.type === "QUEUE_STATUS_UPDATE" && "status" in msg;
    }

    const updateFromBackground = (message: unknown) => {
      if (isQueueStatusUpdate(message)) {
        setStatus(message.status);
      }
    };

    chrome.runtime.sendMessage({ type: "GET_QUEUE_STATUS" })
      .then((response) => {
        if (isQueueStatusUpdate(response)) {
          setStatus(response.status);
        }
      })
      .catch(() => {
      setStatus((current) => ({ ...current, status: "failed", lastError: "Background service unavailable" }));
    });

    chrome.runtime.onMessage.addListener(updateFromBackground);

    return () => {
      chrome.runtime.onMessage.removeListener(updateFromBackground);
    };
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, minWidth: 340 }}>
      <section style={{ border: "1px solid #d1d5db", borderRadius: 12, padding: 12, background: "#fff" }}>
        <div style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5, color: "#6b7280" }}>
          Sync Status
        </div>
        <div style={{ marginTop: 8, fontSize: 16, fontWeight: 600 }}>
          {status.status === "uploading" ? "Uploading..." : status.status === "queued" ? "Queued" : status.status === "failed" ? "Failed" : status.status === "synced" ? "Synced" : "Idle"}
        </div>
        <div style={{ color: "#4b5563", fontSize: 13, marginTop: 4 }}>
          {status.queuedCount} queued item{status.queuedCount === 1 ? "" : "s"}
        </div>
        {status.currentUpload ? (
          <div style={{ color: "#2563eb", fontSize: 13, marginTop: 4 }}>
            Uploading job {status.currentUpload}
          </div>
        ) : null}
        {status.lastError ? (
          <div style={{ color: "#dc2626", fontSize: 13, marginTop: 4 }}>
            {status.lastError}
          </div>
        ) : null}
      </section>
      <SearchPanel />
    </div>
  );
}
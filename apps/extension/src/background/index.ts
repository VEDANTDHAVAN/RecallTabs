import { captureTab } from "./services/tabCaptureService";

console.log("RecallTabs Background Started");

chrome.tabs.onUpdated.addListener(
  async (tabId, changeInfo, tab) => {
    if (changeInfo.status !== "complete") {
      return;
    }

    if(!tab.url) {
      return;
    }

    if (
      tab.url.startsWith("chrome://") ||
      tab.url.startsWith("chrome-extension://")
    ) {
      return;
    }

    try {
      console.log("Capturing:", tab.title);

      const result = await captureTab({
        browser_tab_id: tabId,
        title: tab.title || "Untitled",
        url: tab.url,
      });

      console.log("Capture Success", result);
    } catch (error) {
      console.error("Capture Failed", error);
    }
  }
);
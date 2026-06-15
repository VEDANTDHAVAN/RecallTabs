import { captureTab } from "./services/tabCaptureService";

chrome.tabs.onUpdated.addListener(
  async (tabId, changeInfo, tab) => {
    if (
      changeInfo.status !==
      "complete"
    ) {
      return;
    }

    if(!tab.url) {
      return;
    }

    try {
      await captureTab({
        browser_tab_id: tabId,
        title: tab.title ?? "",
        url: tab.url,
        favicon: tab.favIconUrl,
      });
    } catch (error) {
      console.error("Capture failed", error);
    }
  }
);
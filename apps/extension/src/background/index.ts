console.log("BACKGROUND WORKS");
const API_BASE_URL = "http://localhost:8000";

console.log("RecallTabs Background Started");
chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension Installed");
});

chrome.tabs.onUpdated.addListener(

  async (tabId, changeInfo, tab) => {

    if (changeInfo.status !== "complete") {
      return;
    }

    if (
      !tab.url ||

      tab.url.startsWith("chrome://") ||

      tab.url.startsWith("chrome-extension://") ||

      tab.url.startsWith("edge://") ||

      tab.url.startsWith("about:")
    ) {
      return;
    }

    try {

      const response =
        await chrome.tabs.sendMessage(
          tabId,
          {
            type: "EXTRACT_PAGE",
          }
        );

      if (!response) {
        return;
      }

      const apiResponse = await fetch(

        `${API_BASE_URL}/api/v1/tabs/capture`,

        {

          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            browser_tab_id: tabId,

            url: response.url,
            title: response.title,

            content: response.content,
            description: response.description,

            favicon: null, word_count: response.wordCount,
          }),
        }
      );

      if (!apiResponse.ok) {

        const text =
          await apiResponse.text();

        throw new Error(text);
      }

      console.log(
        "Tab Captured",
        response
      );

    }

    catch (error) {

      console.error(

        "Capture Failed",

        error

      );

    }

  }

);
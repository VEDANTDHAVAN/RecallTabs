console.log(
  "RecallTabs Background Started"
);

chrome.tabs.onUpdated.addListener(
  (
    tabId,
    changeInfo,
    tab
  ) => {
    if (
      changeInfo.status !==
      "complete"
    ) {
      return;
    }

    console.log(
      "Tab Updated",
      {
        id: tabId,
        title: tab.title,
        url: tab.url
      }
    );
  }
);
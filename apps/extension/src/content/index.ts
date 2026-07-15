console.log("[RecallTabs] Content script loaded");
import { logger } from "../shared/logger";
//import "./injectSidebar";

function extractPageContent() {
  const title = document.title;
  const url = window.location.href;
  const content = document.body?.innerText?.trim() || "";
  const description = document.querySelector('meta[name="description"]')?.getAttribute("content")?.trim() || "";
  const favicon =
    (document.querySelector('link[rel="icon"]') as HTMLLinkElement | null)?.href ||
    (document.querySelector('link[rel="shortcut icon"]') as HTMLLinkElement | null)?.href ||
    null;

  return {
    title,
    url,
    content,
    description,
    favicon,
    wordCount: content.length > 0 ? content.split(/\s+/).length : 0,
  };
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "EXTRACT_PAGE") {
    try {
      const page = extractPageContent();
      sendResponse({
        browser_tab_id: sender.tab?.id,
        title: page.title,
        url: page.url,
        content: page.content,
        description: page.description,
        favicon: page.favicon,
        wordCount: page.wordCount,
      });
    } catch (error) {
      logger.error("Content extraction failed", error);
      sendResponse(null);
    }
  }

  return true;
});
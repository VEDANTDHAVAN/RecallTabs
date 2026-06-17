console.log("CONTENT WORKS");
function extractPageContent() {
  const title = document.title;
  const url = window.location.href;
  const content = document.body?.innerText?.trim() || "";
  const description = document.querySelector(
        'meta[name="description"]'
      )?.getAttribute("content")?.trim() || "";

  const favicon =(
      document.querySelector(
        'link[rel="icon"]'
      ) as HTMLLinkElement
    )?.href || (
      document.querySelector(
        'link[rel="shortcut icon"]'
      ) as HTMLLinkElement
    )?.href || null;

  console.log({
    title, url, content,
    description, favicon,
    wordCount: content.length > 0
        ? content.split(/\s+/).length : 0,
  })
  
  return {
    title, url, content,
    description, favicon,
    wordCount: content.length > 0
        ? content.split(/\s+/).length : 0,
  };
}

chrome.runtime.onMessage.addListener((
    message, sender, sendResponse
  ) => {
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
      }

      catch (error) {
        console.error(
          "Content Extraction Failed", error
        );
        sendResponse(null);
      }
    }

    return true;
  }
);
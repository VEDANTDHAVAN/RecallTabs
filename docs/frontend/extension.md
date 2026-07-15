# Browser Extension

`apps/extension` is a React/Vite/CRXJS Manifest V3 extension.

The content script extracts document text, title, URL, description, favicon, and word count when the background worker requests `EXTRACT_PAGE`. The background worker reacts to completed loads, activation, and focus changes, filters internal/development URLs, queues a hashed payload in `chrome.storage.local`, and uploads it to the capture API through `SyncManager`. Queue retry uses exponential backoff and a Chrome alarm fallback.

The popup (`src/popup/App.tsx`) shows sync state and `SearchPanel`. It has no authentication, capture controls, settings, provider management, or conversation UI. Chat/sidebar components exist but are not mounted by the popup. `injectSidebar.ts` is commented out in the content script, so the static sidebar is inactive.

There are two API client families: `src/services/api.ts` uses `fetch` and the configured base URL; `src/shared/api/client.ts` uses Axios and re-exported config. There are also duplicate capture request definitions, one of which omits content/description/word count. Consolidate them only after preserving the queue’s full payload contract.

The generated manifest uses `manifest.config.ts`; `public/manifest.json` is a stale parallel manifest and should not be treated as the build source.

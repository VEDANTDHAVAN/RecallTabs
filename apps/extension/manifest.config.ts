import { defineManifest } from "@crxjs/vite-plugin";

export default defineManifest({
    manifest_version: 3,
    name: "RecallTabs",

    version: "0.1.0",

    permissions: [
        "tabs", "storage"
    ],

    host_permissions: [
        "http://localhost:8000/*",
        "http://127.0.0.1:8000/*"
    ],

    background: {
        service_worker: "src/background/index.ts",
        type: "module"
    },

    "content_scripts": [
        {
            "matches": ["<all_urls>"],
            "js": ["content.js"]
        }
    ],

    action: {
        default_popup: "index.html"
    }
});
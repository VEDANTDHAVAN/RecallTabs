# Web Dashboard

No RecallTabs dashboard is implemented yet. `apps/web` is the untouched Next.js/Turborepo starter: template metadata, template page content, and starter assets. It has no auth client, API client, routes, state management, dashboard components, or settings pages.

The extension popup is currently the live product surface. A dashboard should be introduced only after API authentication/user scoping contracts are stable, starting with read-only, authenticated memory views rather than duplicating extension capture logic.

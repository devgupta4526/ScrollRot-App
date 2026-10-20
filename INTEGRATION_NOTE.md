# Integration note: Android starter + Render backend docs

This ZIP combines the **existing experimental Kotlin/XML Android starter source** with the refreshed **Render/Django/PostgreSQL specifications and implementation prompts**. It does NOT yet include a working backend implementation or a deployed Render service. The app has not been fully compiled in this environment.

The authoritative path to the backend is:
1. `RENDER_MIGRATION.md`
2. `docs/16_BACKEND_AND_SOCIAL.md`
3. `docs/23_RENDER_DEPLOYMENT.md`
4. `docs/24_API_CONTRACT.md`
5. `prompts/09_RENDER_BACKEND_SETUP.md`, then `10_AUTH_AND_FRIENDS.md`, `11_GROUP_BATTLES.md`

The underlying Android tracker stays offline-first. No Firebase dependency is required or desired.

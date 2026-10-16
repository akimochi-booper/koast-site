# Website chat Worker

Recovered from the deployed `koast-chat` Worker on 2026-10-16 (active version 45eea2db, secret-only successor 79e6ba32), then migrated to OpenAI Responses. This folder is the source of truth. GitHub Actions deploys it on changes pushed to main; the main Pages job excludes the entire workers folder.

Runtime secret: `OPENAI_API_KEY`, installed in Cloudflare, never in Git or Pages. Optional runtime variable: `OPENAI_CHAT_MODEL` (default `gpt-6-luna`). The production key must be present before deployment. Old Anthropic secrets can remain unused during rollback validation.

The website remains a tool-less information assistant: same live llms.txt fact source, conversation limits, booking/refund handoff rules, reply JSON, CORS origins, and human fallback. Responses are not stored by OpenAI (`store:false`).

Validate with `npm run check`, `npm test`, and an esbuild ESM bundle check. Run a synthetic chat through the live website after a deployment; API-key validation alone does not verify this integration.

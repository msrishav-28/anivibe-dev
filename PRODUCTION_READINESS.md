# AniVibe Production Readiness Tracker

Status values:

- `broken`: known blocker or stale implementation.
- `stub`: intentionally present but not production-capable.
- `baseline`: working production foundation or deterministic fallback.
- `production`: verified with deployed infrastructure, tests, and monitoring.

## Current Status

| Subsystem | Status | Notes |
|---|---:|---|
| Backend startup/imports | baseline | Runtime Supabase imports were removed, Redis is optional outside production, and heavy ML services are lazy-loaded. |
| Database | baseline | Alembic now has a single initial Neon/Postgres schema with pgvector and lineage tables. Needs live Neon migration verification. |
| Auth | baseline | Backend validates Clerk bearer tokens and maps them to internal profiles. Requires Clerk issuer/JWKS env values. |
| Storage | baseline | Avatar uploads target Cloudflare R2. Requires R2 credentials and public base URL. |
| API contract | baseline | Frontend client is aligned with the main backend routes. More contract tests are still needed. |
| Local runtime | baseline | Docker Compose now includes local Postgres/pgvector and Redis so local work no longer needs cloud credentials. |
| Data ingestion | baseline | MAL/Jikan script imports the 250-anime smoke corpus into Postgres and records dataset lineage/validation. |
| Embeddings | baseline | SBERT embeddings can be generated into `anime_embeddings` with dataset-version lineage and CPU-first defaults. |
| Semantic search | baseline | Uses pgvector via `anime_embeddings`, with remote Modal fallback when local model libs are absent. |
| Visual search | stub | Local CLIP poster embedding/evaluation script exists; endpoint stays feature-flagged off until metrics pass. |
| Recommendations | baseline | Existing content/collaborative baseline remains; advanced GNN/BERT4Rec are not production. |
| Explainability | baseline | Explanations are transparent heuristic factors, not SHAP/LIME-backed model explanations. |
| MLOps | baseline | Dataset/model/event/inference tables exist; promotion/evaluation jobs still need implementation. |
| Security | baseline | Clerk JWTs, local-only dev auth, ownership checks, R2 upload validation, request IDs, and route-aware rate limiting are in place. |
| Frontend auth | baseline | Clerk provider and SignIn/SignUp pages are wired. Full UX pass still needed. |
| Deployment | baseline | Render envs now target Neon/Clerk/R2/Redis. Needs staging deployment verification. |
| Testing | baseline | Backend tests, ruff, Python import checks, and frontend type-check pass locally; live Postgres smoke checks still require Docker. |
| Observability | baseline | Request IDs and basic logs are present. Metrics/alerts/runbooks still needed. |
| Documentation | baseline | This tracker is the source of truth until README/DEPLOYMENT are rewritten fully. |

## Immediate Release Blockers

1. Configure real Neon, Clerk, R2, Upstash, and Modal secrets.
2. Run Alembic against an empty Neon branch.
3. Run the local Docker Postgres/Redis stack on a machine with Docker Desktop installed.
4. Seed/import anime data and generate SBERT embeddings against local pgvector.
5. Add CI with backend import tests, migration checks, API contract tests, and frontend type-check.
6. Replace old marketing claims in README/strategy docs with implemented/beta/planned labels.

## Local-First Smoke Workflow

1. Copy `.env.example` to `.env`.
2. Start local infrastructure: `docker compose up -d postgres redis`.
3. Run migrations: `alembic upgrade head`.
4. Import smoke data: `python scripts/fetch_mal_data.py --limit 250 --import-db`.
5. Generate text embeddings: `python scripts/generate_embeddings.py --batch-size 16`.
6. Start the API from PowerShell: `$env:AUTH_REQUIRED='false'; uvicorn app.main:app --reload`.
7. Validate product flow: `python scripts/local_product_smoke.py`.
8. Evaluate poster visual search only after text/recommendation smoke passes: `python scripts/evaluate_visual_search.py --limit 250 --generate --evaluate`.

## External Setup Checklist

- Neon: create project, enable `vector`, set pooled `DATABASE_URL`, set direct `DATABASE_MIGRATION_URL`.
- Clerk: create app, configure frontend publishable key, set backend `CLERK_ISSUER` and `CLERK_JWKS_URL`.
- Cloudflare R2: create bucket, public media domain, and scoped access keys.
- Upstash/Redis: configure `REDIS_URL`.
- Modal: create `anivibe-production` secret with `DATABASE_URL`, then deploy `modal_app.py`.

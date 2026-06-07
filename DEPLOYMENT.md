# AniVibe Deployment Guide

This guide reflects the current production target:

- Frontend: Vercel
- Backend API: Render
- Database: Neon Postgres with pgvector
- Auth: Clerk
- Storage: Cloudflare R2
- Cache: Upstash Redis or Render Redis
- ML service: Modal

## 1. Neon Postgres

1. Create a Neon project and database.
2. Enable pgvector:

   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

3. Set backend environment variables:

   ```text
   DATABASE_URL=postgresql+asyncpg://...pooler.../anivibe?ssl=require
   DATABASE_MIGRATION_URL=postgresql://...direct.../anivibe?ssl=require
   ```

4. Run migrations:

   ```bash
   alembic upgrade head
   ```

## 2. Clerk

1. Create a Clerk application.
2. Set frontend variables in Vercel:

   ```text
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
   CLERK_SECRET_KEY=...
   ```

3. Set backend variables in Render:

   ```text
   CLERK_ISSUER=https://your-clerk-domain
   CLERK_JWKS_URL=https://your-clerk-domain/.well-known/jwks.json
   CLERK_SECRET_KEY=...
   ```

The backend does not own signup, login, refresh, logout, or password reset flows. It verifies Clerk bearer tokens and creates the internal AniVibe profile on first authenticated API request.

## 3. Cloudflare R2

1. Create an R2 bucket for media.
2. Configure a public domain or CDN route.
3. Set backend variables:

   ```text
   R2_ACCOUNT_ID=...
   R2_ACCESS_KEY_ID=...
   R2_SECRET_ACCESS_KEY=...
   R2_BUCKET=anivibe-media
   R2_PUBLIC_BASE_URL=https://media.yourdomain.com
   ```

## 4. Redis

Set `REDIS_URL` to an Upstash or Render Redis connection string. In production, set:

```text
REDIS_REQUIRED=true
```

## 5. Modal ML Service

1. Create a Modal secret named `anivibe-production`.
2. Add `DATABASE_URL` to that secret.
3. Deploy:

   ```bash
   modal deploy modal_app.py
   ```

4. Set `ML_SERVICE_URL` in Render to the Modal endpoint URL.

## 6. Render Backend

Render uses `render.yaml`.

Confirm these values:

```text
buildCommand=pip install -r requirements-api.txt
startCommand=uvicorn app.main:app --host 0.0.0.0 --port $PORT
healthCheckPath=/health
```

Required env vars:

```text
DATABASE_URL
DATABASE_MIGRATION_URL
CLERK_ISSUER
CLERK_JWKS_URL
CLERK_SECRET_KEY
R2_ACCOUNT_ID
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET
R2_PUBLIC_BASE_URL
REDIS_URL
ML_SERVICE_URL
CORS_ORIGINS
```

## 7. Vercel Frontend

Set:

```text
NEXT_PUBLIC_API_URL=https://your-render-backend.onrender.com/api/v1
NEXT_PUBLIC_APP_URL=https://your-frontend-domain
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
CLERK_SECRET_KEY=...
```

## 8. Release Gate

Before production:

```bash
python -c "import app.main"
python -m pytest tests -q
npm --prefix frontend run type-check
```

Also verify:

- `alembic upgrade head` succeeds on a clean Neon branch.
- `/health` returns 200 in staging.
- Clerk-authenticated requests can call `/api/v1/auth/me`.
- Avatar upload writes to R2.
- Semantic search returns real pgvector results after embeddings are generated.

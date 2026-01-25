# 🚀 AniVibe Setup Guide

## Architecture Overview

**Pure Supabase Stack** - Single database, minimal infrastructure

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────┐
│   Next.js       │─────▶│   FastAPI    │─────▶│  Supabase   │
│   Frontend      │      │   Backend    │      │  PostgreSQL │
│  (localhost:3000)│      │(localhost:8000)│      │   (Cloud)   │
└─────────────────┘      └──────────────┘      └─────────────┘
                              │
                              ▼
                         ┌──────────┐
                         │  Redis   │
                         │ (Cache)  │
                         └──────────┘
```

---

## Prerequisites

- **Node.js** 18.17.0+
- **Python** 3.10+
- **Docker** (for Redis)
- **Supabase Account** (free tier works)
- **Gemini API Key** (for LLM features)

---

## 1. Clone & Navigate

```bash
git clone https://github.com/msrishav-28/anivibe-dev.git
cd anivibe-dev
```

---

## 2. Supabase Setup

### Create Project
1. Go to [supabase.com](https://supabase.com)
2. Create new project (choose Mumbai/ap-south-1 region)
3. Wait 2 minutes for provisioning

### Get Credentials
```
Project Settings → API → Copy:
- Project URL (SUPABASE_URL)
- anon/public key (SUPABASE_ANON_KEY)  
- service_role key (SUPABASE_SERVICE_KEY)
```

### Run Database Migrations

**Option A: Using Supabase SQL Editor (Recommended)**
1. Go to SQL Editor in Supabase Dashboard
2. Copy SQL from `alembic/versions/*.py` files
3. Execute in order

**Option B: Using Alembic**
```bash
# After backend setup
alembic upgrade head
```

---

## 3. Backend Setup

### Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Environment
```bash
cp .env.example .env
```

**Edit `.env` with your values:**
```bash
# Required
SECRET_KEY=generate-random-32-char-string-here
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
GEMINI_API_KEY=your-gemini-api-key

# Optional (defaults work)
REDIS_HOST=localhost
REDIS_PORT=6379
USE_GPU=false
```

### Generate Secret Key
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Start Redis (Docker)
```bash
docker-compose up -d
```

### Start Backend
```bash
uvicorn app.main:app --reload
```

**Verify:** http://localhost:8000/docs (Swagger UI)

---

## 4. Frontend Setup

### Install Dependencies
```bash
cd frontend
npm install
```

### Configure Environment
```bash
cp .env.local.example .env.local
```

**Edit `.env.local`:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Start Frontend
```bash
npm run dev
```

**Verify:** http://localhost:3000

---

## 5. Verify Integration

### Test Checklist
- [ ] Backend Swagger docs load (http://localhost:8000/docs)
- [ ] Frontend loads without console errors
- [ ] Can create account (signup flow)
- [ ] Can login
- [ ] Search works (calls `/search/semantic`)
- [ ] Recommendations load on homepage
- [ ] Profile page shows stats

### Debug API Calls
Open browser console → Network tab → Look for XHR requests to `/api/v1/*`

---

## 6. Load Initial Data

### Option A: Use Jikan API (Live Data)
The app will fetch anime data on-demand from MyAnimeList via Jikan API.

### Option B: Seed Database (Recommended for Development)
```bash
# From backend directory
python scripts/seed_database.py
```

This will:
- Fetch top 100 anime from MAL
- Generate embeddings
- Populate Supabase

---

## Common Issues

### 1. "Connection to Supabase failed"
- ✅ Check SUPABASE_SERVICE_KEY is correct (not anon key)
- ✅ Verify project URL has `https://`
- ✅ Check Supabase project is not paused (free tier auto-pauses after 1 week inactivity)

### 2. "Module not found: @/lib/api-client"
- ✅ Run `npm install` in frontend folder
- ✅ Restart Next.js dev server

### 3. "Redis connection refused"
- ✅ Start Redis: `docker-compose up redis -d`
- ✅ Check port 6379 is not in use

### 4. Frontend shows CORS errors
- ✅ Check `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`
- ✅ Restart backend server

### 5. "Alembic can't connect to database"
- ✅ You're using the sync pooler (port 6543) - check config.py `database_url_sync`
- ✅ Service key has correct permissions

---

## Feature Flags

Control which ML features are enabled in `.env`:

```bash
# Heavy features (offload to Modal later)
ENABLE_IMAGE_SEARCH=false  # Requires CLIP model
ENABLE_GNN=false           # Requires trained GNN
ENABLE_BERT4REC=false      # Requires trained BERT4Rec

# Always enabled
ENABLE_RECOMMENDATIONS=true  # Content-based filtering
```

---

## Project Structure

```
anivibe-dev/
├── app/                    # FastAPI backend
│   ├── api/v1/            # API routes
│   ├── core/              # Database, auth, config
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # ML services
│       ├── bert4rec_service.py
│       ├── collaborative_filtering.py
│       ├── content_based.py
│       ├── explainability.py
│       ├── gnn_recommender.py
│       ├── semantic_search.py
│       └── vector_search.py
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/          # Pages (Next.js 14 app router)
│   │   ├── components/   # React components
│   │   ├── hooks/        # React Query hooks
│   │   ├── lib/          # API client, utils
│   │   └── types/        # TypeScript types
│   └── public/
├── alembic/              # Database migrations
├── models/               # Trained ML models
├── logs/                 # Application logs
├── docker-compose.yml    # Redis only
├── requirements.txt      # Python dependencies
└── config.py            # Backend configuration
```

---

## Future Features (Documented, Not Implemented)

### Atlas (3D Anime Network)
- **Route:** `/api/v1/atlas`
- **Status:** Placeholder with mock data
- **Frontend:** Page exists but not functional
- **Todo:** Implement GNN clustering → UMAP projection → Three.js rendering

### Analytics Dashboard
- **Route:** `/api/v1/analytics`  
- **Status:** Backend implemented ✅
- **Frontend:** Integrated in profile page ✅
- **Shows:** Genre distribution, watch time heatmap, user stats

---

## Deployment

### Backend (Railway/Render)
```bash
# Set environment variables in Railway dashboard
# Deploy from main branch
```

### Frontend (Vercel)
```bash
vercel deploy
# Add environment variables in Vercel dashboard
```

### Redis (Upstash)
Use Upstash Redis for production (free tier available)

---

## Development Workflow

1. **Make Changes**
   - Backend: Code auto-reloads with `--reload`
   - Frontend: Hot Module Replacement (HMR)

2. **Database Changes**
   ```bash
   # Generate migration
   alembic revision --autogenerate -m "description"
   
   # Apply migration
   alembic upgrade head
   ```

3. **Test API Changes**
   - Use Swagger UI: http://localhost:8000/docs
   - Or use frontend to test integration

4. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat: description"
   git push origin main
   ```

---

## Support

- **Issues:** [GitHub Issues](https://github.com/msrishav-28/anivibe-dev/issues)
- **Docs:** This file + inline code comments
- **API Docs:** http://localhost:8000/docs (when running)

---

## What Changed (Jan 2026 Refactoring)

✅ **Removed:**
- Local PostgreSQL (now Supabase only)
- MongoDB (embeddings in pgvector)
- Celery task queue (APScheduler for background jobs)
- MLflow (model tracking deferred)
- Docker containers for databases

✅ **Added:**
- Complete API client (`frontend/src/lib/api-client.ts`)
- TypeScript types for all API responses
- Pure Supabase configuration
- Environment file templates

✅ **Cleaned:**
- 4MB of unused frontend dependencies (D3, Plotly, AnimeJS)
- Orphaned backend packages (Celery, MLflow)
- Kept Three.js (your brand identity!)

---

**Ready to build?** Start with Step 2 (Supabase setup) 🚀

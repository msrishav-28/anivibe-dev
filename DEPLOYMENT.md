# 🚀 AniVibe Deployment Guide

## Architecture Overview

```
Vercel (Frontend) → Render (Backend) → Supabase (Database)
                         ↓
                    Modal (ML Models)
```

---

## 1️⃣ Supabase (Database) - DEPLOY FIRST

### Already Done ✅
Your Supabase project should already be set up. Just note down:

```
Project URL: https://xxxxx.supabase.co
Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Service Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Run Migrations
1. Go to Supabase Dashboard → SQL Editor
2. Run migration files from `alembic/versions/`
3. Or use Alembic locally:
   ```bash
   alembic upgrade head
   ```

---

## 2️⃣ Render (Backend API)

### Step 1: Create Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Deploy from Blueprint
1. Click **New** → **Blueprint**
2. Connect your `anivibe-dev` repo
3. Render auto-detects `render.yaml`
4. Click **Apply**

### Step 3: Set Environment Variables
Go to your service → **Environment** → Add:

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
GEMINI_API_KEY=your-gemini-key
```

### Step 4: Verify Deployment
- Wait 2-3 minutes for build
- Visit: `https://anivibe-backend.onrender.com/health`
- Should return: `{"status": "healthy"}`

### Step 5: Note Backend URL
```
https://anivibe-backend.onrender.com
```
You'll need this for Vercel.

---

## 3️⃣ Modal (ML Models) - OPTIONAL (Start without it)

**Skip this initially.** Deploy Modal later when you need GPU features.

### When Ready:

#### Step 1: Install Modal CLI
```bash
pip install modal
modal setup  # Login with GitHub
```

#### Step 2: Add Secrets
```bash
modal secret create supabase-credentials \
  SUPABASE_URL=https://xxxxx.supabase.co \
  SUPABASE_SERVICE_KEY=your-service-key
```

#### Step 3: Deploy
```bash
modal deploy modal_app.py
```

You'll get URLs like:
```
https://your-workspace--anivibe-ml-clip-image-search.modal.run
https://your-workspace--anivibe-ml-semantic-search.modal.run
```

#### Step 4: Update Backend
Add Modal URL to Render environment:
```bash
ML_SERVICE_URL=https://your-workspace--anivibe-ml.modal.run
ENABLE_IMAGE_SEARCH=true
```

---

## 4️⃣ Vercel (Frontend)

### Step 1: Install Vercel CLI
```bash
npm i -g vercel
```

### Step 2: Login
```bash
vercel login
```

### Step 3: Deploy from Frontend Directory
```bash
cd frontend
vercel
```

Follow prompts:
- Link to existing project? **No**
- Project name? **anivibe**
- Directory? **./frontend** (or just `.` if already in frontend/)
- Override settings? **No**

### Step 4: Set Environment Variables
```bash
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://anivibe-backend.onrender.com/api/v1

vercel env add NEXT_PUBLIC_SUPABASE_URL
# Enter: https://xxxxx.supabase.co

vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY  
# Enter: your-anon-key
```

**Or** add in Vercel Dashboard:
1. Go to project → Settings → Environment Variables
2. Add all `NEXT_PUBLIC_*` variables
3. Set for: Production, Preview, Development

### Step 5: Deploy Production
```bash
vercel --prod
```

### Step 6: Get Your URL
```
https://anivibe.vercel.app
```

---

## 5️⃣ Update CORS (IMPORTANT)

### Backend (Render)
Update environment variable:
```bash
CORS_ORIGINS=https://anivibe.vercel.app,https://www.anivibe.com
```

### Redeploy
Render auto-redeploys when you change env vars.

---

## 6️⃣ Custom Domain (Optional)

### Vercel
1. Buy domain (Namecheap, Cloudflare, etc.)
2. Vercel Dashboard → Domains → Add Domain
3. Update DNS records as instructed

### Example:
```
www.anivibe.com → anivibe.vercel.app (CNAME)
anivibe.com → 76.76.21.21 (A Record)
```

---

## 🔍 Verify Deployment

### Checklist
- [ ] Supabase migrations ran successfully
- [ ] Render backend: `https://your-backend.onrender.com/health` returns `{"status": "healthy"}`
- [ ] Render backend: `https://your-backend.onrender.com/docs` shows Swagger UI
- [ ] Vercel frontend loads without errors
- [ ] Frontend can call backend (check Network tab)
- [ ] Three.js particle background renders
- [ ] Search works
- [ ] Can create account
- [ ] Can login
- [ ] Recommendations load

---

## 💰 Cost Breakdown

### Free Tier (Start Here)
| Service | Plan | Limits | Cost |
|---------|------|--------|------|
| **Supabase** | Free | 500MB DB, 1GB storage, 2GB bandwidth | $0 |
| **Render** | Free | 512MB RAM, sleeps after 15min idle | $0 |
| **Vercel** | Hobby | 100GB bandwidth, unlimited sites | $0 |
| **Modal** | Free | $30 free credits/month | $0* |
| **Total** | | | **$0/month** |

*Modal charges $0.00015/sec for T4 GPU. $30 credit = ~56 hours GPU time.

### Production (Recommended)
| Service | Plan | Specs | Cost |
|---------|------|-------|------|
| **Supabase** | Pro | 8GB DB, 100GB storage, 250GB bandwidth | $25/mo |
| **Render** | Starter | 512MB RAM, always on | $7/mo |
| **Vercel** | Pro | 1TB bandwidth, analytics | $20/mo |
| **Modal** | Pay-as-go | Only pay for GPU usage | ~$10/mo |
| **Total** | | | **~$62/month** |

---

## 🐛 Troubleshooting

### Render Backend Won't Start
**Error:** `Connection to Supabase failed`
- ✅ Check `SUPABASE_SERVICE_KEY` is set correctly
- ✅ Verify Supabase project is not paused
- ✅ Check Render logs: Dashboard → Logs

### Vercel CORS Errors
**Error:** `CORS policy blocked`
- ✅ Add Vercel URL to `CORS_ORIGINS` in Render
- ✅ Redeploy backend
- ✅ Clear browser cache

### Modal Functions Timing Out
- ✅ Increase timeout in `modal_app.py` (max 900s)
- ✅ Check Modal logs: `modal app logs anivibe-ml`
- ✅ Verify secrets are set: `modal secret list`

### Render Free Tier Sleeping
**Problem:** First request takes 30 seconds
- ✅ Upgrade to Starter plan ($7/mo) for always-on
- ✅ Or use cron-job.org to ping `/health` every 14 minutes

---

## 📊 Monitoring

### Render
- Dashboard → Metrics (CPU, RAM, requests)
- Logs → Real-time logs

### Vercel  
- Analytics (available on Pro plan)
- Deployment logs
- Function logs (for API routes)

### Modal
```bash
modal app logs anivibe-ml
modal app stats anivibe-ml
```

### Supabase
- Dashboard → Database → Usage
- Monitor query performance
- Check connection pooling stats

---

## 🔄 CI/CD (Auto-Deploy on Push)

### Already Configured! ✅

**Vercel:** Auto-deploys on every push to `main`

**Render:** Auto-deploys on every push to `main`

**Modal:** Manual deploy with `modal deploy`

---

## 🚀 Deployment Order

**First Time:**
1. ✅ Supabase (already done)
2. Deploy Render backend
3. Deploy Vercel frontend
4. Update CORS
5. Test everything
6. *(Later)* Add Modal for GPU features

**Updates:**
- Push to GitHub → Auto-deploys to Vercel & Render
- Modal: Run `modal deploy` manually

---

## 🎯 Next Steps After Deployment

1. **Test thoroughly**
   - Create test account
   - Try all features
   - Check error tracking

2. **Add monitoring**
   - Set up Sentry for error tracking
   - Add analytics (Plausible/PostHog)
   - Set up uptime monitoring (UptimeRobot)

3. **Performance**
   - Enable Vercel Edge Caching
   - Optimize images with `next/image`
   - Add Redis caching in Render

4. **SEO**
   - Add meta tags
   - Generate sitemap
   - Set up Google Search Console

---

**Ready to deploy?** Start with Step 2 (Render) 🚀

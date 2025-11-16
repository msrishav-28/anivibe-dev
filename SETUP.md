# AniVibe Setup Guide

Complete guide to set up AniVibe backend from scratch.

## Prerequisites

### Required Software
- Python 3.11+
- Docker Desktop (for containerized setup)
- PostgreSQL 15+ (if running locally)
- MongoDB 7+ (if running locally)
- Redis 7+ (if running locally)
- Git

### Optional
- NVIDIA GPU with CUDA (for faster ML inference)
- Make (for using Makefile commands)

## Installation Methods

### Method 1: Docker (Recommended for Quick Start)

**Step 1: Clone the repository**
```bash
git clone https://github.com/yourusername/AniVibe.git
cd AniVibe
```

**Step 2: Configure environment**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Required: SECRET_KEY, database passwords
# Optional: GEMINI_API_KEY, MAL_CLIENT_ID, ANILIST_CLIENT_ID
```

**Step 3: Start services**
```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Step 4: Access the application**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MLflow: http://localhost:5000

**Step 5: Create initial data**
```bash
# Run database setup (creates admin user and genres)
docker-compose exec backend python scripts/setup_database.py
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@anivibe.com`

⚠️ **Important**: Change the admin password after first login!

---

### Method 2: Local Development Setup

**Step 1: Clone and setup Python environment**
```bash
git clone https://github.com/yourusername/AniVibe.git
cd AniVibe

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Step 2: Setup databases**

Install and start PostgreSQL, MongoDB, and Redis locally or use Docker:

```bash
# Using Docker for databases only
docker run -d --name anivibe_postgres \
  -e POSTGRES_USER=anivibe \
  -e POSTGRES_PASSWORD=anivibe_password \
  -e POSTGRES_DB=anivibe_db \
  -p 5432:5432 \
  postgres:15-alpine

docker run -d --name anivibe_mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=anivibe \
  -e MONGO_INITDB_ROOT_PASSWORD=anivibe_password \
  -p 27017:27017 \
  mongo:7

docker run -d --name anivibe_redis \
  -p 6379:6379 \
  redis:7-alpine
```

**Step 3: Configure environment**
```bash
cp .env.example .env
# Edit .env with your local database configurations
```

**Step 4: Initialize database**
```bash
# Create tables and initial data
python scripts/setup_database.py

# Or use Alembic migrations
alembic upgrade head
```

**Step 5: Run the application**
```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Make
make dev
```

---

## Configuration

### Environment Variables

#### Application Settings
```bash
APP_NAME=AniVibe
ENVIRONMENT=development  # or production
DEBUG=True
SECRET_KEY=your-super-secret-key-min-32-chars  # REQUIRED
```

#### Database Configuration
```bash
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=anivibe
POSTGRES_PASSWORD=your_secure_password  # REQUIRED
POSTGRES_DB=anivibe_db

# MongoDB
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USER=anivibe
MONGODB_PASSWORD=your_secure_password  # REQUIRED
MONGODB_DB=anivibe_embeddings

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=  # Optional
```

#### ML Model Configuration
```bash
MODEL_CACHE_DIR=./models/cache
EMBEDDINGS_DIR=./data/embeddings
FAISS_INDEX_PATH=./data/faiss_indexes

# CLIP
CLIP_MODEL_NAME=ViT-B-32
CLIP_PRETRAINED=openai

# BERT
SBERT_MODEL_NAME=all-mpnet-base-v2  # or all-MiniLM-L6-v2 for lighter

# GPU
USE_GPU=True  # Set to False if no GPU available
GPU_DEVICE=cuda:0
```

#### External API Keys (Optional but Recommended)
```bash
# Gemini AI for LLM query parsing
GEMINI_API_KEY=your_gemini_api_key

# MyAnimeList OAuth
MAL_CLIENT_ID=your_mal_client_id
MAL_CLIENT_SECRET=your_mal_client_secret

# AniList OAuth
ANILIST_CLIENT_ID=your_anilist_client_id
ANILIST_CLIENT_SECRET=your_anilist_client_secret
```

---

## Data Setup

### Option 1: Using Sample Data (Quick Test)

```bash
# Download sample dataset
python scripts/download_sample_data.py

# This will create:
# - data/raw/anime_sample.csv (100 anime)
# - data/raw/ratings_sample.csv (1000 ratings)
```

### Option 2: Full Dataset from MAL/AniList

```bash
# Fetch full dataset (takes ~30 minutes)
python scripts/fetch_mal_data.py --limit 10000

# Fetch anime posters
python scripts/download_anime_posters.py

# Generate embeddings (requires ~8GB RAM)
python scripts/generate_embeddings.py

# Create FAISS indexes
python scripts/create_faiss_indexes.py
```

---

## Verification

### 1. Check Services
```bash
# Using Docker
docker-compose ps

# All services should be "Up" and "healthy"
```

### 2. Test API
```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### 3. Test Authentication
```bash
# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=TestPass123"
```

### 4. Test ML Models
```bash
# This will download models on first run (may take a few minutes)
python -c "
from app.core.ml_models import init_ml_models
import asyncio
asyncio.run(init_ml_models())
print('✅ ML models loaded successfully')
"
```

---

## Troubleshooting

### Issue: Database connection failed

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Recreate database
docker-compose down -v
docker-compose up -d postgres
```

### Issue: ML models not loading

**Solution:**
```bash
# Check if models directory exists
mkdir -p models/cache

# Clear cache and re-download
rm -rf models/cache/*
python -c "from app.core.ml_models import init_ml_models; import asyncio; asyncio.run(init_ml_models())"
```

### Issue: Out of memory

**Solution:**
```bash
# Use lighter models in .env
SBERT_MODEL_NAME=all-MiniLM-L6-v2  # 384-dim instead of 768-dim
CLIP_MODEL_NAME=ViT-B-32  # Instead of ViT-L-14

# Reduce batch size
BATCH_SIZE=8  # Instead of 32
```

### Issue: Port already in use

**Solution:**
```bash
# Change ports in docker-compose.yml
# Or stop conflicting services
docker stop $(docker ps -q)  # Stop all Docker containers
```

---

## Development Workflow

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_recommendations.py -v
```

### Code Quality
```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint
flake8 app/ --max-line-length=120

# Type checking
mypy app/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Production Deployment

### Security Checklist
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Change all database passwords
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Enable rate limiting
- [ ] Review CORS settings

### Environment Variables for Production
```bash
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=$(openssl rand -hex 32)
# Use strong passwords for all databases
```

### Docker Production Build
```bash
# Build for production
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

## Next Steps

1. **Populate Database**: Run data fetching scripts to get anime data
2. **Generate Embeddings**: Create CLIP and BERT embeddings for all anime
3. **Build FAISS Indexes**: Enable fast similarity search
4. **Setup Frontend**: Deploy React frontend (see frontend/README.md)
5. **Configure OAuth**: Setup MAL and AniList authentication
6. **Monitor**: Setup Prometheus and Grafana for monitoring

---

## Support

- **Documentation**: See [docs/](docs/) folder
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: support@anivibe.com

---

## Quick Commands Reference

```bash
# Start everything
make start

# Stop everything
make stop

# View logs
docker-compose logs -f

# Database setup
make db-setup

# Run migrations
make migrate

# Development server
make dev

# Run tests
make test

# Format code
make format

# Clean cache
make clean
```

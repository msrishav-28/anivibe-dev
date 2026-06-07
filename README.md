# AniVibe: Neo-Tokyo Edition

<div align="center">

![AniVibe Banner](https://img.shields.io/badge/AniVibe-Neo--Tokyo_Protocol-8B5CF6?style=for-the-badge)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.1-black.svg?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC.svg?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)

[![Neon](https://img.shields.io/badge/Neon-PostgreSQL_+_pgvector-00E599.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
[![pgvector](https://img.shields.io/badge/pgvector-Vector_Search-2CA5E0.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**AI-Powered Anime Discovery & "Ethereal" Watchlist Platform**

</div>

---

## Project DNA: "It's Not a Database, It's a World"

**AniVibe** is not just another anime tracking list. It is a **$50,000 valued** "Digital Dark Academia" experience designed to immerse users in a **Neo-Tokyo** interface.

*   **Aesthetic:** Deep AMOLED Black (`#050505`), Film Grain overlays, and Holographic UI cards.
*   **Physics:** Framer Motion "Kinetic Snappiness" (Spring 400/25).
*   **Discoverability:** We don't use keywords. We use **Vectors**.

---

## Production Readiness Status

> [!IMPORTANT]
> AniVibe is being hardened for production. The source of truth is
> [`PRODUCTION_READINESS.md`](PRODUCTION_READINESS.md). Current AI behavior should be treated as
> baseline or beta unless that tracker marks it as production.
> *   **Semantic Search**: Baseline pgvector/SBERT path.
> *   **Visual Search**: Beta Modal/CLIP path; requires generated CLIP embeddings.
> *   **Recommendations**: Baseline content/collaborative path; GNN/BERT4Rec are not production.

### 1. Semantic Vibe Search
Type: *"A cyberpunk city with rain and neon lights"*
*   **Tech**: **SBERT (Sentence-BERT)** generates a 384-dimensional vector from your query.
*   **Vector DB**: Queries **Neon/Postgres pgvector** using cosine distance (`<=>`) against versioned embeddings.

### 2. Reverse Image Search
Upload a screenshot.
*   **Tech**: **OpenAI CLIP (ViT-B-32)** runs on a GPU (via Modal).
*   **Process**: Converts image pixels -> 512-dim embedding -> Finds nearest anime poster in the vector space.

### 3. Hybrid Recommendations
*   **Collaborative Filtering**: "Users who liked X also liked Y."
*   **Content-Based**: Genre/Tag matching.
*   **Hidden Gems**: A specialized algorithm that mathematically penalizes "Popularity" to surface high-rated, under-watched masterpieces.

---

## Architecture

```mermaid
graph TD
    Client(Next.js Frontend) -->|REST API| API(FastAPI Backend)
    
    subgraph "Infrastructure"
        API -->|Data| DB[(Neon PostgreSQL)]
        Client -->|Auth| Clerk(Clerk)
        API -->|JWT Verification| Clerk
        DB -->|Vector Search| PGVector(pgvector Ext)
        API -->|Cache| Redis(Redis 7)
    end
    
    subgraph "AI Microservices"
        API -->|RPC| Modal(Modal GPU Service)
        Modal -->|CLIP Inference| GPU[NVIDIA T4]
    end
```

### Tech Stack Breakdown
| Component | Technology | Why? |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 14 + Tailwind** | Server-side rendering for SEO, Framer Motion for premium feel. |
| **Backend** | **FastAPI (Python)** | High-performance async API, native Pydantic integration. |
| **Database** | **Neon Postgres** | Managed PostgreSQL with `pgvector`, branching, and pooled connections. |
| **Auth** | **Clerk** | Hosted auth with JWT verification in the backend. |
| **Storage** | **Cloudflare R2** | S3-compatible media storage for avatars and future poster assets. |
| **Vectors** | **SBERT + CLIP** | State-of-the-art semantic text and image understanding. |
| **Infra** | **Docker + Render** | Portable, distinct containerization. |

---

## Quick Start

### Prerequisites
*   Docker & Docker Compose
*   Neon Postgres database with pgvector
*   Clerk application
*   Cloudflare R2 bucket for uploads
*   Modal account (optional for image search)

### 1. Environment Setup
```bash
cp .env.example .env
```
Fill in `DATABASE_URL`, `DATABASE_MIGRATION_URL`, Clerk, R2, Redis, and optional Modal credentials.

### 2. Run with Docker
**Standard Mode (With Local ML):**
```bash
docker-compose up -d --build
```
**Lightweight Mode (Cloud-Only):**
If you want to run like the free-tier production setup:
```bash
pip install -r requirements-api.txt
uvicorn app.main:app
```
*   **Frontend**: `http://localhost:3000`
*   **Backend**: `http://localhost:8000`
*   **Docs**: `http://localhost:8000/docs`

### 3. Initialize Vectors
The app needs the `vector` extension.
```bash
# Run Alembic migrations to set up schema and vector functions
docker-compose exec backend alembic upgrade head
```

---

## Testing
We maintain a strict testing culture for reliability.

```bash
# Run backend tests
docker-compose exec backend pytest
```

---

## Project Structure

```
AniVibe/
├── app/                  # FastAPI Backend
│   ├── api/v1/           # Endpoints (Auth, Anime, Search)
│   ├── core/             # Config, Security, Database
│   ├── models/           # SQLAlchemy Models (with pgvector)
│   └── services/         # Business Logic (Recommendations, Search)
├── frontend/             # Next.js Frontend
│   ├── src/components/   # Neo-Tokyo UI Components
│   └── src/app/          # Pages & Routing
├── modal_app.py          # AI Microservice (CLIP/GPU)
├── alembic/              # Database Migrations
└── docker-compose.yml    # Orchestration
```

---

## License
**MIT License**. Built for the "Ethereal Archive" initiative.

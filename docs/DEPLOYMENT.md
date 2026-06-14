# Deployment Guide

CoverageIQ AI is containerized for seamless remote deployment.

## Prerequisites
- Docker Engine
- A provisioned PostgreSQL Database (we recommend Neon).
- Groq or Google Gemini API Keys.

## Architecture

The project splits into:
1. **Frontend**: Standalone Vite bundle served statically or via Node.
2. **Backend**: FastAPI web server relying on an external DB.

## Docker Deployment (Single Node)

The simplest deployment utilizes the bundled `docker-compose.yml`.

```bash
# 1. Clone the repository
git clone https://github.com/sujith0466/CoverageIQ_AI.git
cd CoverageIQ_AI

# 2. Populate Environments
cp backend/.env.example backend/.env
# Edit backend/.env with your production database URL and LLM keys.

# 3. Spin up
docker-compose up -d --build
```

## Hosted Provider Suggestions

### Render (Backend)
1. Fork to GitHub.
2. Create a **Web Service** on Render pointing to the `/backend` folder.
3. Configure the Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`.
4. Provide the `.env` variables in the dashboard.

### Vercel (Frontend)
1. Import the repository into Vercel.
2. Set the Root Directory to `frontend`.
3. Framework Preset: `Vite`.
4. Add environment variable `VITE_API_URL` pointing to your Render backend domain.

### Neon (Database)
1. Provision a Serverless Postgres cluster.
2. Copy the `postgresql://` string.
3. Append `+asyncpg` to the driver format in your backend `.env` (e.g., `postgresql+asyncpg://...`).

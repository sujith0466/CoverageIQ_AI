# CoverageIQ AI

Enterprise Coverage Intelligence & Autonomous Test Generation Platform

## Project Structure

- `frontend/`: React + Vite + Tailwind CSS frontend
- `backend/`: FastAPI + SQLAlchemy + Neon PostgreSQL backend

## Setup

1. Copy `.env.example` to `.env` and fill in your Neon database connection string.
   ```bash
   cp .env.example .env
   ```

2. Start the development environment using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. The backend API will be available at `http://localhost:8000` and the frontend at `http://localhost:5173`.

## Migrations

To generate and apply database migrations using Alembic:

```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

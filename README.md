# this_code_is_made_by_copilot
# TaskMaster

Simple task manager API built with FastAPI, SQLAlchemy (async), and JWT auth.

## Quickstart

1. Install dependencies:
   - Using Poetry: `poetry install`
2. Run locally:
   - `uvicorn app.main:app --reload`
3. API docs:
   - Open `http://localhost:8000/docs`

## Docker
- Build: `docker build -t taskmaster .`
- Run: `docker run -p 8000:8000 taskmaster`

## Notes
- This repo uses SQLite for demo. Replace with Postgres in production and use Alembic for migrations.

# Notes Backend (FastAPI)

A simple notes backend providing CRUD operations for notes.

## Features
- FastAPI with automatic OpenAPI docs
- SQLAlchemy (SQLite by default) for persistence
- Clean architecture (routers, services, repositories, models, schemas)
- Configurable via `.env`

## Configuration
Copy `.env.example` to `.env` and adjust as needed:
```
cp .env.example .env
```

Available variables:
- `DATABASE_URL` (default `sqlite:///./notes.db`)
- `CORS_ALLOW_ORIGINS` (default `*`)

## Running
Install dependencies and start with uvicorn:
```
pip install -r requirements.txt
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Open docs at: http://localhost:8000/docs

## API Endpoints
- GET `/` - health check
- GET `/api/v1/notes` - list notes
- POST `/api/v1/notes` - create note
- GET `/api/v1/notes/{note_id}` - retrieve note
- PUT `/api/v1/notes/{note_id}` - update note
- PATCH `/api/v1/notes/{note_id}` - partial update
- DELETE `/api/v1/notes/{note_id}` - delete note

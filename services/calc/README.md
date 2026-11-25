# Calculation service

Stateless Python service (FastAPI): birth data in, chart / dasha / transit JSON out. No network calls at runtime, no database. Rules for this folder are in `CLAUDE.md`.

## Setup (Windows PowerShell, from `services/calc/`)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Requires Python 3.11 or newer.

## Commands

| What | Command |
|---|---|
| Run tests | `.\.venv\Scripts\python.exe -m pytest` |
| Lint | `.\.venv\Scripts\python.exe -m ruff check .` |
| Run the service | `.\.venv\Scripts\python.exe -m uvicorn calc.main:app --reload` |

Health check: `GET http://127.0.0.1:8000/health` returns `{"status": "ok", "engine_version": "..."}`.
OpenAPI docs: `http://127.0.0.1:8000/docs`.

## Status
M0 task T1 (scaffolding) only. No calculations exist yet.

# Calculation service

Stateless Python service (FastAPI): birth data in, chart / dasha / transit JSON out. No network calls at runtime, no database. Rules for this folder are in `CLAUDE.md`.

## Setup (Windows PowerShell, from `services/calc/`)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Requires Python 3.11 or newer.

Download the ephemeris kernel once (about 32 MB, not committed):

```powershell
.\.venv\Scripts\python.exe scripts/fetch_ephemeris.py
```

The service refuses to start without it and never downloads at runtime. Set `CALC_EPHEMERIS_PATH` to use a kernel stored elsewhere.

## Commands

| What | Command |
|---|---|
| Run tests | `.\.venv\Scripts\python.exe -m pytest` |
| Lint | `.\.venv\Scripts\python.exe -m ruff check .` |
| Run the service | `.\.venv\Scripts\python.exe -m uvicorn calc.main:app --reload` |

Health check: `GET http://127.0.0.1:8000/health` returns `{"status": "ok", "engine_version": "..."}`.
OpenAPI docs: `http://127.0.0.1:8000/docs`.

## Status
M0 tasks T1 (scaffolding) and T2 (ephemeris loading) done. No calculations exist yet.

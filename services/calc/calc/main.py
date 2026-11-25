from contextlib import asynccontextmanager

from fastapi import FastAPI

from calc.ephemeris import get_ephemeris
from calc.version import ENGINE_VERSION


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_ephemeris()  # fail fast at startup if the kernel is missing
    yield


app = FastAPI(title="Calculation service", version=ENGINE_VERSION, lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    eph = get_ephemeris()
    return {
        "status": "ok",
        "engine_version": ENGINE_VERSION,
        "ephemeris": {
            "kernel": eph.kernel_name,
            "start": eph.start.isoformat(),
            "end": eph.end.isoformat(),
        },
    }

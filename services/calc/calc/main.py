from fastapi import FastAPI

from calc.version import ENGINE_VERSION

app = FastAPI(title="Calculation service", version=ENGINE_VERSION)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "engine_version": ENGINE_VERSION}

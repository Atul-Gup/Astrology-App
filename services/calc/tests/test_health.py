import re

from fastapi.testclient import TestClient

from calc.main import app
from calc.version import ENGINE_VERSION

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_includes_engine_version():
    body = client.get("/health").json()
    assert body["engine_version"] == ENGINE_VERSION


def test_engine_version_is_semver_like():
    assert re.fullmatch(r"\d+\.\d+\.\d+", ENGINE_VERSION)


def test_openapi_docs_available():
    assert client.get("/openapi.json").status_code == 200

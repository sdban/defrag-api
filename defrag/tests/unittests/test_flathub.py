from fastapi.testclient import TestClient
from defrag import app
from defrag.modules.flathub import get_all_apps
import pytest

client = TestClient(app)


@pytest.mark.asyncio
async def test_apps():
    res = await get_all_apps()
    assert res


def test_apps_handler():
    response = client.get("/flathub/apps?category=AudioVideo")
    assert response.status_code == 200
    results = response.json()["results"]
    assert results

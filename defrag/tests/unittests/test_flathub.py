from fastapi.testclient import TestClient
from starlette.responses import Response
from defrag import app
from defrag.modules.flathub import get_apps

client = TestClient(app)


def test_apps():
    res = client.get("/flathub/apps")
    assert res


def test_apps_handler():
    response = client.get("/flathub/apps?category=AudioVideo")
    assert response.status_code == 200
    results = response.json()["results"]
    assert results
    

def test_search_handler():
    response = client.get("/flathub/apps/search?keywords=youtube")
    assert response.status_code == 200
    results = response.json()
    print(results)

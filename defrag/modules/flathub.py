from typing import List, Optional
from pydantic.main import BaseModel
from defrag.modules.helpers.requests import Req
from defrag.modules.helpers import Query, QueryResponse
from defrag import app

__MOD_NAME__ = "flathub"

base_url = "https://flathub.org/api/v1/apps"
categories = [
    "AudioVideo",
    "Development",
    "Education",
    "Game",
    "Graphics",
    "Network",
    "Office",
    "Science",
    "System",
    "Utility"
]


class FlatHubEntry(BaseModel):
    flatpakAppId: str
    name: str
    summary: str
    currentReleaseVersion: Optional[str]
    currentReleaseDate: str
    iconDesktopUrl: Optional[str]
    iconMobileUrl: Optional[str]
    inStoreSinceDate: Optional[str]


async def list_apps(category: Optional[str]) -> List[FlatHubEntry]:
    url = f"{base_url}/category/{category}" if (
        category and category in categories) else base_url
    async with Req(url) as response:
        res = await response.json()
        return [FlatHubEntry(**v) for v in res] if res else []


@app.get(f"/{__MOD_NAME__}/apps")
async def get_all_apps(category: Optional[str] = None) -> QueryResponse:
    query = Query(service=__MOD_NAME__)
    results = await list_apps(category)
    return QueryResponse(query=query, results=results, results_count=len(results))

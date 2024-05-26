import fastapi
from scraper import scrape_menu_by_oranization_id
from fastapi_cache.decorator import cache

app = fastapi.FastAPI()

@cache(expire=3600)
@app.get("/")
async def scrape_yandex_menu_by_id(id: int):
    return await scrape_menu_by_oranization_id(id)



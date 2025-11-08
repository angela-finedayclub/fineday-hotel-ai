from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from playwright.sync_api import sync_playwright
from backend.gpt_matcher import match_hotel_name
from backend.playwright_utils import search_hotels

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.post("/api/search")
async def search_hotels_api(request: Request):
    p = await request.json()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        results = search_hotels(page, p["city"], p["hotel"], p["checkin"], p["checkout"], p["people"])
        browser.close()
    final, site, price = match_hotel_name(p["hotel"], results)
    return {"results": final, "lowest_site": site, "lowest_price": price}

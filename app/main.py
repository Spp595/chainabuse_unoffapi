from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


class InputData(BaseModel):
    value: str


class OutputData(BaseModel):
    reports: str
    types: list[str]


proxy_host = os.getenv("PROXY_HOST")
proxy_user = os.getenv("PROXY_USER")
proxy_pass = os.getenv("PROXY_PASS")

if proxy_user and proxy_pass:
    proxy = {
        "server": (proxy_host),
        "username": (proxy_user),
        "password": (proxy_pass)}
else:
    proxy = {"server": (proxy_host)}


@app.post("/checkwallet", response_model=OutputData)
async def process_data(data: InputData):
    async with async_playwright() as p:
        ua = UserAgent()
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        print(ua.chrome)
        if proxy_host:

            page = await browser.new_page(user_agent=ua.chrome, proxy=proxy)
        else:
            page = await browser.new_page(user_agent=ua.chrome)
        images = [".png", ".svg", ".jpg", ".jpeg", ".webp"]

        async def block_images(route, request):
            url = request.url.lower()
            if any(url.endswith(ext) for ext in images):
                await route.abort()
            else:
                await route.continue_()
        await page.route("**/*", block_images)

        url = f"https://www.chainabuse.com/address/{data.value}"

        await page.goto(url, wait_until="domcontentloaded")

        await page.wait_for_selector("h3.create-ResultsSection__results-title")
        await page.wait_for_selector("div.create-FilterTable")

        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, 'lxml')
    result_scam_tag = soup.find(
        "h3", class_="create-ResultsSection__results-title")
    if not result_scam_tag:
        raise HTTPException(
            status_code=404, detail="Result element not found on page")

    text = result_scam_tag.text
    if "No Reports" in text:
        return OutputData(reports="0", types=[])
    else:

        scam_index = text.find("Scam")
        text = text[:scam_index].strip()
        result_category_tag = soup.find_all(
            "div", class_="create-FilterTable__filter-option")
        types_scam = []
        for i in result_category_tag:
            type_scam = (i.find("p", class_="create-Text type-body-lg"))
            type_scam_count = i.find(
                "div",
                class_='create-Badge size-small variant-default '
                'create-FilterTable__num-reports'
            )
            types_scam.append(type_scam.text + " " + type_scam_count.text)
    return OutputData(reports=text,  types=types_scam)

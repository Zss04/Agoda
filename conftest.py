import pytest_asyncio
from playwright.async_api import async_playwright


@pytest_asyncio.fixture(scope="session")
async def search_url():
    return {"url": None}
        
@pytest_asyncio.fixture(scope="function")
async def browser():
    print("Launching browser")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        if browser is None:
            print(f"The browser:'{browser} did not load")
        yield browser
        await browser.close()

@pytest_asyncio.fixture(scope="function")
async def page_tuple(browser,search_url):
    print("Creating a new page")
    page = await browser.new_page()
    if page is None:
        print(f"The page:'{page} did not load")
    yield page, search_url
    await page.close()


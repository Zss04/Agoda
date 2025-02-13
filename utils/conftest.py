import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

@pytest_asyncio.fixture()
async def browser(scope="function"):
    print("Launching browser")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            if browser is None:
                print(f"The browser:'{browser} did not load")
            yield page
            yield browser
            await browser.close()
    except Exception as err: 
        print("Cannot launch browser")


@pytest_asyncio.fixture(scope="function")
async def page(browser):
    try:
        print("Creating a new page")
        page = await browser.new_page()
        if page is None:
            print(f"The page:'{page} did not load")
        yield page
        await page.close()
    except Exception as err: 
        print("Cannot launch browser")


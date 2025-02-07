import pytest
import pytest_asyncio
from playwright.async_api import async_playwright


@pytest_asyncio.fixture()
async def browser_and_page():
    print("Inside the function")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        yield page
        await browser.close()

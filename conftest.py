import pytest
import asyncio
import pytest_asyncio
import pytest_html
import os
from datetime import datetime
from playwright.async_api import async_playwright
import pytest_html.extras


@pytest_asyncio.fixture(scope="session")
async def search_url():
    """Fixture to provide a search URL."""
    return {"url": None}


@pytest_asyncio.fixture(scope="function")
async def browser():
    """Fixture to launch and manage the browser instance."""
    print("Launching browser")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        if browser is None:
            pytest.fail("The browser did not load.")
        yield browser
        await browser.close()


@pytest_asyncio.fixture(scope="function")
async def page_tuple(browser, search_url, request):
    print("Creating a new page")
    page = await browser.new_page()
    if page is None:
        pytest.fail("The page did not load.")
    yield page, search_url

    # After the test completes, take a screenshot
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = os.path.expanduser("~/Downloads/agoda/Reports/Images/")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(
            screenshot_dir, f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        print(f"Saving screenshot to: {screenshot_path}")
        await page.screenshot(path=screenshot_path)
        print(f"Setting screenshot_path: {screenshot_path}")
        request.node.screenshot_path = screenshot_path
        print(f"Saved screenshot to: {screenshot_path}")

    await page.close()
    
def pytest_html_report_title(report):
    """Hook to set the title of the HTML report."""
    module_name = "Agoda Flight Booking"
    report.title = f"Test Report: {module_name}"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        print(f"Report phase: {report.when}, Outcome: {report.outcome}, Failed: {report.failed}")
        item.rep_call = report

    if report.when == "teardown":
        if hasattr(item, "rep_call") and item.rep_call.failed:
            if hasattr(item, "screenshot_path"):
                screenshot_path = item.screenshot_path
                extras = getattr(report, "extras", [])
                if os.path.exists(screenshot_path):
                    print(f"appending screenshot to report with path {screenshot_path}")
                    extras.append(pytest_html.extras.image(screenshot_path))
                    item.rep_call.extras = extras
                print("Screenshot attached successfully!")
            else:
                print("screenshot_path not found on item")

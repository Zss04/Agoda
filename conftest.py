import pytest, pytest_asyncio
import pytest_html
import os
from datetime import datetime 
from playwright.async_api import async_playwright
import pytest_html.extras


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
async def page_tuple(browser, search_url, request):
    print("Creating a new page")
    page = await browser.new_page()
    if page is None:
        print(f"The page:'{page} did not load")
    
    # screenshot_dir = os.path.expanduser("~/Downloads/agoda/Reports/Images")
    # os.makedirs(screenshot_dir, exist_ok=True)

    # # Save screenshot path before closing page
    # screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    # request.node.screenshot_path = screenshot_path 

    yield page, search_url    
    # await page.screenshot(path=screenshot_path)  # Ensure screenshot before closing
    await page.close()

'''
def pytest_html_report_title (report):
    module_name = "Agoda Flight Booking"
    report.title = f"Test Report: {module_name}"


    
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call" :
        xfail = hasattr(report, "wasxfail")
        if not xfail:
            # only add additional html on failure
            extras.append(pytest_html.extras.html("<div>It failed lol</div>"))
            screenshot_path = getattr(item.node, "screenshot_path", None)
            if screenshot_path:
                extras.append(pytest_html.extras.image(screenshot_path))
        report.extras = extras
        '''
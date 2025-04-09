import pytest
import pytest_asyncio
import pytest_html
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright
import pytest_html.extras
from utils.logger_config import setup_logging
from test_data import test_parameters


# Set up logging at the module level
logger = setup_logging("conftest")

def pytest_addoption(parser):
    """Add command-line options for test parameters."""
    parser.addoption("--origin", action="store", default="LHE",
                    help="Use test parameters from test_data.py")
    parser.addoption("--destination", action="store", default="IST",
                    help="Use test parameters from test_data.py")
    parser.addoption("--adults", action="store", default=1,
                    help="Use test parameters from test_data.py")
    parser.addoption("--children", action="store", default=0,
                    help="Use test parameters from test_data.py")
    parser.addoption("--infants", action="store", default=0,
                    help="Use test parameters from test_data.py")
    parser.addoption("--cabin", action="store", default="Economy",
                    help="Use test parameters from test_data.py")  
    parser.addoption("--test-browser", action="store", default="chromium",
                     choices=["chromium", "firefox", "webkit"],
                     help="Specify the browser to run tests on (chromium, firefox, webkit)")

def pytest_generate_tests(metafunc):
    """
    Generate test parameters dynamically for all tests that need them.
    This function is called once for each test function.
    """
    # Check if the test function needs flight booking parameters
    if all(param in metafunc.fixturenames for param in 
        ["departure_airport", "arrival_airport", "adults", "children", "infants", "cabin"]):
    # Get parameters from the test data
        try:
            metafunc.parametrize(
                ["departure_airport", "arrival_airport", "adults", "children", "infants", "cabin"],
                test_parameters
            )
            logger.info(f"Parametrized {metafunc.function.__name__} with {len(test_parameters)} parameter sets")
        except Exception as e:
            logger.error(f"Error loading parameters: {e}")
    

@pytest_asyncio.fixture(scope="session")
async def search_url():
    """Provides a base URL dictionary for tests."""
    logger.info("Creating search_url fixture")
    return {"url": None}


@pytest_asyncio.fixture(scope="function")
async def browser(request):
    """Launches and manages a browser instance for each test."""
    browser_name = request.config.getoption("--test-browser")
    
    async with async_playwright() as p:
        if browser_name == "chromium":
            browser = await p.chromium.launch(headless=True)
            logger.info(f"Launching browser: {browser_name}")

        elif browser_name == "firefox":
            browser = await p.firefox.launch(headless=True)
            logger.info(f"Launching browser: {browser_name}")

        elif browser_name == "webkit":
            browser = await p.webkit.launch(headless=True)
            logger.info(f"Launching browser: {browser_name}")

        else:
            pytest.fail(f"Unsupported browser: {browser_name}")
        yield browser
        logger.info("Closing browser")
        await browser.close()


@pytest_asyncio.fixture(scope="function")
async def page_tuple(browser, search_url, request, create_screenshot_directory):
    """
    Creates a page for testing and handles cleanup.
    Takes screenshots on test failure.
    """
    logger.info(f"Creating new page for test: {request.node.name}")
    page = await browser.new_page()
    if page is None:
        logger.error("Failed to create new page")
        pytest.fail("The page did not load.")
    
    logger.info(f"Page created successfully: {page}")
    yield page, search_url
    
    # Take screenshot if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        logger.info(f"Test failed, capturing screenshot for: {request.node.name}")
        await capture_screenshot(page, request, create_screenshot_directory)
    else:
        logger.info(f"Test completed: {request.node.name}")
    
    logger.info("Closing page")
    await page.close()


@pytest.fixture(scope="session", autouse=True)
def create_screenshot_directory():
    """
    Create the screenshot directory at the start of the session.
    Clears any existing screenshots to avoid accumulation.
    """
   
    screenshot_dir = os.path.expanduser("~/Downloads/agoda/Reports/Images/")
    logger.info(f"Creating screenshot directory: {screenshot_dir}")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Clear any existing files in the directory
    file_count = 0
    for file in os.listdir(screenshot_dir):
        file_path = os.path.join(screenshot_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                file_count += 1
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
    
    logger.info(f"Cleared {file_count} existing screenshots from directory")
    return screenshot_dir


async def capture_screenshot(page, request, screenshot_dir):
    """Capture screenshot on test failure and add it to HTML report."""
    screenshot_path = os.path.join(
        screenshot_dir, f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
    )
    logger.info(f"Capturing screenshot to: {screenshot_path}")
    
    # Capture screenshot
    try:
        await page.screenshot(path=screenshot_path)
        logger.info("Screenshot captured successfully")
    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")
        return
    
    # Add to report if file exists
    if os.path.exists(screenshot_path):
        logger.info("Adding screenshot to HTML report")
        extras = getattr(request.node.rep_call, "extras", [])
        extras.append(pytest_html.extras.image(screenshot_path))
        request.node.rep_call.extras = extras
    else:
        logger.error(f"Screenshot file not found: {screenshot_path}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures test reports and stores them on the test item.
    Used to determine test status for screenshot capture.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Store the test reports on the test item for later use
    setattr(item, f"rep_{report.when}", report)
    
    # Log test status
    if report.when == "call":
        if report.passed:
            logger.info(f"Test PASSED: {item.name}")
        elif report.failed:
            logger.error(f"Test FAILED: {item.name}")
            if hasattr(report, "longrepr"):
                logger.error(f"Error: {report.longrepr}")
        elif report.skipped:
            logger.info(f"Test SKIPPED: {item.name}")


def pytest_html_report_title(report):
    """Sets the title for the HTML report."""
    module_name = "Agoda Flight Booking"
    report.title = f"Test Report: {module_name}"        


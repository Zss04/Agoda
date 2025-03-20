import pytest
import pytest_asyncio
import pytest_html
import os
import json
import sys
from datetime import datetime
from playwright.async_api import async_playwright
import pytest_html.extras

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def pytest_addoption(parser):
    """Add command-line options for test parameters."""
    parser.addoption("--testParameters", action="store", default=None,
                    help="Use test parameters from package.json")

def pytest_sessionstart(session):
    """Called after the Session object has been created and before tests are collected."""
    pass

def pytest_generate_tests(metafunc):
    """
    Generate test parameters dynamically for all tests that need them.
    This function is called once for each test function.
    """
    # Check if the test function needs flight booking parameters
    if all(param in metafunc.fixturenames for param in 
           ["departure_airport", "arrival_airport", "adults", "children", "infants", "cabin"]):
        # Get parameters from the fixture
        params = metafunc.config.getoption("--testParameters")
        test_params = []
        
        if params:
            # Use command line parameters if provided
            try:
                project_root = os.path.dirname(os.path.abspath(__file__))
                json_path = os.path.join(project_root, 'package.json')
                
                # Read the package.json file in read mode
                with open(json_path, 'r') as f:
                    data = json.load(f)
                
                # Check if 'testParameters' key exists in the JSON data
                if 'testParameters' in data:
                    test_params = [
                        (
                            param.get('origin', ''),
                            param.get('destination', ''),
                            param.get('adults', 1),
                            param.get('children', 0),
                            param.get('infants', 0),
                            param.get('class', 'Economy')
                        ) for param in data['testParameters']
                    ]
                else:
                    pass
            except Exception as e:
                pass
        
        # Parametrize the test function
        metafunc.parametrize(
            ["departure_airport", "arrival_airport", "adults", "children", "infants", "cabin"],
            test_params
        )


@pytest_asyncio.fixture(scope="session")
async def search_url():
    """Provides a base URL dictionary for tests."""
    return {"url": None}


@pytest_asyncio.fixture(scope="function")
async def browser():
    """Launches and manages a browser instance for each test."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        if browser is None:
            pytest.fail("The browser did not load.")
        yield browser
        await browser.close()


@pytest_asyncio.fixture(scope="function")
async def page_tuple(browser, search_url, request, create_screenshot_directory):
    """
    Creates a page for testing and handles cleanup.
    Takes screenshots on test failure.
    """
    page = await browser.new_page()
    if page is None:
        pytest.fail("The page did not load.")
    
    yield page, search_url
    
    # Take screenshot if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        await capture_screenshot(page, request, create_screenshot_directory)
    
    await page.close()


@pytest.fixture(scope="session", autouse=True)
def create_screenshot_directory():
    """
    Create the screenshot directory at the start of the session.
    Clears any existing screenshots to avoid accumulation.
    """
    screenshot_dir = os.path.expanduser("~/Downloads/agoda/Reports/Images/")
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
            pass
    
    return screenshot_dir


async def capture_screenshot(page, request, screenshot_dir):
    """Capture screenshot on test failure and add it to HTML report."""
    screenshot_path = os.path.join(
        screenshot_dir, f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
    )
    
    # Capture screenshot
    try:
        await page.screenshot(path=screenshot_path)
    except Exception as e:
        return
    
    # Add to report if file exists
    if os.path.exists(screenshot_path):
        extras = getattr(request.node.rep_call, "extras", [])
        extras.append(pytest_html.extras.image(screenshot_path))
        request.node.rep_call.extras = extras


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


def pytest_html_report_title(report):
    """Sets the title for the HTML report."""
    module_name = "Agoda Flight Booking"
    report.title = f"Test Report: {module_name}"        


import pytest
import pytest_asyncio
import pytest_html
import os
import json
import sys
from datetime import datetime
from playwright.async_api import async_playwright
import pytest_html.extras
from utils.logger_config import setup_logging, get_logger

# Set up logging at the module level
logger = setup_logging("conftest")

def pytest_addoption(parser):
    """Add command-line options for test parameters and report paths."""
    parser.addoption("--testParameters", action="store", default=None,
                    help="Use test parameters from package.json")
    logger.info("Added command-line option: --testParameters")

def pytest_sessionstart(session):
    """Called after the Session object has been created and before tests are collected."""
    logger.info(f"Test session started: {session.config.rootdir}")

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
                logger.info(f"Loading test parameters from package.json for {metafunc.function.__name__}")
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
                    logger.info(f"Loaded {len(test_params)} parameter sets from package.json")
                else:
                    logger.warning("No 'testParameters' key found in package.json")
            except Exception as e:
                logger.error(f"Error loading parameters: {e}")
        
        # Parametrize the test function
        metafunc.parametrize(
            ["departure_airport", "arrival_airport", "adults", "children", "infants", "cabin"],
            test_params
        )
        logger.info(f"Parametrized {metafunc.function.__name__} with {len(test_params)} parameter sets")


@pytest_asyncio.fixture(scope="session")
async def search_url():
    """Provides a base URL dictionary for tests."""
    logger.info("Creating search_url fixture")
    return {"url": None}


@pytest_asyncio.fixture(scope="function")
async def browser():
    """Launches and manages a browser instance for each test."""
    logger.info("Launching browser")
    async with async_playwright() as p:
        # Use headless mode in CI environment (typical for CI/CD pipelines)
        is_ci = os.environ.get("CI", "false").lower() == "true"
        browser = await p.chromium.launch(headless=is_ci)
        if browser is None:
            logger.error("Browser failed to launch")
            pytest.fail("The browser did not load.")
        logger.info(f"Browser launched successfully: {browser}")
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


@pytest.fixture(scope="session")
def create_screenshot_directory(request):
    """
    Create the screenshot directory at the start of the session.
    Uses the artifacts directory if specified in command line options.
    """
<<<<<<< HEAD
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
=======
    # Get artifacts directory from command line option
    artifacts_dir = request.config.getoption("--artifacts-dir")
    screenshot_dir = os.path.join(artifacts_dir, "screenshots")
    
    # Create directory if it doesn't exist
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Don't clear existing files in CI environment to preserve all artifacts
    is_ci = os.environ.get("CI", "false").lower() == "true"
    if not is_ci:
        # Clear any existing files in the directory (only in local development)
        for file in os.listdir(screenshot_dir):
            file_path = os.path.join(screenshot_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                pass
>>>>>>> 35f4cc7 (added docker runner)
    
    logger.info(f"Cleared {file_count} existing screenshots from directory")
    return screenshot_dir


async def capture_screenshot(page, request, screenshot_dir):
    """Capture screenshot on test failure and add it to HTML report."""
<<<<<<< HEAD
    screenshot_path = os.path.join(
        screenshot_dir, f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
    )
    logger.info(f"Capturing screenshot to: {screenshot_path}")
=======
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"{request.node.name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
>>>>>>> 35f4cc7 (added docker runner)
    
    # Capture screenshot
    try:
        await page.screenshot(path=screenshot_path)
<<<<<<< HEAD
        logger.info("Screenshot captured successfully")
    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")
=======
    except Exception:
>>>>>>> 35f4cc7 (added docker runner)
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


def pytest_configure(config):
    """Configure HTML report generation with timestamp and register markers."""
    # Generate timestamped report filename for unique report in CI
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifacts_dir = config.getoption("--artifacts-dir")
    reports_dir = os.path.join(artifacts_dir, "reports")
    
    # Create HTML report config
    html_report_path = os.path.join(reports_dir, f"report_{timestamp}.html")
    
    # Register the HTML report path
    if not hasattr(config, "_metadata"):
        config._metadata = {}
    config._metadata["Report Path"] = html_report_path
    
    # Configure HTML report
    config.option.htmlpath = html_report_path
    
    # Register custom markers
    config.addinivalue_line("markers", "agoda: mark tests as part of the Agoda test suite")


def pytest_html_report_title(report):
    """Sets the title for the HTML report."""
    is_ci = os.environ.get("CI", "false").lower() == "true"
    ci_info = " (CI/CD Pipeline)" if is_ci else ""
    
    module_name = "Agoda Flight Booking"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report.title = f"Test Report: {module_name}{ci_info} - {timestamp}"        


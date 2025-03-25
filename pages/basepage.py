from playwright.async_api import Page, Locator
from utils.logger_config import get_logger

# Get logger for this module
logger = get_logger("BasePage")

class BasePage:
    # This is so we dont have to pass page everytime
    def __init__(self, page: Page):
        # stores page value in instance created
        self.page = page
        logger.debug(f"BasePage initialized with page: {page}")

    async def wait_for_element(self, Loc: Locator, timeout: int = 5000):
        # Wait for an element to appear on the page.
        logger.debug(f"Waiting for element to be visible: {Loc} (timeout: {timeout}ms)")
        try:
            await Loc.wait_for(timeout=timeout, state='visible')
            logger.debug(f"Element is now visible: {Loc}")
        except Exception as e:
            logger.warning(f"Locator '{Loc}' not found. Error: {e}")
        return None

    async def wait_for_loaded_state(self, state: str = 'domcontentloaded', timeout: int = 10000):
        # Wait for the page to load.
        logger.debug(f"Waiting for page load state: {state} (timeout: {timeout}ms)")
        try:
            await self.page.wait_for_load_state(state, timeout=timeout)
            logger.debug(f"Page reached load state: {state}")
        except Exception as e:
            logger.warning(f"Page did not load to state '{state}'. Error: {e}")
        return None
    
    async def get_element(self, selector: str, timeout: int = 10000) -> Locator | None:
        # Finds and returns a single element locator.
        logger.debug(f"Getting element with selector: '{selector}' (timeout: {timeout}ms)")
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            element = self.page.locator(selector)
            logger.debug(f"Element found: '{selector}'")
            return element
        except Exception as e:
            logger.warning(f"Element '{selector}' not found. Error: {e}")
            return None

    async def get_elements(self, selector: str, timeout: int = 5000) -> list[Locator]:
        # Finds and returns a list of element locators.
        logger.debug(f"Getting all elements with selector: '{selector}' (timeout: {timeout}ms)")
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            logger.debug(f"Found {len(elements)} elements with selector: '{selector}'")

            return await self.page.locator(selector).all()
            
        except Exception as e:
            logger.warning(f"Elements '{selector}' not found. Error: {e}")
            return []

    async def get_element_child(self, parent: Locator, selector: str, timeout: int = 5000) -> Locator | None:
        # Finds a child element within a parent locator.
        logger.debug(f"Getting child element with selector: '{selector}' from parent (timeout: {timeout}ms)")
        try:
            await self.wait_for_element(parent, timeout=timeout)
            child = parent.locator(selector)
            logger.debug(f"Child element found: '{selector}'")
            return child
        except Exception as e:
            logger.warning(f"Child element '{selector}' not found in parent. Error: {e}")
            return None

    async def click_element(self, selector: str):
        # Clicks an element if found.
        logger.debug(f"Attempting to click element: '{selector}'")
        element = await self.get_element(selector)
        try:
            await element.click()
            logger.debug(f"Clicked element: '{selector}'")
        except Exception as e:
            logger.warning(f"Could not click element '{selector}'. Error: {e}")
            return None

    async def fill_input(self, selector: str, text: str):
        # Fills an input field if found.
        logger.debug(f"Attempting to fill input '{selector}' with text: '{text}'")
        element = await self.get_element(selector)
        try:
            await element.fill(text)
            logger.debug(f"Filled input '{selector}' with text: '{text}'")
        except Exception as e:
            logger.warning(f"Could not fill text in element '{selector}'. Error: {e}")
            return None

    async def get_text(self, selector: str):
        # Gets inner text of an element.
        logger.debug(f"Getting text from element: '{selector}'")
        try:
            element = await self.get_element(selector)
            text = await element.inner_text()
            logger.debug(f"Got text from element '{selector}': '{text}'")
            return text
        except Exception as e:
            logger.warning(f"Could not get text from element '{selector}'. Error: {e}")
            return None

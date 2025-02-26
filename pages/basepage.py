from playwright.async_api import Page, Locator


class BasePage:
    # This is so we dont have to pass page everytime
    def __init__(self, page: Page):
        # stores page value in instance created
        self.page = page

    async def wait_for_element(self, selector: str, timeout: int = 5000):
        # Wait for an element to appear on the page.
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
        except Exception:
            print(f"Warning: selector '{selector}' not found.")
        return None

    async def get_element(self, selector: str, timeout: int = 10000) -> Locator | None:
        # Finds and returns a single element locator.
        try:
            await self.wait_for_element(selector, timeout=timeout)
            return self.page.locator(selector)
        except Exception:
            print(f"Warning: Element '{selector}' not found.")
            return None

    async def get_elements(self, selector: str, timeout: int = 5000) -> list[Locator]:
        # Finds and returns a list of element locators.
        try:
            await self.wait_for_element(selector, timeout=timeout)
            return self.page.locator(selector).all()
        except Exception:
            print(f"Warning: Elements '{selector}' not found.")
            return []

    async def get_element_child(self, parent: Locator, selector: str, timeout: int = 5000) -> Locator | None:
        # Finds a child element within a parent locator.
        try:
            await parent.wait_for(timeout=timeout, state='visible')
            return parent.locator(selector)
        except Exception:
            print(f"Warning: Child element '{selector}' not found in parent.")
            return None

    async def click_element(self, selector: str):
        # Clicks an element if found.
        element = await self.get_element(selector)
        try:
            await element.click()
        except:
            print(f"Could not click element '{selector}'")
            return None

    async def fill_input(self, selector: str, text: str):
        # Fills an input field if found.
        element = await self.get_element(selector)
        try:
            await element.fill(text)
        except:
            print(f"Could not fill text in element '{selector}'")
            return None

    async def get_text(self, selector: str):
        # Gets inner text of an element.
        try:
            element = await self.get_element(selector)
            return await element.inner_text()
        except:
            print(f"Could not get text from element '{selector}'")
            return None

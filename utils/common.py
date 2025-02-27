from playwright.async_api import Page


class PlaywrightHelper:
    def __init_(self, page: Page):
        self.page = page

    async def wait1(page):
        try:
            await page.wait_for_timeout(1000)
        except Exception as err:
            print("Warning: Did not wait timeout")
            return None
        
    async def wait2(page):
        try:
            await page.wait_for_timeout(2000)
        except Exception as err:
            print("Warning: Did not wait timeout")
            return None

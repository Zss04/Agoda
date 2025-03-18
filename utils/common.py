from playwright.async_api import Page, Locator
from datetime import datetime

class PlaywrightHelper:
    def __init__(self, page: Page):
        self.page = page

    @staticmethod
    def format_date (date_str):
        # Convert string to datetime object 
        date = datetime.strftime(date_str, "%Y-%m-%d")
        return date
    
    async def wait_1000 (self):
        await self.page.wait_for_timeout(1000)
    
    async def date_select_helper(self, get_depart_arrive_date_temp, get_next_month_button, depart_arrive_date_str ) -> Locator :
        max_attempts =12 
        attempts = 0 

        while attempts < max_attempts:
            try:
                date = await get_depart_arrive_date_temp(depart_arrive_date_str)
                if await date.is_visible(timeout=1000):
                    return date
            except Exception:
                pass
            next_month_button = await get_next_month_button()
            if next_month_button:
                await next_month_button.click()
                await self.wait_1000()
            else:
                raise Exception("Next month button not found")
            attempts += 1
    
    
        

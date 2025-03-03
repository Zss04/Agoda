from playwright.async_api import Page
from datetime import datetime, timedelta

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
        
    def format_date (date_str):
        # Convert string to datetime object 
        date = datetime.strftime(date_str, "%Y-%m-%d")
        return date
    
    
        

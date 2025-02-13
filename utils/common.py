from playwright.async_api import Page
from datetime import datetime
import pytest

class PlaywrightHelper:
    def __init__(self, page: Page): # This is so we dont have to pass page everytime
        self.page = page            # stores page value in instance created 
        

    async def get_element(self, selector, timeout=5000):
        try:
            await self.page.wait_for_selector(selector,timeout=timeout)
            return self.page.locator(selector) # Need to return locator and not an element handle 
        
        except Exception:                       # gives warning if get element fails
            print(f"Warning: Did not find element '{selector}'")
            return None
    async def wait(self):
        try:
            await self.page.wait_for_timeout(1000)
    
        except Exception:                       # gives warning if timeout does not work
            print(f"Warning: Did not wait timeout")
            return None
        


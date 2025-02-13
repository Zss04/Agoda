from playwright.async_api import Page



class PlaywrightHelper:
    def __init__(self, page: Page):                                 # This is so we dont have to pass page everytime
        self.page = page                                            # stores page value in instance created 
        
    async def get_element(self, selector, timeout=5000):
        try:
            await self.page.wait_for_selector(selector,timeout=timeout)
            return self.page.locator(selector)                      # returns matching locator
        
        except Exception as err:                                           # gives warning if get element fails
            print(f"Warning: Did not find element '{selector}'")
            return None
        
    async def wait1(self):
        try:
            await self.page.wait_for_timeout(1000)
    
        except Exception as err :                                   # gives warning if timeout does not work
            print(f"Warning: Did not wait timeout")
            return None
    async def get_title(self,selector):
        try:
            return self.page.title(selector)
             
        except Exception as err:                                    # gives warning if cannot find title 
            print(f"Warning: Did not get title")
            return None

    async def get_url(self):
        try:
            page_url = await self.page.url
             
        except Exception as err:                                    # gives warning if cannot find title 
            print(f"Warning: Did not get title")
            return None
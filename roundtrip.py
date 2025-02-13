from playwright.async_api import Page
from utils.common import PlaywrightHelper
import pytest

class test_roundTrip:    # Ideally should be in page object file but for this case its in common
    def __init__(self, page: Page): # This is so we dont have to pass page everytime
        self.page = page            # stores page value in instance created 
        self.helper = PlaywrightHelper(page)

    async def flights(self):                                        # selects the flights tab in the main page
        flight = await self.helper.get_element("//li[@id='tab-flight-tab']")
        await flight.click()
        return 
    
    async def select_trip_type(self, trip_type):
            valid_trip_types = ["roundTrip", "oneWay"]
            if trip_type not in valid_trip_types:
                pytest.fail(f"Invalid trip type: {trip_type}")
                return
            trip_type_locator = await self.helper.get_element(f"//button[@data-component='flight-search-type-{trip_type}']")
            await trip_type_locator.click()
            return

    async def agoda_image(self):
        try:
            img = self.page.wait_for_selector("img[src='https://cdn6.agoda.net/images/kite-js/logo/agoda/color-default.svg']")
            return img
        except: 
            print(f"Warning: Did not find image") # Warns if agoda image is not found on main page
            return None
        
    async def select_airport_options(self, Airport_name):
        # Get options in airport list
        airport_options = await self.helper.get_element( 
            "//li[@class='Suggestion__categoryName_item']"
        )
        if not airport_options:
            pytest.fail("cannot find airport options list")
            
            # count number of options in search list to iterate following 'for' loop
        count = await airport_options.count()
        for i in range (count):
            option_text = await airport_options.nth(i).text_content()

            # Matches user inputted text with text from list 
            if Airport_name.lower() in option_text.lower() :
                await airport_options.nth(i).click()
                return
            # if no other search option matches then click first option
        await airport_options.first.click()



    # Making a function to select Airport
    async def select_airport(self, departure_Airport_name, arrival_Airport_name):
        # takes departure airport and types in search box
        departure_airport = await self.helper.get_element("#flight-origin-search-input")
        await departure_airport.click()
        await self.page.keyboard.type(departure_Airport_name)
        await self.select_airport_options(departure_Airport_name)
        await self.helper.wait1()


        # takes arrival airport and types in search box
        arrival_airport = await self.helper.get_element("#flight-destination-search-input")
        await arrival_airport.click()
        await self.page.keyboard.type(arrival_Airport_name)
        await self.select_airport_options(arrival_Airport_name)
        await self.helper.wait1()
    
    async def select_date(self, departure_date, return_date):
        departure_date_str = departure_date.strftime("%Y-%m-%d")    # Converts date to agoda format 
        return_date_str = return_date.strftime("%Y-%m-%d")          # this should ideally be in a helper file and function should be used here

        departure_locator = await self.helper.get_element(f"//span[@data-selenium-date='{departure_date_str}']")
        await departure_locator.click()
        
        return_locator = await self.helper.get_element(f"//span[@data-selenium-date='{return_date_str}']")
        await return_locator.click()

        


    async def select_passengers_and_cabin(self, adults=1, children=0, infants=0, cabin="Economy"):
        categories = {
            "adult": adults,
            "children": children,
            "infant": infants
        }

        for category, target_count in categories.items():
            increase_btn = await self.helper.get_element(f"//button[@data-element-name='flight-occupancy-{category}-increase']")
            decrease_btn = await self.helper.get_element(f"//button[@data-element-name='flight-occupancy-{category}-decrease']")
            current_category_locator = await self.helper.get_element(f"//span[@data-component='flight-occupancy-{category}-number']")
            current_count_text = await current_category_locator.text_content()
            current_count = int(current_count_text)

            print(f"Current {category}s: {current_count}, Target: {target_count}")

                # Adjust count
            if target_count > current_count:
                for _ in range(target_count - current_count):
                    await increase_btn.click()
            elif target_count < current_count:
                for _ in range(current_count - target_count):
                    await decrease_btn.click()

        # select cabin class
        cabin_locator = await self.helper.get_element(f"//button[@data-component ='flight-search-cabinClass-{cabin}']")
        await cabin_locator.click()

        search_button = await self.helper.get_element("//button[@data-test='SearchButtonBox']")
        await search_button.click() 
     
    async def results (self):
        try: 
            await self.helper.wait1()
            validate_result = self.page.wait_for_selector("div[data-testid='flight-search-box']")
            return validate_result
        
        except Exception as err:
            print(f"Warning: Did not find results")
            return None


        
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
        
        except Exception:
            print(f"Warning: Did not find element '{selector}'")
            return None
        

class roundTrip:    # Ideally should be in page object file but for this case its in common
    def __init__(self, page: Page): # This is so we dont have to pass page everytime
        self.page = page            # stores page value in instance created 
        self.helper = PlaywrightHelper(page)

    async def select_trip_type(self, trip_type):
            valid_trip_types = ["roundTrip", "oneWay"]
            if trip_type not in valid_trip_types:
                pytest.fail(f"Invalid trip type: {trip_type}")
                return
            trip_type_locator = await self.helper.get_element(f"//button[@data-component='flight-search-type-{trip_type}']")
            if trip_type_locator:
                await trip_type_locator.click()
            else:
                pytest.fail("Cannot find trip type {trip_type} button")

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
        if count > 0 :
            await airport_options.first.click()
        else: 
            pytest.fail("No airport with this name can be found")


    # Making a function to select Airport
    async def select_airport(self, departure_Airport_name, arrival_Airport_name):
        # takes departure airport and types in search box
        departure_airport = await self.helper.get_element("#flight-origin-search-input")
        if departure_airport:
            await departure_airport.click()
            await self.page.keyboard.type(departure_Airport_name)
            await self.select_airport_options(departure_Airport_name)
            await self.page.wait_for_timeout(1000)
        else:
            pytest.fail("Departure airport input not found")

        # takes arrival airport and types in search box
        arrival_airport = await self.helper.get_element("#flight-destination-search-input")
        if arrival_airport:
            await arrival_airport.click()
            await self.page.keyboard.type(arrival_Airport_name)
            await self.select_airport_options(arrival_Airport_name)
            await self.page.wait_for_timeout(1000)
        else:
            pytest.fail("Arrival airport input not found")

    async def select_date(self, departure_date, return_date):
        departure_date_str = departure_date.strftime("%Y-%m-%d")  # this should ideally be in a helper file and function should be used here
        return_date_str = return_date.strftime("%Y-%m-%d")

        departure_locator = await self.helper.get_element(f"//span[@data-selenium-date='{departure_date_str}']")
        if departure_locator:
            await departure_locator.click()
        else:
            pytest.fail(f"Departure date '{departure_date_str}' not found!")

        return_locator = await self.helper.get_element(f"//span[@data-selenium-date='{return_date_str}']")
        if return_locator:
            await return_locator.click()
        else:
            pytest.fail(f"Return date '{return_date_str}' not found!")
        


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
        if cabin_locator:
            await cabin_locator.click()
        else: 
            pytest.fail("Cannot find cabin classes")
    
        
from playwright.async_api import Page
from utils.common import PlaywrightHelper
from datetime import datetime, timedelta
import pytest
from pages.basepage import basepage
import re


class test_roundTrip(basepage):
    def __init__(self, page: Page):
        super().__init__(page)

    # selects the flights tab in the main page
    async def click_flights(self):
        await self.click_element("//li[@id='tab-flight-tab']")
        

    async def flights_is_clicked(self):
        flight_tab = await self.get_element("//li[@id='tab-flight-tab']")
        # Check if it has an 'active' or 'selected' class
        is_clicked = await flight_tab.get_attribute("data-selected")
        assert is_clicked == "true", "Flight tab was not selected"
        return True

    async def select_trip_type(self, trip_type):
        valid_trip_types = ["roundTrip", "oneWay"]
        try:
            if trip_type in valid_trip_types:
                await self.click_element(f"//button[@data-component='flight-search-type-{trip_type}']")
                print(f"Selecting trip type: {trip_type}")
        except Exception:
            print(f"Cannot select trip type '{trip_type}'")
            return

    
    async def wait_for_agoda_image(self):
        try:
            await self.page.wait_for_selector("img[src='https://cdn6.agoda.net/images/kite-js/logo/agoda/color-default.svg']", timeout=10000)
        except TimeoutError:
            print("Agoda image not found within timeout")
            return None

    def extract_airport_code(self, text: str) -> str:
        match = re.search(r"([A-Z]{3})\b", text)
        if match: 
            return match.group(0)
        pytest.fail(f"No airport code found in text: '{text}'")
         

    async def select_airport_options(self, Airport_name):
        # Get options in airport list
        airport_options = await self.get_element(
            "//li[@class='Suggestion__categoryName_item']"
        )
        assert airport_options is not None, "Airport options list not found"

        # count number of options in search list to iterate following 'for' loop
        count = await airport_options.count()
        for i in range(count):
            Airport_list = await airport_options.nth(i).text_content()

            # Matches user inputted text with text from list
            if Airport_name.lower() in Airport_list.lower():
                Airport_list_name = Airport_list.strip()
                await airport_options.nth(i).click()
                return Airport_list_name
            # if no other search option matches then click first option
        Airport_list_name = await airport_options.first.text_content()
        await airport_options.first.click()
        return Airport_list_name.strip()

    
    # Making a function to select Airport
    async def set_departure_airport(self, departure_Airport_name):
        # takes departure airport and types in search box
        departure_airport = await self.get_element("#flight-origin-search-input")
        assert departure_airport is not None, "Departure date locator not found"
        await departure_airport.click()
        await self.page.keyboard.type(departure_Airport_name)
        selected_departure_text = await self.select_airport_options(departure_Airport_name)
        selected_departure_code = self.extract_airport_code(selected_departure_text)
        await PlaywrightHelper.wait2(self.page)

        actual_departure_text = await departure_airport.input_value()
        actual_departure_code = self.extract_airport_code(actual_departure_text)
        assert selected_departure_code in actual_departure_code, f"Departure Airport mismatch: '{selected_departure_code}', but got '{actual_departure_code}'"

    async def set_arrival_airport(self, arrival_Airport_name):
        # takes arrival airport and types in search box
        arrival_airport = await self.get_element("#flight-destination-search-input")
        assert arrival_airport is not None, "arrival date locator not found"
        await arrival_airport.click()
        await self.page.keyboard.type(arrival_Airport_name)
        selected_arrival_text = await self.select_airport_options(arrival_Airport_name)
        selected_arrival_code = self.extract_airport_code(selected_arrival_text)
        await PlaywrightHelper.wait2(self.page)

        actual_arrival_text = await arrival_airport.input_value()
        actual_arrival_code = self.extract_airport_code(actual_arrival_text)
        assert selected_arrival_code in actual_arrival_text,  f"Arrival Airport mismatch: '{selected_arrival_code}', but got '{actual_arrival_code}'"

    async def set_date(self):
        # Get tomorrows date
        departure_date = (datetime.today() + timedelta(days=1))
        return_date = departure_date + \
            timedelta(days=3)  # Calculate the return date

        departure_date_str = departure_date.strftime("%Y-%m-%d")
        return_date_str = return_date.strftime("%Y-%m-%d")

        await self.wait_for_element("//dix[@data-selenium='range-picker-date'")

        departure_locator = await self.get_element(f"//span[@data-selenium-date='{departure_date_str}']")
        await departure_locator.click()

        return_locator = await self.get_element(f"//span[@data-selenium-date='{return_date_str}']")
        await return_locator.click()

        assert departure_locator.is_checked(
        ), f"could not select calender date {departure_date_str}"
        assert return_locator.is_checked(
        ), f"could not select calender date {return_date_str}"

    async def set_passengers_and_cabin(self, adults=1, children=0, infants=0, cabin="Economy"):
        categories = {
            "adult": adults,
            "children": children,
            "infant": infants
        }

        for category, target_count in categories.items():
            increase_btn = await self.get_element(f"//button[@data-element-name='flight-occupancy-{category}-increase']")
            decrease_btn = await self.get_element(f"//button[@data-element-name='flight-occupancy-{category}-decrease']")
            current_category_locator = await self.get_element(f"//span[@data-component='flight-occupancy-{category}-number']")
            current_count_text = await current_category_locator.text_content()
            current_count = int(current_count_text)

            print(
                f"Current {category}s: {current_count}, Target: {target_count}")

            # Adjust count
            if target_count > current_count:
                for _ in range(target_count - current_count):
                    await increase_btn.click()
            elif target_count < current_count:
                for _ in range(current_count - target_count):
                    await decrease_btn.click()

        # select cabin class
        cabin_locator = await self.get_element(f"//button[@data-component ='flight-search-cabinClass-{cabin}']")
        assert cabin_locator, f"Cabin class button '{cabin}' not found"
        await cabin_locator.click()

        search_button = await self.get_element("//button[@data-test='SearchButtonBox']")
        assert search_button, "Search button not found"
        await search_button.click()

    async def search_successful(self):
        try:
            await self.page.wait_for_selector("div[data-testid='flight-search-box']")
            return True

        except Exception as err:
            print(f"Warning: Did not find results")
            return None

import re
import pytest
from datetime import datetime, timedelta
from playwright.async_api import Page, TimeoutError
from playwright.async_api._generated import Locator
from utils.common import PlaywrightHelper
from pages.basepage import BasePage


class RoundTrip(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    async def get_flights_frontdoor(self) -> Locator | None:
        return await self.get_element("//li[@id='tab-flight-tab']")

    async def get_round_trip(self) -> Locator | None:
        return await self.get_element("//button[@data-component='flight-search-type-roundTrip']")

    async def get_agoda_image(self) -> Locator | None:
        return await self.get_element(
            "img[src='https://cdn6.agoda.net/images/kite-js/logo/agoda/color-default.svg']"
        )

    async def get_airport_options(self) -> list[Locator]:
        return await self.get_element(
            "//li[@class='Suggestion__categoryName_item']"
        )

    async def get_departure_airport(self) -> Locator | None:
        return await self.get_element("#flight-origin-search-input")

    async def get_arrival_airport(self) -> Locator | None:
        return await self.get_element("#flight-destination-search-input")

    async def get_calender(self) -> Locator | None:
        return await self.get_element("//div[@data-selenium='range-picker-date']")

    async def get_next_month_button(self) -> Locator | None:
        return await self.get_element("//button[@data-selenium='calendar-next-month-button']")
    
    async def get_departure_date_temp(self, departure_date_str) -> Locator | None:
        return await self.get_element(f"//span[@data-selenium-date='{departure_date_str}']")

    async def get_departure_date(self, departure_date_str) -> Locator | None:
        max_attempts =12 
        attempts = 0 

        while attempts < max_attempts:
            try:
                departure_date = await self.get_departure_date_temp(departure_date_str)
                if await departure_date.is_visible():
                    return departure_date
            except Exception:
                pass
            next_month_button = await self.get_next_month_button()
            if next_month_button:
                await next_month_button.click()
                await PlaywrightHelper.wait1(self.page)
            else:
                raise Exception("Next month button not found")
            attempts += 1

    async def get_return_date_temp(self, return_date_str) -> Locator | None:
        return await self.get_element(f"//span[@data-selenium-date='{return_date_str}']")

    async def get_return_date (self, return_date_str) -> Locator | None:
        max_attempts =12 
        attempts = 0 

        while attempts < max_attempts:
            try:
                return_date = await self.get_return_date_temp(return_date_str)
                if await return_date.is_visible():
                    return return_date
            except Exception:
                pass
            next_month_button = await self.get_next_month_button()
            if next_month_button:
                await next_month_button.click()
                await PlaywrightHelper.wait1(self.page)
            else:
                raise Exception("Next month button not found")
            attempts += 1

    async def get_selected_departure_date(self) -> Locator | None:
        return await self.get_element("//div[@data-component='flight-search-departureDate']")

    async def get_selected_return_date(self) -> Locator | None:
        return await self.get_element("//div[@data-component='flight-search-returnDate']")

    async def get_increase_button(self, category: str) -> Locator | None:
        return await self.get_element(f"//button[@data-element-name='flight-occupancy-{category}-increase']")

    async def get_decrease_button(self, category: str) -> Locator | None:
        return await self.get_element(f"//button[@data-element-name='flight-occupancy-{category}-decrease']")

    async def get_category_count(self, category: str) -> Locator | None:
        return await self.get_element(f"//span[@data-component='flight-occupancy-{category}-number']")

    async def get_cabin_class_button(self, cabin: str) -> Locator | None:
        return await self.get_element(f"//button[@data-component='flight-search-cabinClass-{cabin}']")

    async def get_search_button(self) -> Locator | None:
        return await self.get_element("//button[@data-test='SearchButtonBox']")

    async def get_search_results(self) -> Locator | None:
        return await self.get_element("//div[@data-component='flight-search-box']")

    async def get_passengers_and_cabin_count(self) -> Locator | None:
        return await self.get_element("//div[@data-component='flight-search-occupancy']//div[@class='SearchBoxTextDescription__title']")

    async def set_departure_airport(self, airport_name: str) -> None:
        departure_airport = await self.get_departure_airport()
        await departure_airport.click()
        await departure_airport.type(airport_name)
        await PlaywrightHelper.wait2(self.page)

    async def set_arrival_airport(self, airport_name: str) -> None:
        arrival_airport = await self.get_arrival_airport()
        await arrival_airport.click()
        await arrival_airport.type(airport_name)
        await PlaywrightHelper.wait2(self.page)

    async def set_departure_date(self) -> None:
        departure_date_str = self.departure_date_generator()
        await (await self.get_departure_date(departure_date_str)).click()

    async def set_return_date(self) -> None:
        return_date_str = self.return_date_generator()
        await (await self.get_return_date(return_date_str)).click()

    def departure_date_generator(self) -> str:
        # Get tomorrows date
        departure_date = (datetime.today() + timedelta(days=2))
        # Format the dates in (YYYY-MM-DD) format
        departure_date_str = PlaywrightHelper.format_date(departure_date)
        return departure_date_str

    def return_date_generator(self) -> str:
        # Get return date
        return_date = (datetime.today() + timedelta(days=10))
        # Format the dates in (YYYY-MM-DD) format
        return_date_str = PlaywrightHelper.format_date(return_date)
        return return_date_str

    # selects the flights tab in the main page
    async def click_flights(self) -> None:
        flight_btn = await self.get_flights_frontdoor()
        await flight_btn.click()

    # asserts if flights was clicked
    async def flights_is_clicked(self) -> str | None:
        flights_tab = await self.get_flights_frontdoor()
        return await flights_tab.get_attribute("data-selected")

    async def select_roundtrip(self):
        round_trip_btn = await self.get_round_trip()
        await round_trip_btn.click()

    async def is_round_trip_selected(self) -> bool:
        round_trip_btn_selected = (await self.get_round_trip()).get_attribute("aria-pressed")
        if round_trip_btn_selected:
            return True
        return False

    async def wait_for_agoda_image(self, timeout=10000):
        try:
            agoda_image = await self.get_agoda_image()
            await agoda_image.wait_for(timeout=timeout, state="visible")
            return None
        except TimeoutError:
            print("Agoda image not found within timeout")
            return None

    def extract_airport_code(self, text: str) -> str:
        match = re.search(r"([A-Z]{3})\b", text)
        if match:
            return match.group(0)
        pytest.fail(f"No airport code found in text: '{text}'")

    async def select_airport_options(self, Airport_name):
        airport_options = await self.get_airport_options()
        # count number of options in search list to iterate following 'for'
        # loop
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

    async def select_departure_airport(self, departure_Airport_name):
        # takes departure airport and types in search box
        await self.set_departure_airport(departure_Airport_name)

       # Extracts airport code from airport list and user typed airport and
       # asserts if they match
        selected_departure_text = await self.select_airport_options(departure_Airport_name)
        selected_departure_code = self.extract_airport_code(
            selected_departure_text)
        await PlaywrightHelper.wait2(self.page)
        actual_departure_text = await (await self.get_departure_airport()).input_value()
        actual_departure_code = self.extract_airport_code(
            actual_departure_text)
        assert selected_departure_code in actual_departure_code, f"Departure Airport mismatch: '{selected_departure_code}', but got '{actual_departure_code}'"

    async def select_arrival_airport(self, arrival_Airport_name):
        # takes arrival airport and types in search box
        await self.set_arrival_airport(arrival_Airport_name)

       # Extracts airport code from airport list and user typed airport and
       # asserts if they match
        selected_arrival_text = await self.select_airport_options(arrival_Airport_name)
        selected_arrival_code = self.extract_airport_code(
            selected_arrival_text)
        await PlaywrightHelper.wait2(self.page)
        actual_arrival_text = await (await self.get_arrival_airport()).input_value()
        actual_arrival_code = self.extract_airport_code(actual_arrival_text)
        assert selected_arrival_code in actual_arrival_text, f"Arrival Airport mismatch: '{selected_arrival_code}', but got '{actual_arrival_code}'"

    async def wait_for_calender(self, timeout=10000):
        calender = await self.get_calender()
        await calender.wait_for(timeout=timeout, state="visible")

    async def is_departure_date_selected(self) -> bool:
        departure_date_str = self.departure_date_generator()
        selected_departure_date_loc = await self.get_selected_departure_date()
        selected_departure_date = await selected_departure_date_loc.get_attribute("data-date")
        if selected_departure_date == departure_date_str:
            return True
        return False

    async def is_return_date_selected(self) -> bool:
        return_date_str = self.return_date_generator()
        selected_return_date_loc = await self.get_selected_return_date()
        selected_return_date = await selected_return_date_loc.get_attribute("data-date")
        if selected_return_date == return_date_str:
            return True
        return False

    async def select_passengers_and_cabin(
            self, adults: int, children: int, infants: int, cabin: str) -> int:

        # Storing total passengers for assert in next function
        total_passengers = adults + children + infants
        categories = {
            "adult": adults,
            "children": children,
            "infant": infants
        }

        for category, target_count in categories.items():
            increase_btn = await self.get_increase_button(category)
            decrease_btn = await self.get_decrease_button(category)
            current_category_locator = await self.get_category_count(category)
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
        cabin_locator = await self.get_cabin_class_button(cabin)
        await cabin_locator.click()
        return total_passengers

    async def search(self) -> Locator | None:
        search_button = await self.get_search_button()
        await search_button.click()

    async def passengers_and_cabin_count(self) -> int:
        passenger_element = await self.get_passengers_and_cabin_count()
        passengers_text = await passenger_element.inner_text()
        passenger_count = int(passengers_text.split()[0])
        return passenger_count

    async def search_successful(self) -> bool:
        try:
            results = await self.get_search_results()
            await results.wait_for(timeout=15000, state="visible")
            return True

        except TimeoutError:
            print(f"Warning: Did not find results")
            return False

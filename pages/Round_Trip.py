import re
import pytest
from datetime import datetime, timedelta
from playwright.async_api import Page, TimeoutError
from playwright.async_api._generated import Locator
from utils.common import PlaywrightHelper 
from pages.basepage import BasePage
from utils.logger_config import get_logger

# Get logger for this module
logger = get_logger("RoundTrip")


class RoundTrip(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.PlaywrightHelper = PlaywrightHelper(page)
        logger.info("RoundTrip page object initialized")

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

    async def get_departure_date(self , depart_arrive_date_str) -> Locator | None:
        get_departure_date_temp = self.get_departure_date_temp
        next_month_button = self.get_next_month_button
        return await self.PlaywrightHelper.date_select_helper(get_departure_date_temp, next_month_button, depart_arrive_date_str)

    async def get_return_date_temp(self, return_date_str) -> Locator | None:
        return await self.get_element(f"//span[@data-selenium-date='{return_date_str}']")

    async def get_return_date (self, depart_arrive_date_str) -> Locator | None:
        get_arrival_date_temp = self.get_departure_date_temp
        next_month_button = self.get_next_month_button
        return await self.PlaywrightHelper.date_select_helper(get_arrival_date_temp, next_month_button, depart_arrive_date_str)

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

    async def set_departure_airport(self, airport_name: str, timeout = 2000) -> None:
        logger.debug(f"Setting departure airport to: {airport_name}")
        departure_airport = await self.get_departure_airport()
        await departure_airport.click()
        await departure_airport.type(airport_name, timeout=timeout)
        logger.info(f"Departure airport set to: {airport_name}")
        

    async def set_arrival_airport(self, airport_name: str, timeout = 2000) -> None:
        logger.info(f"Setting arrival airport to: {airport_name}")
        arrival_airport = await self.get_arrival_airport()
        await arrival_airport.click()
        await arrival_airport.type(airport_name, timeout=timeout)
        logger.info(f"Arrival airport set to: {airport_name}")


    async def set_departure_date(self) -> None:
        departure_date_str = self.departure_date_generator()
        date = await self.get_departure_date(departure_date_str)
        await date.click()
        logger.info(f"Departure date set to: {departure_date_str}")
        

    async def set_return_date(self) -> None:
        return_date_str = self.return_date_generator()
        date = await self.get_return_date(return_date_str)
        await date.click()
        logger.info(f"Return date set to: {return_date_str}")

    def departure_date_generator(self) -> str:
        # Get tomorrows date
        departure_date = (datetime.today() + timedelta(days=40))
        # Format the dates in (YYYY-MM-DD) format
        departure_date_str = PlaywrightHelper.format_date(departure_date)
        logger.info(f"Generated departure date: {departure_date_str}")
        return departure_date_str

    def return_date_generator(self) -> str:
        # Get return date
        return_date = (datetime.today() + timedelta(days=60))
        # Format the dates in (YYYY-MM-DD) format
        return_date_str = PlaywrightHelper.format_date(return_date)
        logger.info(f"Generated return date: {return_date_str}")
        return return_date_str

    # selects the flights tab in the main page
    async def click_flights(self) -> None:
        logger.info("Clicking on Flights tab")
        flight_btn = await self.get_flights_frontdoor()
        if not flight_btn:
            logger.error("Flights tab element not found")
            return
        await flight_btn.click()
        logger.info("Flights tab clicked")

    # asserts if flights was clicked
    async def flights_is_clicked(self) -> str | None:
        logger.info("Checking if Flights tab is selected")
        flights_tab = await self.get_flights_frontdoor()
        return await flights_tab.get_attribute("data-selected")

    async def select_roundtrip(self):
        logger.info("Selecting round trip option")
        round_trip_btn = await self.get_round_trip()
        await round_trip_btn.click()

    async def is_round_trip_selected(self) -> bool:
        round_trip_btn_selected = (await self.get_round_trip()).get_attribute("aria-pressed")
        if round_trip_btn_selected:
            logger.info("Round trip option selected")
            return True
        logger.info("Round trip option not selected")
        return False

    async def wait_for_agoda_image(self):
        logger.info("Waiting for Agoda image to appear")
        try:
            agoda_image = await self.get_agoda_image()
            await self.wait_for_element(agoda_image)
            logger.info("Agoda image found - website loaded successfully")
            return True
        except TimeoutError:
            logger.error("CRITICAL: Agoda image not found within timeout - website may not have loaded properly")
            return False


    async def _set_and_verify_airport(self, airport_name: str, set_airport_func, get_airport_func, airport_label: str) -> None:
        logger.info(f"Setting and verifying {airport_label} airport: {airport_name}")
        # Set the airport via the search box.
        await set_airport_func(airport_name)
        await PlaywrightHelper.wait_1000(self)

        # Select the airport from the options and extract its code.
        selected_text = await self.select_airport_options(airport_name)
        selected_code = self.extract_airport_code(selected_text)
        logger.info(f"Selected {airport_label} airport: {selected_text} (Code: {selected_code})")
                
        # Get the current value from the airport input field and extract its code.
        actual_text = await (await get_airport_func()).input_value()
        actual_code = self.extract_airport_code(actual_text)
        logger.info(f"Actual {airport_label} airport: {actual_text} (Code: {actual_code})")
        
        # Assert that the selected airport code is in the actual airport code.
        assert (
            selected_code in actual_code
        ), f"{airport_label} Airport mismatch: '{selected_code}', but got '{actual_code}'"

    def extract_airport_code(self, text: str) -> str:
        logger.debug(f"Extracting airport code from: {text}")
        match = re.search(r"([A-Z]{3})\b", text)
        if match:
            return match.group(0)
        pytest.fail(f"No airport code found in text: '{text}'")

    async def select_airport_options(self, Airport_name):
        logger.info(f"Selecting airport from options: {Airport_name}")
        airport_options = await self.get_airport_options()
        # count number of options in search list to iterate following 'for'
        # loop
        count = await airport_options.count()
        logger.info(f"Found {count} airport options")
        
        for i in range(count):
            Airport_list = await airport_options.nth(i).text_content()
            logger.debug(f"Option {i+1}: {Airport_list}")

            # Matches user inputted text with text from list
            if Airport_name.lower() in Airport_list.lower():
                Airport_list_name = Airport_list.strip()
                logger.info(f"Found matching airport: {Airport_list_name}")
                await airport_options.nth(i).click()
                return Airport_list_name # returns airport name to assert function

        # if no other search option matches then click first option
        logger.warning(f"No exact match found for '{Airport_name}', selecting first option")
        Airport_list_name = await airport_options.first.text_content()
        await airport_options.first.click()
        return Airport_list_name.strip()

    async def select_departure_airport(self, departure_airport_name: str) -> None:
        logger.info(f"Selecting departure airport: {departure_airport_name}")
        await self._set_and_verify_airport(
            departure_airport_name,
            self.set_departure_airport,
            self.get_departure_airport,
            "Departure"
        )
        logger.info(f"Departure airport selected: {departure_airport_name}")


    async def select_arrival_airport(self, arrival_airport_name: str) -> None:
        logger.info(f"Selecting arrival airport: {arrival_airport_name}")
        await self._set_and_verify_airport(
            arrival_airport_name,
            self.set_arrival_airport,
            self.get_arrival_airport,
            "Arrival"
        )
        logger.info(f"Arrival airport selected: {arrival_airport_name}")

    async def wait_for_calender(self):
        logger.info("Waiting for calendar to appear")
        calender = await self.get_calender()
        await self.wait_for_element(calender)
        logger.info("Calendar appeared successfully")

    async def is_departure_date_selected(self) -> bool:
        logger.info("Checking if departure date is selected")
        departure_date_str = self.departure_date_generator()
        selected_departure_date_loc = await self.get_selected_departure_date()
        selected_departure_date = await selected_departure_date_loc.get_attribute("data-date")
        logger.info(f"Expected departure date: {departure_date_str}, Actual: {selected_departure_date}")
        
        if selected_departure_date == departure_date_str:
            logger.info("Departure date is correctly selected")
            return True
        logger.warning(f"Departure date mismatch: expected {departure_date_str}, got {selected_departure_date}")
        return False

    async def is_return_date_selected(self) -> bool:
        logger.info("Checking if return date is selected")
        return_date_str = self.return_date_generator()
        selected_return_date_loc = await self.get_selected_return_date()
        selected_return_date = await selected_return_date_loc.get_attribute("data-date")
        logger.info(f"Expected return date: {return_date_str}, Actual: {selected_return_date}")
        
        if selected_return_date == return_date_str:
            logger.info("Return date is correctly selected")
            return True
        logger.warning(f"Return date mismatch: expected {return_date_str}, got {selected_return_date}")
        return False

    async def select_passengers_and_cabin(
            self, adults: int, children: int, infants: int, cabin: str) -> int:
        logger.info(f"Selecting passengers: Adults={adults}, Children={children}, Infants={infants}, Cabin={cabin}")
        # Storing total passengers for assert in next function
        total_passengers = adults + children + infants
        categories = {
            "adult": adults,
            "children": children,
            "infant": infants
        }

        for category, target_count in categories.items():
            logger.info(f"Adjusting {category} count to {target_count}")
            increase_btn = await self.get_increase_button(category)
            decrease_btn = await self.get_decrease_button(category)
            current_category_locator = await self.get_category_count(category)
            current_count_text = await current_category_locator.text_content()
            current_count = int(current_count_text)

            logger.info(
                f"Current {category}s: {current_count}, Target: {target_count}")

            # Adjust count
            if target_count > current_count:
                for i in range(target_count - current_count):
                    await increase_btn.click()
                    logger.debug(f"Increased {category} count ({i+1}/{target_count - current_count})")
            elif target_count < current_count:
                for i in range(current_count - target_count):
                    await decrease_btn.click()
                    logger.debug(f"Decreased {category} count ({i+1}/{current_count - target_count})")

        # select cabin class
        logger.info(f"Selecting cabin class: {cabin}")
        cabin_locator = await self.get_cabin_class_button(cabin)
        await cabin_locator.click()
        return total_passengers

    async def search(self) -> Locator | None:
        logger.info("Clicking search button")
        search_button = await self.get_search_button()
        await search_button.click()
        logger.info("Search button clicked")
        

    async def passengers_and_cabin_count(self) -> int:
        logger.info("Getting passengers and cabin count")
        passenger_element = await self.get_passengers_and_cabin_count()
        passengers_text = await passenger_element.inner_text()
        passenger_count = int(passengers_text.split()[0])
        return passenger_count

    async def search_successful(self) -> bool:
        logger.info("Checking if search was successful")
        try:
            results = await self.get_search_results()
            await self.wait_for_element(results)
            logger.info("Search successful - results found")
            return True

        except TimeoutError:
            logger.warning("Search results not found within timeout")
            return False

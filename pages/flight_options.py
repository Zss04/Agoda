import pytest
from playwright.async_api import Page
from urllib.parse import urlparse, parse_qs
from utils.logger_config import get_logger

# Get logger for this module
logger = get_logger("FlightOptions")

from playwright.async_api import Locator
from pages.basepage import BasePage
from utils.common import PlaywrightHelper

class FlightInfo(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
    

    # Getters for UI elements
    async def get_search_departure_loc(self) -> Locator | None:
        return await self.get_element("//div[@data-testid='flight-origin-text-search']//input[@role='combobox']")

    async def get_search_arrival_loc(self) -> Locator | None:
        return await self.get_element("//div[@data-testid='flight-destination-text-search']//input[@role='combobox']")

    async def get_search_calender_departure(self) -> Locator | None:
        return await self.get_element("//button[@data-testid='departure-date-input']")

    async def get_search_departure_date(self) -> Locator | None:
        return await self.get_element(
            "//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') "
            "and contains(@class, 'filled') and contains(@class, 'Calendar__startDate--3vDzR')]/div[@data-selenium-date]"
        )

    async def get_search_calender_arrival(self) -> Locator | None:
        return await self.get_element("//button[@data-testid='arrival-date-input']")

    async def get_search_return_date(self) -> Locator | None:
        return await self.get_element(
            "//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') "
            "and contains(@class, 'filled') and contains(@class, 'Calendar__endDate--1j6dD')]/div[@data-selenium-date]"
        )

    async def get_search_passengers(self) -> Locator | None:
        return await self.get_element("//div[@data-element-name='flight-occupancy']")

    async def get_search_adults(self) -> Locator | None:
        return await self.get_element("//p[@data-component='adults-count']")

    async def get_search_children(self) -> Locator | None:
        return await self.get_element("//p[@data-component='children-count']")

    async def get_search_infants(self) -> Locator | None:
        return await self.get_element("//p[@data-component='infants-count']")

    async def get_search_cabin_type(self) -> Locator | None:
        return await self.get_element("//div[@data-element-name='flight-cabin-class']//p[@class='sc-jsMahE sc-kFuwaP bEtAca gEKgFh']")

    async def get_flight_cards(self) -> list[Locator]:
        return await self.get_elements("//div[contains(@data-testid, 'web-refresh-flights-card') and not(contains(@style, 'display: none'))]")

    async def get_flight_carrier(self, flight) -> Locator | None:
        return await self.get_element_child(flight, "//div[@data-testid='flightCard-flight-detail']//p[@class='sc-jsMahE sc-kFuwaP bEtAca ftblUM']")
    
    async def get_flight_duration(self, flight) -> Locator | None:
        return await self.get_element_child(flight, "//div[@data-testid='flightCard-flight-detail']//span[@data-testid='duration']")
    
    async def get_flight_price(self, flight) -> Locator | None:
        return await self.get_element_child(flight, "//span[@data-element-name='flight-price-breakdown']//span[@class='sc-jsMahE sc-kFuwaP bEtAca kkhXWj']")
    
    async def get_flight_currency(self, flight) -> Locator | None:
        return await self.get_element_child(flight, "//span[@data-element-name='flight-price-breakdown']//span[@class='sc-jsMahE sc-kFuwaP brYcTc bpqEor']")
    
    async def get_flight_dropdown(self, flight) -> Locator | None:
        return await self.get_element_child(flight, "//div[@class='FlightsCard-module__collapsedChevron--kYIMo']")
    
    async def get_direct_stop_checkbox(self) -> Locator | None:
        return await self.get_element("//div[@data-component='Direct']//label[@data-element-name='flight-filter-stops-item']")

    async def get_one_stop_checkbox(self) -> Locator | None:
        return await self.get_element("//div[@data-component='One']//label[@data-element-name='flight-filter-stops-item']")
    
    async def get_two_plus_stop_checkbox(self) -> Locator | None:
        return await self.get_element("//div[@data-component='TwoPlus']//label[@data-element-name='flight-filter-stops-item']")
    
    async def get_layover_count(self, flight) -> Locator | None:
        return await self.get_element_child(flight, "//span[@class='sc-jsMahE sc-kFuwaP bEtAca fdKTiB']")
        
    async def get_temp_title(self) -> Locator | None:
        return await self.get_element("//h2[@data-component='mob-flight-result-title']")
    
    async def get_no_results_page(self) -> Locator | None:
        return await self.get_element("//div[@data-testid='no-result-page']")
    
    async def get_clicked_checkbox(self) -> Locator | None:
        return await self.get_element("//label[@class='a83dd-box a83dd-fill-product-primary a83dd-text-product-primary a83dd-cursor-pointer a83dd-flex']")
    
    async def validate_search(self, search_url) -> bool:
        logger.info("Validating search parameters")
        url = self.validate_url(search_url)
        header = await self.validate_from_header()

        for url_value, header_value in zip(url, header):
            url_value = (str(url_value)).replace(" ","").lower()
            header_value = (str(header_value)).replace(" ","").lower()
            if url_value.strip() not in header_value.strip():
                logger.warning(f"URL value '{url_value}' not found in header value '{header_value}'")
                return False
        logger.info("Search parameters validated successfully")
        return True

    def validate_url(self, search_url) -> list:
        logger.info(f"Validating URL: {search_url}")
        parsed_url = urlparse(search_url)
        query_params = parse_qs(parsed_url.query)

        keys = ["departureFrom", "arrivalTo", "departDate", "returnDate", "adults", "children", "infants", "cabinType"]
        url = [query_params.get(key, ["0"])[0] for key in keys]  # "0" as default for missing values

        logger.info("Extracted from URL:")
        for key, value in zip(keys, url):
            logger.info(f"{key}: {value}")

        return url

    async def validate_from_header(self) -> list:
        logger.info("Validating from header")
        header_data = []

        # Extract departure and arrival locations
        await self.wait_for_loaded_state()
        await PlaywrightHelper.wait_1000(self)

        departure_input_element = await self.get_search_departure_loc()
        await self.wait_for_element(departure_input_element)
        departure_value = await departure_input_element.get_attribute("value")
        header_data.append(departure_value)
        logger.info(f"Departure value: {departure_value}")

        arrival_input_element = await self.get_search_arrival_loc()
        await self.wait_for_element(arrival_input_element)
        arrival_value = await arrival_input_element.get_attribute("value")
        header_data.append(arrival_value)
        logger.info(f"Arrival value: {arrival_value}")

        # Open the departure calendar and get the selected departure date
        departure_calendar_button = await self.get_search_calender_departure()
        await departure_calendar_button.click()
        logger.info("Clicked departure calendar button")

        departure_date_element = await self.get_search_departure_date()
        departure_date = await departure_date_element.get_attribute("data-selenium-date")
        header_data.append(departure_date)
        logger.info(f"Departure date: {departure_date}")

        # Open the return calendar and get the selected return date
        return_calendar_button = await self.get_search_calender_arrival()
        await return_calendar_button.click()
        logger.info("Clicked return calendar button")

        await PlaywrightHelper.wait_1000(self)  

        return_date_element = await self.get_search_return_date()
        return_date = await return_date_element.get_attribute("data-selenium-date")
        header_data.append(return_date)
        logger.info(f"Return date: {return_date}")

        # Open passenger selection dropdown and extract passenger details
        passenger_dropdown = await self.get_search_passengers()
        await passenger_dropdown.click()
        logger.info("Clicked passenger dropdown")

        adults_element = await self.get_search_adults()
        adults_count = await adults_element.inner_text()
        header_data.append(adults_count)
        logger.info(f"Adults count: {adults_count}")

        children_element = await self.get_search_children()
        children_count = await children_element.inner_text()
        header_data.append(children_count)
        logger.info(f"Children count: {children_count}")

        infants_element = await self.get_search_infants()
        infants_count = await infants_element.inner_text()
        header_data.append(infants_count)
        logger.info(f"Infants count: {infants_count}")

        # Extract cabin class type
        cabin_type_element = await self.get_search_cabin_type()
        cabin_type = await cabin_type_element.inner_text()
        header_data.append(cabin_type)
        logger.info(f"Cabin type: {cabin_type}")

        logger.info(f"Extracted from Header: {header_data}")
        return header_data

    async def flight_data(self) -> list[list[str]]:
        """
        Collects and organizes flight data into a structured 2D array.
        
        Returns:
            list[list[str]]: A 2D array with flight information including carrier, duration, price, and layovers
        """
        logger.info("Collecting flight data")
        # Check if results are available
        await self.check_no_flights_message()
        
        # check all flight options and store headings in 2D array
        flight_loc = await self.get_flight_cards()
        flight_data_2d = [["Carrier", "Duration", "Price", "Layovers"]]
        # gets details for all flights in flight instance on page until all flights on page have been stored in array
        for flight in flight_loc:
            carrier_loc = await self.get_flight_carrier(flight)
            carrier = await carrier_loc.inner_text()

            duration_loc = await self.get_flight_duration(flight)
            duration = await duration_loc.inner_text()
            
            price_loc = await self.get_flight_price(flight)
            price = await price_loc.inner_text()
            
            currency_loc = await self.get_flight_currency(flight)
            currency = await currency_loc.inner_text()
            
            stops = await self.layover_count(flight)

            
            # appends data in array under respective headers
            flight_data_2d.append(
                [carrier.strip(), duration.strip(), f"{price.strip()} {currency.strip()}", stops ])

        return flight_data_2d
        

    async def process_flight_option(self, checkbox_getter, allowed_stops: list) -> bool:
        """
        Processes flight options by clicking a filter checkbox and validating layover counts.
        
        Args:
            checkbox_getter: Function to get the checkbox element
            allowed_stops: List of allowed layover counts (e.g., [0] for direct, [0,1] for direct and one-stop)
        
        Returns:
            bool: True if all flights match the allowed stops criteria, False otherwise
        """
        # Click the appropriate checkbox and wait for the page to load
        await self.click_checkbox_and_wait(checkbox_getter)
        
        if allowed_stops == [0]: 
            trip_stops = "direct" 
        elif allowed_stops == [0,1]:
            trip_stops = "One Stop"
        else: 
            trip_stops = "2+ stops"
        
        logger.info(f"Processing flight option: {trip_stops}")
        
        try:
            # Check each flight against the criteria
            flights_available = await self.get_flight_cards()
            logger.info(f"Number of stops for {trip_stops} are: ")
            for flight in flights_available:
                stops = await self.layover_count(flight)
                logger.info(f"{stops}\n")
                if stops not in allowed_stops:
                    return False
            return True
        except Exception as e:
            logger.warning(f"warning processing flight option {trip_stops}: {e}")
            return False
            

    async def layover_count(self, flight, timeout=2000):
        """
        Gets the layover count for a flight.
        Uses multiple strategies to determine the correct count.
        
        Args:
            flight: The flight element
            timeout: Maximum time to wait for the layover element
        
        Returns:
            int: The number of layovers (0 for direct flights)
        """
        try:
            layovers_loc = await self.get_layover_count(flight)
            if layovers_loc:  
                layovers = await layovers_loc.inner_text(timeout=timeout)
                layovers_count = int(layovers.strip())
            else:
                layovers_count = 0  # If no element found, assume 0 layovers
        except Exception as e:
            logger.info(f"Error retrieving layover count: {e}")
            layovers_count = 0
        return layovers_count
        
    async def check_no_flights_message(self) :
        logger.info("Checking for 'no flights' message")
        try:
            await self.wait_for_loaded_state()
            no_results = await self.get_no_results_page()
            if no_results:
                logger.error("No flights available for these dates")
                pytest.fail("No flights available for these dates")  # Indicates that the "no flights" message is displayed
            logger.info("Flights are available (no 'no flights' message found)")
            
        except Exception as e:
            logger.info(f"Error checking for no flights message: {e}")
            

    async def click_checkbox_and_wait(self, checkbox_getter) -> None:
        logger.info(f"Clicking checkbox: {checkbox_getter.__name__}")
        checkbox = await checkbox_getter()
        await self.wait_for_element(checkbox)
        await checkbox.click()
        logger.info(f"Clicked checkbox: {checkbox_getter.__name__}")
        

    # Direct flights should only have 0 stops.
    async def flight_direct_stop(self) -> bool:
        logger.info("Checking direct flights")
        await self.check_no_flights_message()
        result = await self.process_flight_option(self.get_direct_stop_checkbox, [0])
        await self.PlaywrightHelper.wait_1000()
        await self.wait_for_loaded_state(state='networkidle')
        logger.info(f"Direct flights check result: {result}")
        return result

    # One-stop flights can have either 0 or 1 stop.
    async def flight_one_stop(self) -> bool:
        logger.info("Checking one-stop flights")
        result = await self.process_flight_option(self.get_one_stop_checkbox, [0,1])
        logger.info(f"One-stop flights check result: {result}")
        return result
    
    async def flight_two_plus_stop(self) -> bool:
        logger.info("Checking two-plus-stop flights")
        result = await self.process_flight_option(self.get_two_plus_stop_checkbox, [0, 1, 2, 3, 4])
        logger.info(f"Two-plus-stop flights check result: {result}")
        return result
            
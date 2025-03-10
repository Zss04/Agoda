from playwright.async_api import Page
from urllib.parse import urlparse, parse_qs

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
        return await self.get_elements("//div[@data-testid='web-refresh-flights-card']")

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
    
    async  def get_no_results_page(self) -> Locator | None:
        return await self.get_element("//div[@data-testid='no-result-page']")
    
    async def validate_search(self, search_url) -> bool:
        url = self.validate_url(search_url)
        header = await self.validate_from_header()

        for url_value, header_value in zip(url, header):
            url_value = (str(url_value)).replace(" ","").lower()
            header_value = (str(header_value)).replace(" ","").lower()
            if url_value.strip() not in header_value.strip():
                return False
        return True

    def validate_url(self, search_url) -> list:
        parsed_url = urlparse(search_url)
        query_params = parse_qs(parsed_url.query)

        keys = ["departureFrom", "arrivalTo", "departDate", "returnDate", "adults", "children", "infants", "cabinType"]
        url = [query_params.get(key, ["0"])[0] for key in keys]  # "0" as default for missing values

        print("Extracted from URL:")
        for key, value in zip(keys, url):
            print(f"{key}: {value}")

        return url

    async def validate_from_header(self) -> list:
        header_data = []

        # Extract departure and arrival locations
        await self.wait_for_loaded_state()

        departure_input_element = await self.get_search_departure_loc()
        await self.wait_for_element(departure_input_element)
        departure_value = await departure_input_element.get_attribute("value")
        header_data.append(departure_value)

        arrival_input_element = await self.get_search_arrival_loc()
        await self.wait_for_element(arrival_input_element)
        arrival_value = await arrival_input_element.get_attribute("value")
        header_data.append(arrival_value)

        # Open the departure calendar and get the selected departure date
        departure_calendar_button = await self.get_search_calender_departure()
        await departure_calendar_button.click()

        departure_date_element = await self.get_search_departure_date()
        departure_date = await departure_date_element.get_attribute("data-selenium-date")
        header_data.append(departure_date)

        # Open the return calendar and get the selected return date
        return_calendar_button = await self.get_search_calender_arrival()
        await return_calendar_button.click()

        
        return_date_element = await self.get_search_return_date()
        return_date = await return_date_element.get_attribute("data-selenium-date")
        header_data.append(return_date)

        # Open passenger selection dropdown and extract passenger details
        passenger_dropdown = await self.get_search_passengers()
        await passenger_dropdown.click()

        adults_element = await self.get_search_adults()
        adults_count = await adults_element.inner_text()
        header_data.append(adults_count)

        children_element = await self.get_search_children()
        children_count = await children_element.inner_text()
        header_data.append(children_count)

        infants_element = await self.get_search_infants()
        infants_count = await infants_element.inner_text()
        header_data.append(infants_count)

        # Extract cabin class type
        cabin_type_element = await self.get_search_cabin_type()
        cabin_type = await cabin_type_element.inner_text()
        header_data.append(cabin_type)

        print(f"Extracted from Header:\n{header_data}")
        return header_data

    async def flight_data(self) -> list[list[str]]:
        # check if results are available
        no_results = await self.check_no_flights_message()
        if no_results:
            return [["No flights available for these dates."]]
        
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
        # Click the appropriate checkbox and wait for the page to load
        await self.click_checkbox_and_wait(checkbox_getter)
        
        if allowed_stops == [0]: 
            trip_stops = "direct" 
        elif allowed_stops == [0,1]:
            trip_stops = "One Stop"
        else: 
            trip_stops = "2+ stops"
        
        flight_data = await self.flight_data()
        no_results = await self.check_no_flights_message()
        # Getting layover count at index 3 in each row (after the header row)
        layover_column = [row[3] for row in flight_data[1:] if len(row) > 3]

        
        # If no results message is shown and all extracted layover values are within allowed stops, we return True
        if no_results and all(stop in allowed_stops for stop in layover_column):
            print(f"There were no flights available for these days for {trip_stops}")
            return True

        # Otherwise, check the flight cards one by one
        flights_available = await self.get_flight_cards()
        print(f"\033[1m" + "Number of stops for {trip_stops} are: " + "\033[1m")

        for flight in flights_available:
            stops = await self.layover_count(flight)
            print(f"{stops}\n")
            if stops not in allowed_stops:
                return False
        return True

    async def layover_count (self, flight, timeout=5000):
        layovers_loc = await self.get_layover_count(flight)
        try:
            if layovers_loc:  
                layovers = await layovers_loc.inner_text(timeout=timeout)
                layovers_count = int(layovers.strip())
            else:
                layovers_count = 0  # If no element found, assume 0 layovers
        except Exception as e: 
            print(f"Error retrieving layover count: {e}")
            layovers_count = 0
        return layovers_count
        
    async def check_no_flights_message(self) -> bool:
        try:
            await self.wait_for_loaded_state()
            no_results = await self.get_no_results_page()
            if no_results:
                return True  # Indicates that the "no flights" message is displayed
            return False  # Indicates that flights are available
        except Exception as e:
            print(f"Error checking for no flights message: {e}")
            return False  # Assume flights are available if there's an error

    async def click_checkbox_and_wait(self, checkbox_getter) -> None:
        checkbox = await checkbox_getter()
        await self.wait_for_element(checkbox)
        await checkbox.click()
        await self.wait_for_loaded_state()

    # Direct flights should only have 0 stops.
    async def flight_direct_stop(self) -> bool:
        no_results = await self.check_no_flights_message()
        if no_results:
            return True
        return await self.process_flight_option(self.get_direct_stop_checkbox, [0])

    # One-stop flights can have either 0 or 1 stop.
    async def flight_one_stop(self) -> bool:
        return await self.process_flight_option(self.get_one_stop_checkbox, [0,1])
    
    async def flight_two_plus_stop(self) -> bool:
        return await self.process_flight_option(self.get_two_plus_stop_checkbox, [0, 1, 2, 3, 4])


        
        
       
            
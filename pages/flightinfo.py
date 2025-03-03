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

    async def get_next_month_button(self) -> Locator | None:
        return await self.get_element("//button[@data-selenium='calendar-next-month-button']")

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
    
    async def get_direct_stop_checkbox(self) -> Locator | None:
        return await self.get_element("//div[@data-component='Direct']//label[@data-element-name='flight-filter-stops-item']")

    async def get_one_stop_checkbox(self) -> Locator | None:
        return await self.get_element("//div[@data-component='One']//label[@data-element-name='flight-filter-stops-item']")
    
    async def get_layover_count(self, flight) -> Locator | None:
        return await self.get_element_child(flight, "//div[@aa373-box aa373-fill-inherit aa373-text-inherit aa373-relative aa373-mx-auto      ']//span[@data-testid='layover']")
    
    async def get_temp_title(self) -> Locator | None:
        return await self.get_element("//h2[@data-component='mob-flight-result-title']")
    
    async  def get_no_results_page(self):
        return await self.get_element("//div[@data-testid='no-result-page']")
    
    def validate_url(self, search_url) -> list:
        parsed_url = urlparse(search_url)
        query_params = parse_qs(parsed_url.query)

        keys = ["departureFrom", "arrivalTo", "departDate", "returnDate", "adults", "children", "infants", "cabinType"]
        url = [query_params.get(key, ["0"])[0] for key in keys]  # "0" as default for missing values

        print("Extracted from URL:")
        for key, value in zip(keys, url):
            print(f"{key}: {value}")

        return url

    async def validate_from_header(self):
        header_data = []

        # Extract departure and arrival locations
        departure_input_element = await self.get_search_departure_loc()
        await self.wait_for_loaded_state(state='load')
        departure_value = await departure_input_element.get_attribute("value")
        header_data.append(departure_value)

        arrival_input_element = await self.get_search_arrival_loc()
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
        await PlaywrightHelper.wait1(self.page)
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

    async def validate_search(self, search_url):
        url = self.validate_url(search_url)
        header = await self.validate_from_header()

        for url_value, header_value in zip(url, header):
            url_value = str(url_value)
            header_value = str(header_value)
            if url_value.strip() not in header_value.strip():
                return False
        return True


    async def flight_data(self):

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
            
            # layover_loc = await self.get_layover_count(flight)
            # if layover_loc.wait_for(timeout=5000, state='visible'):
            #     layovers = await layover_loc.inner_text()
            #     layovers_count = int(layovers)
            # else: 
            #     layovers_count = 0 # Flight is direct 

            # appends data in array under respective headers
            flight_data_2d.append(
                [carrier.strip(), duration.strip(), f"{price.strip()} {currency.strip()}"])

        return flight_data_2d
    
    # async def check_no_flights_message(self) -> bool:
    #     no_results = await self.get_no_results_page()
    #     if no_results:
    #         return False
    #     return True

    # async def flight_direct_stop (self) -> bool:
    #     direct_stop = await self.get_direct_stop_checkbox()
    #     await direct_stop.is_visible()
    #     await direct_stop.click() 
        
    #     await self.wait_for_loaded_state()

    #     await self.get_no_results_page()
    #     flight_info = await self.flight_data()
    #     flights_available = await self.get_flight_cards()
    #     for flights in flights_available:
    #         stops = await self.get_layover_count(flights)
    #         if not stops:
    #             pass
    #         else:
    #             return False
    #     return True
        
    # async def flight_one_stop (self) -> bool:
    #     one_stop = await self.get_one_stop_checkbox()
    #     await one_stop.is_visible()
    #     await one_stop.click() 
        
    #     await self.wait_for_loaded_state()

    #     flights_available = await self.get_flight_cards()
    #     for flights in flights_available:
    #         layover_loc = await self.get_layover_count(flights)
    #         if not layover_loc:
    #             break
    #         number_of_stops = int(await layover_loc.inner_text())
    #         print(number_of_stops)
            
    #         if number_of_stops >= 0:
    #             pass
    #         else:
    #             return False
    #     return True
    
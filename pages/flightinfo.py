from playwright.async_api import Page
from urllib.parse import urlparse, parse_qs
from pages.basepage import BasePage

class FlightInfo(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    # Getters for UI elements
    async def get_search_departure_loc(self):
        return await self.get_element("//div[@data-testid='flight-origin-text-search']//input[@role='combobox']")

    async def get_search_arrival_loc(self):
        return await self.get_element("//div[@data-testid='flight-destination-text-search']//input[@role='combobox']")

    async def get_search_calender_departure(self):
        return await self.get_element("//div[@data-testid='date-picker-container']")

    async def get_search_departure_date(self):
        return await self.get_element(
            "//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') "
            "and contains(@class, 'filled') and contains(@class, 'Calendar__startDate--3vDzR')]/div[@data-selenium-date]"
        )

    async def get_search_calender_arrival(self):
        return await self.get_element("//button[@data-testid='arrival-date-input']")

    async def get_search_return_date(self):
        return await self.get_element(
            "//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') "
            "and contains(@class, 'filled') and contains(@class, 'Calendar__endDate--1j6dD')]/div[@data-selenium-date]"
        )

    async def get_search_passengers(self):
        return await self.get_element("//div[@data-element-name='flight-occupancy']")

    async def get_search_adults(self):
        return await self.get_element("//p[@data-component='adults-count']")

    async def get_search_children(self):
        return await self.get_element("//p[@data-component='children-count']")

    async def get_search_infants(self):
        return await self.get_element("//p[@data-component='infants-count']")

    async def get_search_cabin_type(self):
        return await self.get_element("//div[@data-element-name='flight-cabin-class']//p[@class='sc-jsMahE sc-kFuwaP bEtAca gEKgFh']")

    async def get_flight_cards(self):
        return await self.get_elements("//div[@data-testid='web-refresh-flights-card']")

    async def get_flight_carrier(self, flight):
        return await self.get_element_child(flight, "//div[@data-testid='flightCard-flight-detail']//p[@class='sc-jsMahE sc-kFuwaP bEtAca ftblUM']")
    
    async def get_flight_duration(self, flight):
        return await self.get_element_child(flight, "//div[@data-testid='flightCard-flight-detail']//span[@data-testid='duration']")
    
    async def get_flight_price(self, flight):
        return await self.get_element_child(flight, "//span[@data-element-name='flight-price-breakdown']//span[@class='sc-jsMahE sc-kFuwaP bEtAca kkhXWj']")
    
    async def get_flight_currency(self, flight):
        return await self.get_element_child(flight, "//span[@data-element-name='flight-price-breakdown']//span[@class='sc-jsMahE sc-kFuwaP brYcTc bpqEor']")
    
    async def validate_search(self, search_url):
        # Parse URL and extract search parameters
        parsed_url = urlparse(search_url)
        query_params = parse_qs(parsed_url.query)

        url_departure = query_params.get("departureFrom", [""])[0]
        url_arrival = query_params.get("arrivalTo", [""])[0]
        url_departure_date = query_params.get("departDate", [""])[0]
        url_return_date = query_params.get("returnDate", [""])[0]
        url_cabin_type = query_params.get("cabinType", [""])[0]
        url_adults = query_params.get("adults", [""])[0]
        url_children = query_params.get("children", "0")[0]
        url_infants = query_params.get("infants", "0")[0]

        print("Extracted from URL:")
        print("Departure:", url_departure)
        print("Arrival:", url_arrival)
        print("Departure Date:", url_departure_date)
        print("Return Date:", url_return_date)
        print("Cabin Type:", url_cabin_type)
        print("Adults:", url_adults)
        print("Children:", url_children)
        print("Infants:", url_infants)

        # Extract values from UI
        search_departure = await (await self.get_search_departure_loc()).get_attribute("value")
        search_arrival = await (await self.get_search_arrival_loc()).get_attribute("value")

        await (await self.get_search_calender_departure()).click()
        search_selected_departure_date = await (await self.get_search_departure_date()).get_attribute("data-selenium-date")

        await (await self.get_search_calender_arrival()).click()
        search_selected_return_date = await (await self.get_search_return_date()).get_attribute("data-selenium-date")

        await (await self.get_search_passengers()).click()
        adults_count = await (await self.get_search_adults()).inner_text()
        children_count = await (await self.get_search_children()).inner_text()
        infants_count = await (await self.get_search_infants()).inner_text()
        cabin_type = await (await self.get_search_cabin_type()).inner_text()

        print("Extracted from UI:")
        print("Departure:", search_departure)
        print("Arrival:", search_arrival)
        print("Departure Date:", search_selected_departure_date)
        print("Return Date:", search_selected_return_date)
        print("Cabin Type:", cabin_type)
        print("Adults:", adults_count)
        print("Children:", children_count)
        print("Infants:", infants_count)

        # Assertions
        assert url_departure in search_departure, f"Departure mismatch: {url_departure} != {search_departure}"
        assert url_arrival in search_arrival, f"Arrival mismatch: {url_arrival} != {search_arrival}"
        assert url_departure_date == search_selected_departure_date, f"Departure date mismatch: {url_departure_date} != {search_selected_departure_date}"
        assert url_return_date == search_selected_return_date, f"Return date mismatch: {url_return_date} != {search_selected_return_date}"
        assert url_cabin_type in cabin_type, f"Cabin type mismatch: {url_cabin_type} != {cabin_type}"
        assert url_adults == adults_count, f"Adults count mismatch: {url_adults} != {adults_count}"
        assert url_children == children_count, f"Children count mismatch: {url_children} != {children_count}"
        assert url_infants == infants_count, f"Infants count mismatch: {url_infants} != {infants_count}"


    async def flight_data(self):

        # check all flight options and store headings in 2D array
        flight_loc = await self.get_flight_cards()
        flight_data_2d = [["Carrier", "Duration", "Price"]]

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
            
            # appends data in array under respective headers
            flight_data_2d.append(
                [carrier.strip(), duration.strip(), f"{price.strip()} {currency.strip()}"])

        return flight_data_2d

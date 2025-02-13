from playwright.async_api import Page
from utils.common import PlaywrightHelper
from urllib.parse import urlparse, parse_qs


class test_flightInfo:
    def __init__(self, page: Page): # This is so we dont have to pass page everytime
        self.page = page            # stores page value in instance created 
        self.helper = PlaywrightHelper(page)
  

    async def validate_search (self, search_url):
        
        await self.page.wait_for_selector("//div[@data-testid='flight-search-box']")
        parsed_url = urlparse(search_url)
        query_params = parse_qs(parsed_url.query)

        url_departure = query_params.get("departureFrom", [""])[0]
        url_arrival = query_params.get("arrivalTo",[""])[0]
        url_departure_date = query_params.get("departureDate",[""])[0]
        url_return_date = query_params.get("returnDate", [""])[0]  
        url_passengers = query_params.get("adults", [""])[0] 
        url_cabin_type = query_params.get("cabinType", [""])[0]  
        print("Departure:", url_departure)
        print("Arrival:", url_arrival)
        print("Departure Date:", url_departure_date)
        print("Return Date:", url_return_date)
        print("Cabin Type:", url_cabin_type)
        print("Adults:", url_passengers)

        search_departure_loc = await self.helper.get_element("//input[@aria-controls='06370d9f01272']")
        search_departure = await search_departure_loc.get_attribute("value")

        search_arrival_loc = await self.helper.get_element("//input[@aria-controls='aa65a3abdd984']")
        search_arrival = await search_arrival_loc.get_attribute("value")

        search_calender_departure = await self.helper.get_element("//button[@data-testid='departure-date-input']")
        await search_calender_departure.click()
        search_departure_date = await self.helper.get_element("//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') and contains(@class, 'filled') and contains(@class, 'Calendar__startDate--3vDzR')]/div[@data-selenium-date]")
        search_selected_departure_date = await search_departure_date.get_attribute("data-selenium-date")

        search_calender_arrival = await self.helper.get_element("//button[@data-testid='arrival-date-input']")
        await search_calender_arrival.click()
        search_return_date = await self.helper.get_element(
        "//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') and contains(@class, 'filled') and contains(@class, 'Calendar__endDate--1j6dD')]/div[@data-selenium-date]")        
        search_selected_arrival_date = await search_return_date.get_attribute("data-selenium-date")

        search_cabin_type = await self.helper.get_element("selector_for_cabin").inner_text()
        search_adults = await self.helper.get_element("selector_for_adults").inner_text()

    async def flight_data(self):
        await self.page.wait_for_selector("//div[@data-testid='web-refresh-flights-card']")
        flights = await self.helper.get_element("//div[@data-testid='web-refresh-flights-card']") # check all flight options
        count = await flights.count()   # get count
        print(f"Found {count} flights")
        flight_data = []
        

        for i in range (count):
            flight = flights.nth(i)
            text = await flight.inner_text()
            print(f"Flight {i+1}:\n{text}\n{'-'*80}")
            flight_data.append(text)
        return flight_data
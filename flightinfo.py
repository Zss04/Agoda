from playwright.async_api import Page
from utils.common import PlaywrightHelper
from urllib.parse import urlparse, parse_qs


class test_flightInfo:
    def __init__(self, page: Page):  # This is so we dont have to pass page everytime
        self.page = page            # stores page value in instance created
        self.helper = PlaywrightHelper(page)

    async def validate_search(self, search_url):

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

        search_departure_loc = await self.helper.get_element(
            "//div[@data-testid='flight-origin-text-search']//input[@role='combobox']"

        )
        search_departure = await search_departure_loc.get_attribute("value")

        search_arrival_loc = await self.helper.get_element(
            "//div[@data-testid='flight-destination-text-search']//input[@role='combobox']"
        )
        search_arrival = await search_arrival_loc.get_attribute("value")

        search_calender_departure = await self.helper.get_element(
            "//div[@data-testid='date-picker-container']"
        )
        await search_calender_departure.click()
        search_departure_date = await self.helper.get_element(
            "//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') "
            "and contains(@class, 'filled') and contains(@class, 'Calendar__startDate--3vDzR')]"
            "/div[@data-selenium-date]"
        )
        search_selected_departure_date = await search_departure_date.get_attribute(
            "data-selenium-date"
        )

        search_calender_arrival = await self.helper.get_element(
            "//button[@data-testid='arrival-date-input']"
        )
        await search_calender_arrival.click()
        search_return_date = await self.helper.get_element(
            "//div[contains(@class, 'DesktopCalendar-module__day--1Eu4R') "
            "and contains(@class, 'filled') and contains(@class, 'Calendar__endDate--1j6dD')]"
            "/div[@data-selenium-date]"
        )
        search_selected_return_date = await search_return_date.get_attribute(
            "data-selenium-date"
        )

        search_passengers = await self.helper.get_element("//div[@data-element-name='flight-occupancy']")
        await search_passengers.click()

        search_adults = await self.helper.get_element("//p[@data-component='adults-count']")
        adults_count = await search_adults.inner_text()

        search_children = await self.helper.get_element(
            "//p[@data-component='children-count']"
        )
        children_count = await search_children.inner_text()

        search_infants = await self.helper.get_element(
            "//p[@data-component='infants-count']"
        )
        infants_count = await search_infants.inner_text()

        search_cabin_type = await self.helper.get_element(
            "//div[@data-element-name='flight-cabin-class']//p[@class='sc-jsMahE sc-kFuwaP bEtAca gEKgFh']"
        )
        cabin_type = await search_cabin_type.inner_text()

        print("Extracted from UI:")
        print("Departure:", search_departure)
        print("Arrival:", search_arrival)
        print("Departure Date:", search_selected_departure_date)
        print("Return Date:", search_selected_return_date)
        print("Cabin Type:", cabin_type)
        print("Adults:", adults_count)
        print("Children:", children_count)
        print("Infants:", infants_count)

        assert url_departure in search_departure, (
            f"Departure mismatch: {url_departure} != {search_departure}"
        )
        assert url_arrival in search_arrival, (
            f"Arrival mismatch: {url_arrival} != {search_arrival}"
        )
        assert url_departure_date == search_selected_departure_date, (
            f"Departure date mismatch: {url_departure_date} != {search_selected_departure_date}"
        )
        assert url_return_date == search_selected_return_date, (
            f"Return date mismatch: {url_return_date} != {search_selected_return_date}"
        )
        assert url_cabin_type in cabin_type, f"Cabin type mismatch: {url_cabin_type} != {cabin_type}"
        assert url_adults == adults_count, f"Passenger count mismatch: {url_adults} != {adults_count}"
        assert url_children == children_count, f"Passenger count mismatch: {url_children} != {children_count}"
        assert url_infants == infants_count, f"Passenger count mismatch: {url_infants} != {infants_count}"

    async def flight_data(self):

        await self.page.wait_for_selector("//div[@data-testid='web-refresh-flights-card']")
        # check all flight options
        flight_loc = await self.helper.get_element("//div[@data-testid='web-refresh-flights-card']")
        flight_data_2d = [["Carrier", "Duration", "Price"]]

        for flight in flight_loc:
            # carrier_loc = await self.helper.get_element(flight, "//div[@data-testid='flightCard-flight-detail']//p[@class='sc-jsMahE sc-kFuwaP bEtAca ftblUM']")
            carrier_loc = await self.helper.get_element(
                "//div[@data-testid='flightCard-flight-detail']//p[@class='sc-jsMahE sc-kFuwaP bEtAca ftblUM']")
            carrier = await carrier_loc.inner_text()
            duration_loc = await self.helper.get_element(
                "//div[@data-testid='flightCard-flight-detail']//span[@data-testid='duration']")
            duration = await duration_loc.inner_text()
            price_loc = await self.helper.get_element(
                "//span[@data-element-name='flight-price-breakdown']//span[@class='sc-jsMahE sc-kFuwaP bEtAca kkhXWj']")
            price = await price_loc.inner_text()
            currency_loc = await self.helper.get_element(
                "//span[@data-element-name='flight-price-breakdown']//span[@class='sc-jsMahE sc-kFuwaP brYcTc bpqEor']")
            currency = await currency_loc.inner_text()

            flight_data_2d.append(
                [carrier.strip(), duration.strip(), f"{price.strip()} {currency.strip()}"])

        return flight_data_2d

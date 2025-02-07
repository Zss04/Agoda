import pytest
from datetime import datetime
from playwright.async_api import async_playwright
from common import PlaywrightHelper, roundTrip


@pytest.mark.asyncio
async def test_flight_booking(browser_and_page):

    page = browser_and_page
    helper = PlaywrightHelper(page)
    rt = roundTrip(page)

    # Go to Agoda website
    if page is None:
        pytest.fail("Page is None! Check fixture.")
    await page.goto("https://agoda.com")

    # Locate and click on Flights tab
    flight = await helper.get_element("//li[@id='tab-flight-tab']")
    if flight:
        await flight.click()
    else:
        pytest.fail("Flights tab not found")
    await rt.select_trip_type("roundTrip")
    await rt.select_airport("Jinnah International Airport", "Toronto Pearson International Airport")

    user_departure_date = datetime(2025, 2, 20)
    user_return_date = datetime(2025, 2, 25)
    await rt.select_date(user_departure_date, user_return_date)
    await rt.select_passengers_and_cabin(adults=3, children=2, infants=1, cabin="Business")

    search = await helper.get_element("//button[@data-test='SearchButtonBox']")
    if search:
        await search.click()
    else:
        pytest.fail("Search button not found!")

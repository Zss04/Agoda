import pytest
from playwright.async_api import async_playwright
from flightinfo import test_flightInfo

'''
@pytest.mark.asyncio
async def test_verify_search_results(page):
    # create an instance of trip options class
    page, search_url = page
    trip = test_flightInfo(page)  
    await page.goto(search_url["url"])
    await trip.validate_search(search_url["url"])
    print("search validated")
    return None '''


@pytest.mark.asyncio
async def test_flight_data(page):
    page, search_url = page
    trip = test_flightInfo(page)
    await page.goto(search_url["url"])
    store_flight_data = await trip.flight_data()
    print("Flights are visible")

    assert len(store_flight_data) > 0, "No flights found!"
    return store_flight_data
   
import pytest
from playwright.async_api import async_playwright
from pages.flightinfo import FlightInfo
from tabulate import tabulate


@pytest.mark.asyncio
async def test_verify_search_results(page_tuple):
    # create an instance of trip options class
    page, get_url = page_tuple
    trip = FlightInfo(page)
    await page.goto(get_url["url"])
    await trip.validate_search(get_url["url"])
    print("search validated")
    return None


@pytest.mark.asyncio
async def test_flight_data(page_tuple):
    page, get_url = page_tuple   # recieves tuple from page fixture
    trip = FlightInfo(page)    # creates instance  of flightinfo class
    await page.goto(get_url["url"])
    flight_data_2d = await trip.flight_data()  # Call flight_data on the instance

    print("\nFlight Data (Array):")
    # arranges all data in a table
    print(tabulate(flight_data_2d, headers="firstrow", tablefmt="grid"))
    assert len(flight_data_2d) > 0, "No flights found!"

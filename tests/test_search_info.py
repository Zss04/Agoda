import pytest
from playwright.async_api import async_playwright
from flightinfo import test_flightInfo
from tabulate import tabulate


@pytest.mark.asyncio
async def test_verify_search_results(page):
    # create an instance of trip options class
    page, search_url = page
    trip = test_flightInfo(page)  
    await page.goto(search_url["url"])
    await trip.validate_search(search_url["url"])
    print("search validated")
    return None 


@pytest.mark.asyncio
async def test_flight_data(page):
    page, search_url = page
    trip = test_flightInfo(page)
    await page.goto(search_url["url"])
    flight_data_2d = await trip.flight_data() # Call flight_data on the instance


    print("\nFlight Data (2D Array):")
    print(tabulate(flight_data_2d, headers="firstrow", tablefmt="grid"))
    assert len(flight_data_2d) > 0, "No flights found!"
   
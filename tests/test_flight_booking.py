import pytest
from datetime import datetime
from playwright.async_api import async_playwright
from roundtrip import test_roundTrip



@pytest.mark.asyncio
async def test_flight_booking(page):
    page, search_url = page
    rt = test_roundTrip(page)

    # Go to Agoda website and wait for logo
    await page.goto("https://agoda.com")
    await rt.agoda_image() 

    # Locate and click on Flights tab
    await rt.flights()
    await rt.select_trip_type("roundTrip")
    await rt.select_airport("Jinnah International Airport ", "Toronto Pearson International Airport")

    # fill in calender dates and select cabin and passengers
    user_departure_date = datetime(2025, 2, 22)
    user_return_date = datetime(2025, 2, 25)
    await rt.select_date(user_departure_date, user_return_date)
    await rt.select_passengers_and_cabin(adults=2, children=0, infants=0, cabin="Economy")
    
    #  validate results by waiting for results page
    await rt.results()
    search_url["url"] = page.url
    print(f"Stored search URL: {search_url['url']}")


    

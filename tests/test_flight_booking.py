import pytest
from pages.flight_frontdoor import test_roundTrip


@pytest.mark.asyncio
async def test_flight_booking(page_tuple):
    page, search_url = page_tuple
    rt = test_roundTrip(page)

    # Go to Agoda website and wait for logo
    await page.goto("https://agoda.com")
    await rt.wait_for_agoda_image()
    # Locate and click on Flights tab
    await rt.flights()
    await rt.flights_is_clicked()
    
    await rt.select_trip_type("roundTrip")
    await rt.select_airport("Jinnah International ", "toronto pearson")


    # fill in calender dates and select cabin and passengers
    await rt.select_date()
    await rt.select_passengers_and_cabin(adults=2, children=0, infants=0, cabin="Economy")
    
    #  validate results by waiting for results page
    assert rt.search_successful, "Search results were not found"
    search_url["url"] = page.url
    print(f"Stored search URL: {search_url['url']}")
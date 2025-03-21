import pytest
from pages.flight_frontdoor import test_roundTrip

@pytest.mark.asyncio
@pytest.mark.agoda
async def test_flight_booking(page_tuple):
    page, set_url = page_tuple
    rt = test_roundTrip(page)

    # Go to Agoda website and wait for logo
    await page.goto("https://agoda.com")
    await rt.wait_for_agoda_image()
    # Locate and click on Flights tab
    await rt.click_flights()
    await rt.flights_is_clicked()
    
    await rt.select_trip_type("roundTrip")
    await rt.set_departure_airport("LHE")
    await rt.set_arrival_airport("KHI")

    # fill in calender dates and select cabin and passengers
    await rt.set_date()
    await rt.set_passengers_and_cabin(adults=2, children=0, infants=0, cabin="Economy")
    
    #  validate results by waiting for results page
    assert rt.search_successful, "Search results were not found"
    set_url["url"] = page.url
    print(f"Stored search URL: {set_url['url']}")
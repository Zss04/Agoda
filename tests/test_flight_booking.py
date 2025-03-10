import pytest
from pages.Round_Trip import RoundTrip

@pytest.mark.asyncio
@pytest.mark.parametrize("departure_airport, arrival_airport , adults, children, infants, cabin",
                            [
                             ("Jinnah International Airport", "John F. Kennedy", 2 , 1, 0, "Business"),
                             ("Allama Iqbal International Airport", "Istanbul Airport", 1 , 0, 0, "Economy")
                            ])
async def test_flight_booking(page_tuple, departure_airport, arrival_airport, adults, children, infants, cabin):
    page, set_url = page_tuple
    rt = RoundTrip(page)

    # Go to Agoda website and wait for logo
    await page.goto("https://agoda.com")
    await rt.wait_for_agoda_image()
    # Locate and click on Flights tab
    await rt.click_flights()
    assert await rt.flights_is_clicked() == "true", "Flights tab was not clicked"

    await rt.select_roundtrip()
    assert await rt.is_round_trip_selected(), "Round trip was not selected"

    await rt.select_departure_airport(departure_airport)
    await rt.select_arrival_airport(arrival_airport)

    # fill in calender dates and select cabin and passengers
    await rt.set_departure_date()
    await rt.set_return_date()
    assert await rt.is_departure_date_selected(), "Departure date was not selected"
    assert await rt.is_return_date_selected(), "Return date was not selected"

    passengers_count = await rt.select_passengers_and_cabin(adults, children, infants, cabin)
    actual_passengers_count = await rt.passengers_and_cabin_count()
    assert actual_passengers_count == passengers_count, "Passengers and cabin count mismatch"

    await rt.search()
    #  validate results by waiting for results page
    assert await rt.search_successful(), "Search results were not found"
    set_url["url"] = page.url

import pytest
from pages.flight_options import FlightInfo
from tabulate import tabulate
from utils.logger_config import get_logger

logger = get_logger("test_flight_options")

@pytest.mark.asyncio
async def test_verify_search_results(page_tuple):
    # create an instance of trip options class
    page, get_url = page_tuple
    trip = FlightInfo(page)
    await page.goto(get_url["url"])
    assert await trip.validate_search(get_url["url"])
    logger.info("search validated")

    flight_data_2d = await trip.flight_data()  # Call flight_data on the instance
    logger.info("\nFlight Data (Array):")
    # arranges all data in a table
    logger.info(tabulate(flight_data_2d, headers="firstrow", tablefmt="grid"))
    assert len(flight_data_2d) > 0, "No flights found!"

@pytest.mark.asyncio
async def test_flight_stops(page_tuple):
    page, get_url = page_tuple
    trip = FlightInfo(page)
    await page.goto(get_url["url"])
    
    assert await trip.flight_direct_stop(), f"Non direct flights found in direct filter"
    assert await trip.flight_one_stop(), f"Non one stop flights found in one stop filter"
    # assert await trip.flight_two_plus_stop()

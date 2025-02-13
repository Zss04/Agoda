import pytest
from playwright.async_api import async_playwright
from flightinfo import Trip_options

@pytest.mark.asyncio
async def test_verify_search_results(page):
    if hasattr(page, "search_results_url"):
        search_results_url = page.search_results_url
    else:
        pytest.fail("No search URL found from the previous test")

    # ✅ Continue on the same page
    print(f"Continuing from previous search URL: {search_results_url}")

    assert "Jinnah-International-Airport" in search_results_url
    assert "Toronto-Pearson-International-Airport" in search_results_url
    assert "adults=2" in search_results_url
    assert "children=0" in search_results_url
    assert "cabin=Economy" in search_results_url

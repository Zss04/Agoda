import pytest
from datetime import datetime
from playwright.async_api import async_playwright

print("Hello, world")
        
async def get_element(page, selector, timeout=5000):
    try:
        await page.wait_for_selector(selector,timeout=timeout)
        return page.locator(selector)
    except Exception as e:
        print(f"Warning: Did not find element '{selector}' - {e}")
        return None


@pytest.mark.asyncio
async def test_flight_booking():
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
    
        # Go to Agoda website
        await page.goto("https://agoda.com")
        
        # Locate and click on Flights tab
        flight = await get_element(page, "//li[@id='tab-flight-tab']")
        if flight:
            await flight.click()
        else:
            pytest.fail("Flights tab not found")


        # One way or round trip
        async def select_trip_type(page, trip_type):
            valid_trip_types = ["roundTrip", "oneWay"]
            if trip_type not in valid_trip_types:
                pytest.fail(f"Invalid trip type: {trip_type}")
                return
            trip_type_locator = await get_element(page, f"//button[@data-component='flight-search-type-{trip_type}']")
            if trip_type_locator:
                await trip_type_locator.click()
            else:
                pytest.fail("Cannot find trip type {trip_type} button")

        await select_trip_type(page, "roundTrip")
        
        # Making a function to select Airport
        async def select_airport(field_id, Airport_name):

            await page.fill(field_id, Airport_name)
            await page.wait_for_timeout(1000)    
            airport_options = page.locator( 
                "//li[@class='Suggestion__categoryName_item']"
            )
            if not airport_options:
                pytest.fail("cannot find airport options list")
                
            count = await airport_options.count()
            for i in range (count):
                option_text = await airport_options.nth(i).text_content()

                if Airport_name.lower() in option_text.lower() :
                    await airport_options.nth(i).click()
                    return
            if count > 0 :
                await airport_options.first.click()
            else: 
                pytest.fail("No airport with this name can be found")
                
        
        await select_airport("#flight-origin-search-input", "Jinnah International Airport")
        await select_airport("#flight-destination-search-input", "Toronto Pearson International Airport")
    
        # Select date for departure and return
        async def select_date (page, departure_date, return_date):
            
            departure_date_str = departure_date.strftime("%Y-%m-%d")
            return_date_str = return_date.strftime("%Y-%m-%d")

            departure_locator =  await get_element(page, f"//span[@data-selenium-date='{departure_date_str}']", 10000)
            if departure_locator:
                await departure_locator.click()
            else:
                pytest.fail(f"Departure date '{departure_date_str}' not found!")
            
            return_locator =  await get_element(page, f"//span[@data-selenium-date='{return_date_str}']", 10000)
            if return_locator:
                await return_locator.click()
            else:
                pytest.fail(f" Return date '{return_date_str}' not found!")
            

        user_departure_date = datetime(2025, 2, 5)
        user_return_date = datetime(2025, 2, 10)
        await select_date(page, user_departure_date, user_return_date)

        async def select_passengers_and_cabin(page, adults=1, children=0, infants=0, cabin="Economy"):
            categories = {
                "adult": adults,
                "children": children,
                "infant": infants
            }

            for category, target_count in categories.items():
                increase_btn = await get_element(page, f"//button[@data-element-name='flight-occupancy-{category}-increase']")
                decrease_btn = await get_element(page, f"//button[@data-element-name='flight-occupancy-{category}-decrease']")
                current_category_locator = await get_element(page, f"//span[@data-component='flight-occupancy-{category}-number']")
                current_count_text = await current_category_locator.text_content()
                current_count = int(current_count_text)
        
                print(f"Current {category}s: {current_count}, Target: {target_count}")

                 # Adjust count
                if target_count > current_count:
                    for _ in range(target_count - current_count):
                        await increase_btn.click()
                elif target_count < current_count:
                    for _ in range(current_count - target_count):
                        await decrease_btn.click()

            # select cabin class
            cabin_locator = await get_element(page, f"//button[@data-component ='flight-search-cabinClass-{cabin}']")
            if cabin_locator:
                await cabin_locator.click()
            else: 
                pytest.fail("Cannot find cabin classes")

        await select_passengers_and_cabin(page, adults=3, children=2, infants=1, cabin="Business")

        # Locate and click on Search button
        search = await get_element(page, "//button[@data-test='SearchButtonBox']")
        if search:
            await search.click()
        else:
            pytest.fail("❌ Search button not found!")

        # Validating test reults
        # results = await get_element(page, "//div[contains(@data-component ='flight-calendar-search-panel')]")
        # if results:
        #     assert await results.is_visible(), "Search results are not visible"
        # else: 
        #     pytest.fail("Flight search results not found")
    
        await page.pause()
        
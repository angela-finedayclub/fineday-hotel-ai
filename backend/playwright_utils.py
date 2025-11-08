def search_hotels(page, city, hotel, checkin, checkout, people):
    results = []
    page.goto("https://hotel.eztravel.com.tw/?p=oversea")
    page.wait_for_timeout(3000)
    # 這裡僅示範，實際可根據 ezTravel 的 selector 微調
    hotels = page.query_selector_all("div.HotelListItemstyle__Name-sc-1yo1bvo-3")
    prices = page.query_selector_all("div.HotelListItemstyle__Price-sc-1yo1bvo-13")
    for i in range(min(len(hotels), len(prices))):
        results.append({
            "site": "ezTravel",
            "hotel": hotels[i].inner_text().strip(),
            "price": prices[i].inner_text().strip(),
            "room_type": "N/A",
            "link": page.url
        })
    return results

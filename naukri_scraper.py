from playwright.sync_api import sync_playwright

def scrape_naukri(query, limit=20):

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        search_query = query.replace(" ", "-")

        url = f"https://www.naukri.com/{search_query}-jobs"

        page.goto(url, timeout=60000)

        page.wait_for_timeout(5000)

        cards = page.query_selector_all(".srp-jobtuple-wrapper")

        for card in cards[:limit]:

            try:
                title = card.query_selector(".title").inner_text()
            except:
                title = ""

            try:
                company = card.query_selector(".comp-name").inner_text()
            except:
                company = ""

            try:
                location = card.query_selector(".locWdth").inner_text()
            except:
                location = ""

            jobs.append({
                "Source": "Naukri",
                "Title": title,
                "Company": company,
                "Location": location,
                "Summary": "",
            })

        browser.close()

    return jobs
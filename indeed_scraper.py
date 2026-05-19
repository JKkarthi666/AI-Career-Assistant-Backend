from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_indeed(query, location="India", limit=20):

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        url = f"https://in.indeed.com/jobs?q={query}&l={location}"

        page.goto(url, timeout=60000)

        page.wait_for_timeout(5000)

        cards = page.query_selector_all(".job_seen_beacon")

        for card in cards[:limit]:

            try:
                title = card.query_selector("h2").inner_text()
            except:
                title = ""

            try:
                company = card.query_selector(".companyName").inner_text()
            except:
                company = ""

            try:
                location = card.query_selector(".companyLocation").inner_text()
            except:
                location = ""

            try:
                summary = card.query_selector(".job-snippet").inner_text()
            except:
                summary = ""

            jobs.append({
                "Source": "Indeed",
                "Title": title,
                "Company": company,
                "Location": location,
                "Summary": summary,
            })

        browser.close()

    return jobs
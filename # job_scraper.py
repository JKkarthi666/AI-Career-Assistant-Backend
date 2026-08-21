import asyncio
import logging
from playwright.async_api import async_playwright

logger = logging.getLogger("job_engine.scrapers")

async def scrape_naukri(query: str, limit: int = 20) -> list[dict]:
    jobs = []
    search_query = query.replace(" ", "-")
    url = f"https://www.naukri.com/{search_query}-jobs"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0")
        page = await context.new_page()
        
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_selector(".srp-jobtuple-wrapper", timeout=15000)
            cards = await page.query_selector_all(".srp-jobtuple-wrapper")
            
            for card in cards[:limit]:
                try:
                    title_el = await card.query_selector(".title")
                    company_el = await card.query_selector(".comp-name")
                    location_el = await card.query_selector(".locWdth")
                    
                    jobs.append({
                        "Source": "Naukri",
                        "Title": await title_el.inner_text() if title_el else "N/A",
                        "Company": await company_el.inner_text() if company_el else "N/A",
                        "Location": await location_el.inner_text() if location_el else "N/A",
                        "Summary": "N/A",
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse Naukri job card: {e}")
        except Exception as e:
            logger.error(f"Naukri scraping failed for {query}: {e}")
        finally:
            await browser.close()
            
    return jobs

async def scrape_indeed(query: str, location: str = "India", limit: int = 20) -> list[dict]:
    jobs = []
    url = f"https://in.indeed.com/jobs?q={query}&l={location}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0")
        page = await context.new_page()
        
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_selector(".job_seen_beacon", timeout=15000)
            cards = await page.query_selector_all(".job_seen_beacon")
            
            for card in cards[:limit]:
                try:
                    title_el = await card.query_selector("h2")
                    company_el = await card.query_selector(".companyName")
                    loc_el = await card.query_selector(".companyLocation")
                    sum_el = await card.query_selector(".job-snippet")
                    
                    jobs.append({
                        "Source": "Indeed",
                        "Title": await title_el.inner_text() if title_el else "N/A",
                        "Company": await company_el.inner_text() if company_el else "N/A",
                        "Location": await loc_el.inner_text() if loc_el else "N/A",
                        "Summary": await sum_el.inner_text() if sum_el else "N/A",
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse Indeed job card: {e}")
        except Exception as e:
            logger.error(f"Indeed scraping failed for {query}: {e}")
        finally:
            await browser.close()
            
    return jobs

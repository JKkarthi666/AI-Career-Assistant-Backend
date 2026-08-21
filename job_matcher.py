import pandas as pd
import asyncio
from typing import List, Dict
from pathlib import Path
from scrapers import scrape_indeed, scrape_naukri
from config import OUTPUT_DIR, logger

async def find_jobs(skills: List[str]) -> List[Dict]:
    all_jobs = []
    
    # Create a list of coroutines for all skills across both platforms
    tasks = []
    for skill in skills:
        tasks.append(scrape_indeed(skill))
        tasks.append(scrape_naukri(skill))
        
    # Execute all scraping tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Scraping task failed: {result}")
        elif isinstance(result, list):
            all_jobs.extend(result)
            
    return all_jobs

def export_excel(jobs: List[Dict]) -> str:
    if not jobs:
        return ""
        
    df = pd.DataFrame(jobs)
    df.drop_duplicates(subset=['Title', 'Company'], inplace=True)
    
    output_path = OUTPUT_DIR / "matched_jobs.xlsx"
    df.to_excel(output_path, index=False)
    
    logger.info(f"Exported {len(df)} jobs to {output_path}")
    return str(output_path)

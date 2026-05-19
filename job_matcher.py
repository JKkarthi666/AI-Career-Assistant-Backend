from scrapers.indeed_scraper import scrape_indeed
from scrapers.naukri_scraper import scrape_naukri
import pandas as pd

def find_jobs(skills):

    all_jobs = []

    for skill in skills:

        indeed_jobs = scrape_indeed(skill)
        naukri_jobs = scrape_naukri(skill)

        all_jobs.extend(indeed_jobs)
        all_jobs.extend(naukri_jobs)

    return all_jobs


def export_excel(jobs):

    df = pd.DataFrame(jobs)

    df.drop_duplicates(inplace=True)

    output = "outputs/jobs.xlsx"

    df.to_excel(output, index=False)

    return output
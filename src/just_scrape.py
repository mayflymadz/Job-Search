''' Job Finder Tool
    Author -- mayflymadz (Madison Beazer)
    3/18/2025

    This will just scrape LinkedIn and save them in a yaml file. I want to get the AI analiysis working, but for now this is what we've got
'''

import pathlib
import requests
import json
import yaml
from bs4 import BeautifulSoup

import job_scraper
import job_loader
import ai_analyzer


def main():
    # Pull up the loader and scraper
    loader = job_loader.JobLoader("job-boards.yml")
    scraper = job_scraper.JobScraper()
    
    # Scrape each job board and put it in a list for the loader to save
    job_listings = []
    for board in loader.boards:
        job_listings.extend(scraper.scrape(board))
    loader.save_job_listings(job_listings)

if __name__ == "__main__":
    main()

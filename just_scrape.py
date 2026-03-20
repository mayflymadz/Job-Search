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
    print("Hello from job-tool!")
    loader = job_loader.JobLoader("job-boards.yml")
    scraper = job_scraper.JobScraper()
    
    # Comment this out when testing the AI analyzer without scraping
    for board in loader.boards:
        scraper.scrape(board)



if __name__ == "__main__":
    main()

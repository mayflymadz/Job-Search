''' Job Finder Tool
    Author -- mayflymadz (Madison Beazer)
    3/18/2025

    Automating my job search in 2026. Thank you HP site closure for motivating me code at home again lol
'''

import pathlib
import requests
import json
import yaml
from bs4 import BeautifulSoup

import job_scraper
import job_loader


def main():
    print("Hello from job-tool!")
    loader = job_loader.JobLoader("job-boards.yml")
    scraper = job_scraper.JobScraper()
    for board in loader.boards:
        scraper.scrape(board)


if __name__ == "__main__":
    main()

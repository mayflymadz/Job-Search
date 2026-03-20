''' Job Finder Tool
    Author -- mayflymadz (Madison Beazer)
    3/18/2025

    Automating my job search in 2026. Thank you HP site closure for motivating me code at home again lol

    NOTE: this file is for working on my AI anlasys of the the job listings. It isn't fully working right now
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
    # for board in loader.boards:
    #     scraper.scrape(board)

    # Now that we've scraped the job listings, let's see what the bot thinks
    script_dir = pathlib.Path(__file__).parent
    bot = ai_analyzer.AIAnalyzer(script_dir / "job_listings.yml", pathlib.Path("user.yml"))
    analysis = bot.analyze_listings()
    print("AI Analysis of Job Listings:")
    print(analysis)

if __name__ == "__main__":
    main()

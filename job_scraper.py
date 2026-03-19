
import pathlib
import requests
import json
import yaml
from bs4 import BeautifulSoup

class JobScraper:
    """Class for scraping LinkedIn and Indeed for job postings."""

    def scrape(self, board: dict) -> None:
        """Scrape data from a job board."""
        name = board.get("name", "Unknown")
        link = board.get("link", "")
        if not link:
            print(f"No link provided for {name}.")
            return

        print(f"Scraping {name} at {link}...")
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Start with LinkedIn
            if board.get("name").lower() == "linkedin":
                self._scrape_linkedin(soup)
            # Then try Indeed         
            elif board.get("name").lower() == "indeed":
                self._scrape_indeed(soup)
            else:
                print(f"I haven't implemented scraping for: {name}")

            

        except requests.RequestException as e:
            print(f"Error fetching {name}: {e}")
    
    def _scrape_linkedin(self, soup: BeautifulSoup) -> None:
        """Scrape LinkedIn for job postings based on preferences."""
        print("Scraping LinkedIn... (not implemented yet)")
        job_urls = []

        job_url_elements = soup.select("[data-tracking-control-name='public_jobs_jserp-result_search-card']")
        for job_url_element in job_url_elements:
            job_url = job_url_element["href"]
            print(f"Found job URL: {job_url}")
            job_urls.append(job_url)


    def _scrape_indeed(self, soup: BeautifulSoup) -> None:
        """Scrape Indeed for job postings based on preferences."""
        print("Scraping Indeed... (not implemented yet)")




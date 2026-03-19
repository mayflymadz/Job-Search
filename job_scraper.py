
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

        # gotta get the job urls first
        job_url_elements = soup.select("[data-tracking-control-name='public_jobs_jserp-result_search-card']")
        for job_url_element in job_url_elements:
            job_url = job_url_element["href"]
            print(f"Found job URL: {job_url}")
            job_urls.append(job_url)

        # save individual job listings for AI parsing later
        job_listings = []
        for job_url in job_urls:
            response = requests.get(job_url, timeout=10)
            job_soup = BeautifulSoup(response.text, 'html.parser')

            # Here's an example of what the title header looks like: <h1 class="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"> Job Title </h1>
            # We should just be looking for an h1 tag, but we can look fo rthis specifically just in case
            title_elem = (
                job_soup.select_one(".topcard__title")
                or job_soup.select_one(".top-card-layout__title")
                or job_soup.select_one("h1")
            )
            title = "No title found"
            if title_elem:
                title = title_elem.get_text(strip=True)

            # Same kind of thing for the company name: <a class="topcard__org-name-link topcard__flavor--black-link" data-tracking-control-name="public_jobs_topcard-org-name" data-tracking-will-navigate="" href="https://www.linkedin.com/company/autopay?trk=public_jobs_topcard-org-name" rel="noopener" target="_blank"> Company </a>            
            company_elem = job_soup.select_one(
                ".topcard__org-name-link, .topcard__flavor--black-link"
            )
            company = "No company found"
            if company_elem:
                company = company_elem.get_text(strip=True)
            
            # Location: <span class="topcard__flavor topcard__flavor--bullet"> Location </span>
            location_elem = job_soup.select_one(".topcard__flavor--bullet")
            location = "No location found"
            if location_elem:
                location = location_elem.get_text(strip=True)
            
            # Description: <div class="description__text description__text--rich" data-tracking-control-name="public_jobs_jobdetails_description">
            description_elem = job_soup.select_one(".description__text")
            description = "No description found"
            if description_elem:
                description = description_elem.get_text(strip=True)


            job_details = {
                "url": job_url,
                "title": title,
                "company": company,
                "location": location,
                "description": description
            }
            job_listings.append(job_details)

        # Save the job listings to a yaml file for AI parsing later
        self._save_job_listings(job_listings)
        print(f"Scraped {len(job_listings)} job listings from LinkedIn. Hopefully it worked!")

    def _scrape_indeed(self, soup: BeautifulSoup) -> None:
        """Scrape Indeed for job postings based on preferences."""
        print("Scraping Indeed... (not implemented yet)")

    def _save_job_listings(self, job_listings: list[dict]) -> None:
        """Throw the job listing in a yaml file. Note, the 'w' option will overwrite the file each time."""
        try:
            output_path = pathlib.Path("job_listings.yml")
            with output_path.open("w", encoding="utf-8") as file:
                yaml.dump({"job-listings": job_listings}, file, allow_unicode=True)
            print(f"Saved {len(job_listings)} job listings to {output_path}")
        except Exception as e:
            print(f"Error saving job listings: {e}")

    



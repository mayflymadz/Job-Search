
import pathlib
import requests
import json
import yaml
from bs4 import BeautifulSoup

class JobScraper:
    """Class for scraping LinkedIn and Indeed for job postings."""
    def scrape(self, board: dict) -> list:
        """Scrape data from a job board."""
        name = board.get("name", "Unknown")
        link = board.get("link", "")
        if not link:
            print(f"No link provided for {name}.")
            return []
        
        all_job_listings = []

        print(f"Scraping {name} at {link}...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        }

        try:
            response = requests.get(link, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Start with LinkedIn
            board_type = board.get("type", "").lower()
            if board_type == "linkedin":
                all_job_listings.extend(self._scrape_linkedin(soup))
            # Then try Indeed         
            elif board_type == "indeed":
                all_job_listings.extend(self._scrape_indeed(soup))
            else:
                print(f"I haven't implemented scraping for: {name}")

        except requests.HTTPError as e:
            print(f"HTTP error fetching {name}: {e}")
        except requests.RequestException as e:
            print(f"Network error fetching {name}: {e}")
        except Exception as e:
            print(f"Unexpected error fetching {name}: {e}")

        # Save the job listings to a yaml file for analysis.
        return all_job_listings
    
    def _scrape_linkedin(self, soup: BeautifulSoup) -> list:
        """Scrape LinkedIn for job postings."""
        print("Scraping LinkedIn...")
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

        print(f"Scraped {len(job_listings)} job listings from LinkedIn. Hopefully it worked!")
        return job_listings

    def _scrape_indeed(self, soup: BeautifulSoup) -> None:
        """Scrape Indeed for job postings based on preferences."""
        print("Scraping Indeed... (not implemented yet)")


    



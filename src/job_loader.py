import pathlib
import yaml


class JobLoader:
    """Class for loading job data from a file and saving the scraped job listings to a yaml file for analysis."""
    def __init__(self, boards_path: str = "job-boards.yml", output_path: str = "job_listings.yml"):
        self.boards_path = pathlib.Path(boards_path)
        self.output_path = pathlib.Path(output_path)
        self.boards = self._load_job_boards()

    def _load_job_boards(self) -> list[dict]:
        if not self.boards_path.exists():
            return None

        with self.boards_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
        
        print(f"Loaded job boards: {data.get('job-boards', [])}")

        return data.get("job-boards", [])

    
    def save_job_listings(self, job_listings: list[dict]) -> None:
        """Throw the job listing in a yaml file. Note, the 'w' option will overwrite the file each time, so you want to
        do this after you've scraped all the job boards, not after each one."""
        try:
            output_path = pathlib.Path(self.output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w", encoding="utf-8") as file:
                yaml.dump({"job-listings": job_listings}, file, allow_unicode=True)
            print(f"Saved {len(job_listings)} job listings to {output_path}")
        except Exception as e:
            print(f"Error saving job listings: {e}")
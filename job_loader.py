import pathlib
import yaml


class JobLoader:
    """Class for loading job data from a file."""
    def __init__(self, boards_path: str = "job-boards.yml"):
        self.boards_path = pathlib.Path(boards_path)
        self.boards = self._load_job_boards()

    def _load_job_boards(self) -> list[dict]:
        if not self.boards_path.exists():
            return None

        with self.boards_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
        
        print(f"Loaded job boards: {data.get('job-boards', [])}")

        return data.get("job-boards", [])
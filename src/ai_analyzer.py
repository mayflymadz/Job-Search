import yaml
import pathlib
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer

class AIAnalyzer:
    def __init__(self, job_listings_path: pathlib.Path, user_preferences_path: pathlib.Path):
        self.job_listings_path = job_listings_path
        self.user_preferences_path = user_preferences_path
        # Look, they've got a free pipeline :)
        self.checkpoint = "sentence-transformers/all-MiniLM-L6-v2"  
        # self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)  # Not needed for SentenceTransformer

    def analyze_listings(self) -> str:
        """We are going to start with a free model and then upgrade to Gemini or Claude if we aren't happy with the results.
        I'm not paying for this thing, ya know?"""''
        # Load job listings and user preferences
        with self.job_listings_path.open("r", encoding="utf-8") as file:
            job_listings = yaml.safe_load(file).get("job-listings", [])
        with self.user_preferences_path.open("r", encoding="utf-8") as file:
            user_preferences = yaml.safe_load(file)

        if not job_listings:
            return "No job listings found to analyze."

        results = []
        
        for job in job_listings:
            result = self._analyze_with_huggingface(job)
            results.append(result)

        return results
    
    def _analyze_with_huggingface(self, text: str) -> str:
        """this looks kinda hard, lets try it
        https://huggingface.co/sentence-transformers"""
        model = SentenceTransformer(self.checkpoint)
        sentences = text
        embeddings = model.encode(sentences)
        return embeddings
        




















    
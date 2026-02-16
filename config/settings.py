"""
Central configuration — URLs, paths, and constants used across the project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Project root (one level above this file's directory)
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Target website
# ---------------------------------------------------------------------------
OPINION_URL = "https://elpais.com/opinion/"
MAX_ARTICLES = 5

# ---------------------------------------------------------------------------
# Output directories
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
IMAGE_DIR = os.path.join(OUTPUT_DIR, "article_images")
ARTICLES_DIR = os.path.join(OUTPUT_DIR, "articles")
JSON_OUTPUT = os.path.join(OUTPUT_DIR, "articles.json")

# ---------------------------------------------------------------------------
# Translation — Rapid Translate Multi Traduction API
# ---------------------------------------------------------------------------
RAPID_API_KEY = os.getenv("RAPID_API_KEY", "")
RAPID_TRANSLATE_URL = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
RAPID_TRANSLATE_HOST = "rapid-translate-multi-traduction.p.rapidapi.com"

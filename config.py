import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Get configuration from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"
FLASK_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = FLASK_ENV == "development"

# Currency API URLs
CURRENCY_API_URLS = [
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json",
    "https://latest.currency-api.pages.dev/v1/currencies/{base}.json"
]

# Common currency mappings to help with currency identification
CURRENCY_MAPPING = {
    # English
    "dollar": "USD", "dollars": "USD", "usd": "USD", "us dollar": "USD", "american dollar": "USD",
    "euro": "EUR", "euros": "EUR", "eur": "EUR",
    "pound": "GBP", "pounds": "GBP", "gbp": "GBP", "british pound": "GBP",
    "egyptian pound": "EGP", "egypt pound": "EGP", 
    # Arabic
    "دولار": "USD", "دولار أمريكي": "USD",
    "يورو": "EUR",
    "جنيه": "EGP", "جنيه مصري": "EGP",  # Default to Egyptian pound for Arabic
    "جنيه استرليني": "GBP", "استرليني": "GBP",
    # Add more mappings as needed
}

# Logging configuration
LOG_FOLDER = BASE_DIR / "logs"
LOG_FILENAME = LOG_FOLDER / "app.log"
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_ROTATION = "10 MB"
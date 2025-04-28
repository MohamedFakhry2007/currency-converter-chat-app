"""Main entry point for the Currency Converter application."""
import nest_asyncio
from loguru import logger

from app import create_app

# Apply the asyncio patch for compatibility with Flask and async operations
nest_asyncio.apply()

# Initialize logging
logger.info("Starting Currency Converter Application")

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
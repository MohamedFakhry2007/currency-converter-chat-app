"""Initialize the Flask application."""
import os
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from loguru import logger

import config


def setup_logging():
    """Configure application logging."""
    # Create log directory if it doesn't exist
    os.makedirs(config.LOG_FOLDER, exist_ok=True)
    
    # Configure Loguru
    logger.remove()  # Remove default handlers
    logger.add(
        config.LOG_FILENAME,
        rotation=config.LOG_ROTATION,
        level=config.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"
    )
    logger.add(lambda msg: print(msg), level="INFO", format="{message}")  # Console output
    
    return logger


def create_app():
    """Create and configure the Flask application."""
    # Setup logging
    setup_logging()
    logger.info("Initializing Flask application")
    
    # Create Flask app
    app = Flask(__name__, 
                static_folder="static",
                template_folder="templates")
    
    # Configure app
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app)
    
    # Ensure the Gemini API key is set
    if not app.config.get("GEMINI_API_KEY"):
        logger.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)
    
    logger.info("Flask application initialized successfully")
    return app
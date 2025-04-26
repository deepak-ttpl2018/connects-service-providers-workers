#!/usr/bin/env python3
"""
EduMind AI - Main Application Entry Point

This is the main entry point for the EduMind AI tutor application.
It initializes all necessary components and starts the web server.
"""

import logging
from src.web.server import start_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point."""
    logger.info("Starting EduMind AI Tutor application")
    
    # Initialize and start the web server
    start_server()

if __name__ == "__main__":
    main()

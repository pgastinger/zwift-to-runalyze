"""Main entry point for Zwift to Garmin activity transfer."""

import sys
import os
import logging

from dotenv import load_dotenv
from services.zwift_service import ZwiftService
from services.fit_file_service import FitFileService


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to orchestrate the activity transfer process."""
    # Load environment variables from .env file
    logger = logging.getLogger(__name__)
    logger.info("test")
    load_dotenv()


if __name__ == "__main__":
    main()
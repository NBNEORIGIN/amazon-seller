"""
Utilities Module
----------------
General-purpose utility functions (logging, error handling, etc).
"""

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        # Optionally add a file handler:
        # logging.FileHandler('app.log'),
    ]
)

logger = logging.getLogger('AmazonSellerApp')

# Example utility function

def log_exception(exc: Exception, context: str = ""):
    logger.error(f"Exception occurred in {context}: {exc}")

# Add more utility functions as needed

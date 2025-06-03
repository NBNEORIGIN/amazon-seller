"""
Configuration Module
-------------------
Centralizes all application-wide settings, paths, and constants.
"""

import os

# Example paths (edit as needed)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, '001 AMAZON DATA DOWNLOAD')
SVG_OUTPUT_DIR = os.path.join(BASE_DIR, 'SVG_OUTPUT')
GRAPHICS_DIR = os.path.join(BASE_DIR, 'assets')

# Example constants
DEFAULT_BATCH_SIZE = 9
DEFAULT_FONT = 'Georgia'

# Add more configuration as needed

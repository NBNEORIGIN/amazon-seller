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

import pandas as pd
import os
from datetime import datetime

def create_batch_csv(orders_list_of_dicts, batch_num, category, output_dir, date_str=None):
    """
    Creates a CSV file for a batch of processed orders.

    Args:
        orders_list_of_dicts: A list of dictionaries, where each dictionary represents an order.
        batch_num: The batch number.
        category: The category name for the batch (e.g., 'REGULAR_STAKES').
        output_dir: The directory where the CSV file should be saved.
        date_str: Optional date string (YYYYMMDD). If None, current date is used.
    """
    if not orders_list_of_dicts:
        print(f"No orders provided for batch {batch_num} of category {category}, CSV not created.")
        return

    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Convert list of dicts to DataFrame
    # It's important to handle potential variations in dictionary keys
    # and aim for a consistent set of columns in the CSV.
    df_batch = pd.DataFrame(orders_list_of_dicts)

    # Define a common set of columns you expect, and reorder/fill missing ones if necessary.
    # This depends on the data structure of your orders.
    # Example common columns (adjust as per your actual data):
    common_columns = [
        'order-id', 'order-item-id', 'sku', 'type', 'colour',
        'graphic', 'line_1', 'line_2', 'line_3', 'image_path', 'photo_path',
        'quantity', 'warnings', 'SVG Processor'
        # Add other columns that are relevant from your order data
    ]

    # Ensure all common columns exist, fill with NA if not present in this batch
    for col in common_columns:
        if col not in df_batch.columns:
            df_batch[col] = pd.NA

    # Select and reorder columns for consistency
    # Only include columns that are actually present in common_columns to avoid errors
    present_common_columns = [col for col in common_columns if col in df_batch.columns]
    df_to_save = df_batch[present_common_columns]

    csv_filename = f"{category}_{date_str}_{batch_num:03d}.csv"
    csv_filepath = os.path.join(output_dir, csv_filename)

    try:
        df_to_save.to_csv(csv_filepath, index=False, encoding='utf-8-sig')
        print(f"Successfully generated CSV: {csv_filepath}")
    except Exception as e:
        print(f"Error generating CSV {csv_filepath}: {e}")

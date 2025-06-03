"""
File I/O Module
---------------
Handles reading and writing of CSV, Excel, and image files.
This module is independent of the GUI and can be tested separately.
"""

import pandas as pd
from PIL import Image
import os

# Data file reading

def read_orders(filepath: str) -> pd.DataFrame:
    """Read order data from CSV or Excel file."""
    if filepath.lower().endswith('.csv'):
        return pd.read_csv(filepath)
    elif filepath.lower().endswith(('.xls', '.xlsx')):
        return pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file type: {filepath}")


def write_orders(df: pd.DataFrame, filepath: str) -> None:
    """Write order data to CSV or Excel file."""
    if filepath.lower().endswith('.csv'):
        df.to_csv(filepath, index=False)
    elif filepath.lower().endswith(('.xls', '.xlsx')):
        df.to_excel(filepath, index=False)
    else:
        raise ValueError(f"Unsupported file type: {filepath}")

# Image file reading

def load_image(image_path: str) -> Image.Image:
    """Load an image file using PIL."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    return Image.open(image_path)

# Example usage (for testing, not run by GUI):
if __name__ == "__main__":
    df = read_orders("example_orders.csv")
    write_orders(df, "output_orders.csv")
    img = load_image("example.png")
    img.show()

import pandas as pd
import os
from pathlib import Path
import sys
from regular_stakes import RegularStakesProcessor
from bw_stakes import BWStakesProcessor
from photo_stakes import PhotoStakesProcessor
from coloured_large_stakes import ColouredLargeStakesProcessor
from coloured_large_photo_stakes import ColouredLargePhotoStakesProcessor
from bw_large_stakes import BWLargeStakesProcessor
from bw_large_photo_stakes import BWLargePhotoStakesProcessor

# Constants
CSV_PATH = r"G:\My Drive\003 APPS\001 D2C\orders.csv"
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Documents", "MemorialOutput")
GRAPHICS_PATH = r"G:\My Drive\001 NBNE\001 M\M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM\001 Design\002 MUTOH\002 AUTODESIGN"

def main():
    try:
        print("\nMemorial Batch Processor")
        print("----------------------")
        
        # Create output directory if it doesn't exist
        print(f"\nChecking output directory: {OUTPUT_DIR}")
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        print("Output directory ready")
        
        # Check if orders.csv exists
        print(f"\nChecking for orders.csv: {CSV_PATH}")
        if not Path(CSV_PATH).exists():
            print(f"Error: orders.csv not found!")
            return False
        print("Found orders.csv")
        
        # Check if graphics directory exists
        print(f"\nChecking graphics directory: {GRAPHICS_PATH}")
        if not Path(GRAPHICS_PATH).exists():
            print(f"Error: Graphics directory not found!")
            return False
        print("Found graphics directory")
        
        # Read orders file
        df = pd.read_csv(CSV_PATH, encoding="latin1")
        print(f"\nFound {len(df)} total orders")
        
        # Process each memorial type
        processors = [
            RegularStakesProcessor(GRAPHICS_PATH, OUTPUT_DIR),
            BWStakesProcessor(GRAPHICS_PATH, OUTPUT_DIR),
            PhotoStakesProcessor(GRAPHICS_PATH, OUTPUT_DIR),
            ColouredLargeStakesProcessor(GRAPHICS_PATH, OUTPUT_DIR),
            ColouredLargePhotoStakesProcessor(GRAPHICS_PATH, OUTPUT_DIR),
            BWLargeStakesProcessor(GRAPHICS_PATH, OUTPUT_DIR),
            BWLargePhotoStakesProcessor(GRAPHICS_PATH, OUTPUT_DIR)
        ]
        
        for processor in processors:
            print(f"\nProcessing with {processor.__class__.__name__}")
            processor.process_orders(df)
        
        print("\nProcessing complete!")
        return True
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nProcessing failed!")
    input("\nPress Enter to exit...")

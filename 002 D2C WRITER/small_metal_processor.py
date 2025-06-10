import os
import pandas as pd
from base_metal_processor import BaseMetalProcessor
# Ensure core utilities can be found if this script is run directly for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SmallMetalProcessor(BaseMetalProcessor):
    def __init__(self, first_arg_from_gui, output_dir_from_gui, graphics_path_from_gui_if_provided=None):
        # first_arg_from_gui is graphics_path when called by main_gui_qt_clean.py
        actual_graphics_path = first_arg_from_gui
        actual_output_dir = output_dir_from_gui

        super().__init__(
            metal_type_name="small metal", # Specific type name
            mem_w=76.2,                  # Specific width for Small Metal
            mem_h=38.1,                   # Specific height for Small Metal
            first_arg_from_gui=actual_graphics_path,
            output_dir_from_gui=actual_output_dir
        )

if __name__ == "__main__":
    # Basic test block for SmallMetalProcessor
    test_output_dir = "test_small_metal_output"
    test_graphics_dir = "test_small_metal_graphics"
    os.makedirs(test_output_dir, exist_ok=True)
    os.makedirs(test_graphics_dir, exist_ok=True)

    dummy_graphic_name = "Small TestGraphicSmall.png" # Example graphic
    with open(os.path.join(test_graphics_dir, dummy_graphic_name), "w") as f:
        f.write("") # Create an empty file for testing os.path.exists

    processor = SmallMetalProcessor(test_graphics_dir, test_output_dir)

    sample_data = {
        'order-id': ['sm-001', 'sm-002', 'med-001'],
        'SKU': ['SM001', 'SM002', 'MED001'],
        'Type': ['Small Metal', 'small metal', 'Medium Metal'], # Mixed case
        'Colour': ['Aluminium', 'Aluminium', 'Brass'],
        'Graphic': [dummy_graphic_name, 'NonExistentS.png', 'SomeGraphicM.png'],
        'Line_1': ['Small Memory', 'Small Hearts', 'Medium Item'],
        'Line_2': ['Small Name One', 'Small Name Two', 'Medium Name'],
        'Line_3': ['Small Dates', 'Small Dates 2', 'Medium Dates']
    }
    test_df = pd.DataFrame(sample_data)

    print(f"Running SmallMetalProcessor test with initial DataFrame:\n{test_df}")
    processor.process_orders(test_df)
    print(f"SmallMetalProcessor test finished. Check '{test_output_dir}' for SVGs and CSVs.")
    print(f"Expected output: SVGs for SM001, SM002. Graphic '{dummy_graphic_name}' for SM001.")

    # Optional: Cleanup test directories
    # import shutil
    # shutil.rmtree(test_output_dir)
    # shutil.rmtree(test_graphics_dir)
    # print("Cleaned up Small Metal test directories.")

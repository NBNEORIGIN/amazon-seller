import os
import pandas as pd
from base_metal_processor import BaseMetalProcessor
# Ensure core utilities can be found if this script is run directly for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MediumMetalProcessor(BaseMetalProcessor):
    def __init__(self, first_arg_from_gui, output_dir_from_gui, graphics_path_from_gui_if_provided=None):
        # first_arg_from_gui is graphics_path when called by main_gui_qt_clean.py
        actual_graphics_path = first_arg_from_gui
        actual_output_dir = output_dir_from_gui

        super().__init__(
            metal_type_name="medium metal", # Specific type name
            mem_w=101.6,                  # Specific width for Medium Metal
            mem_h=50.8,                   # Specific height for Medium Metal
            first_arg_from_gui=actual_graphics_path,
            output_dir_from_gui=actual_output_dir
        )

if __name__ == "__main__":
    # Basic test block for MediumMetalProcessor
    test_output_dir = "test_medium_metal_output"
    test_graphics_dir = "test_medium_metal_graphics"
    os.makedirs(test_output_dir, exist_ok=True)
    os.makedirs(test_graphics_dir, exist_ok=True)

    dummy_graphic_name = "Small TestGraphicMedium.png" # Example graphic
    with open(os.path.join(test_graphics_dir, dummy_graphic_name), "w") as f:
        f.write("") # Create an empty file for testing os.path.exists

    processor = MediumMetalProcessor(test_graphics_dir, test_output_dir)

    sample_data = {
        'order-id': ['med-001', 'med-002', 'sm-001'],
        'SKU': ['MED001', 'MED002', 'SM001'],
        'Type': ['Medium Metal', 'medium metal', 'Small Metal'], # Mixed case
        'Colour': ['Brass', 'Brass', 'Silver'],
        'Graphic': [dummy_graphic_name, 'NonExistentM.png', 'SomeGraphicS.png'],
        'Line_1': ['Medium Memory', 'Medium Hearts', 'Small Item'],
        'Line_2': ['Medium Name One', 'Medium Name Two', 'Small Name'],
        'Line_3': ['Medium Dates', 'Medium Dates 2', 'Small Dates']
    }
    test_df = pd.DataFrame(sample_data)

    print(f"Running MediumMetalProcessor test with initial DataFrame:\n{test_df}")
    processor.process_orders(test_df)
    print(f"MediumMetalProcessor test finished. Check '{test_output_dir}' for SVGs and CSVs.")
    print(f"Expected output: SVGs for MED001, MED002. Graphic '{dummy_graphic_name}' for MED001.")

    # Optional: Cleanup test directories
    # import shutil
    # shutil.rmtree(test_output_dir)
    # shutil.rmtree(test_graphics_dir)
    # print("Cleaned up Medium Metal test directories.")

import os
import pandas as pd
from base_metal_processor import BaseMetalProcessor
# Ensure core utilities can be found if this script is run directly for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class XLMetalProcessor(BaseMetalProcessor):
    def __init__(self, first_arg_from_gui, output_dir_from_gui, graphics_path_from_gui_if_provided=None):
        # first_arg_from_gui is graphics_path when called by main_gui_qt_clean.py
        actual_graphics_path = first_arg_from_gui
        actual_output_dir = output_dir_from_gui

        super().__init__(
            metal_type_name="xl metal", # Specific type name
            mem_w=152.4,                # Specific width for XL Metal
            mem_h=101.6,                # Specific height for XL Metal
            first_arg_from_gui=actual_graphics_path,
            output_dir_from_gui=actual_output_dir
        )

if __name__ == "__main__":
    # Basic test block for XLMetalProcessor
    test_output_dir = "test_xl_metal_output"
    test_graphics_dir = "test_xl_metal_graphics" # Should match the one used by processor
    os.makedirs(test_output_dir, exist_ok=True)
    os.makedirs(test_graphics_dir, exist_ok=True)

    dummy_graphic_name = "Small TestGraphicXL.png" # Example graphic
    with open(os.path.join(test_graphics_dir, dummy_graphic_name), "w") as f:
        f.write("") # Create an empty file for testing os.path.exists

    # Instantiate the processor
    # It expects graphics_path as first arg, output_dir as second from GUI call pattern
    processor = XLMetalProcessor(test_graphics_dir, test_output_dir)

    sample_data = {
        'order-id': ['xl-001', 'xl-002', 'lm-001'],
        'SKU': ['XL001', 'XL002', 'LM001'],
        'Type': ['XL Metal', 'xl metal', 'Large Metal'], # Mixed case and other types
        'Colour': ['Silver', 'Silver', 'Silver'],
        'Graphic': [dummy_graphic_name, 'NonExistent.png', 'SomeGraphic.png'],
        'Line_1': ['XL In Loving Memory', 'XL Forever In Our Hearts', 'Large Item'],
        'Line_2': ['XL Name One', 'XL Name Two', 'Large Name'],
        'Line_3': ['XL Dates', 'XL Dates 2', 'Large Dates']
    }
    test_df = pd.DataFrame(sample_data)

    print(f"Running XLMetalProcessor test with initial DataFrame:\n{test_df}")
    processor.process_orders(test_df)
    print(f"XLMetalProcessor test finished. Check '{test_output_dir}' for SVGs and CSVs.")
    print(f"Expected output: SVGs for XL001, XL002. Graphic '{dummy_graphic_name}' for XL001.")

    # Optional: Cleanup test directories
    # import shutil
    # shutil.rmtree(test_output_dir)
    # shutil.rmtree(test_graphics_dir)
    # print("Cleaned up XL Metal test directories.")

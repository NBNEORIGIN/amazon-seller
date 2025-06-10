import os
import base64
import pandas as pd
import svgwrite
# from coloured_small_stakes_template_processor import ColouredSmallStakesTemplateProcessor
from base_metal_processor import BaseMetalProcessor # Added import
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import add_multiline_text

class LargeMetalProcessor(BaseMetalProcessor): # Changed parent class
    def __init__(self, first_arg_from_gui, output_dir_from_gui, graphics_path_from_gui_if_provided=None):
        # first_arg_from_gui is graphics_path when called by main_gui_qt_clean.py
        actual_graphics_path = first_arg_from_gui
        actual_output_dir = output_dir_from_gui

        super().__init__(
            metal_type_name="large metal",
            mem_w=127,
            mem_h=76.2,
            first_arg_from_gui=actual_graphics_path,
            output_dir_from_gui=actual_output_dir
        )

# process_orders method is removed
# populate_svg method is removed

if __name__ == "__main__":
    import pandas as pd
    import os

    print("Running LargeMetalProcessor basic test...")

    # Create dummy directories and data for testing
    test_output_dir = "test_lmp_output"
    test_graphics_dir = "test_lmp_graphics"
    os.makedirs(test_output_dir, exist_ok=True)
    os.makedirs(test_graphics_dir, exist_ok=True)

    # Dummy graphics file (empty)
    # In a real scenario, this would be an actual image.
    # The processor's embed_image checks for file existence.
    dummy_graphic_name = "Small TestGraphic.png"
    with open(os.path.join(test_graphics_dir, dummy_graphic_name), "w") as f:
        f.write("") # Create an empty file

    processor = LargeMetalProcessor(test_graphics_dir, test_output_dir)

    # Create a sample DataFrame
    sample_data = {
        'order-id': ['123-001', '123-002', '123-003', '123-004'],
        'SKU': ['LM001', 'LM002', 'SM001', 'LM003'],
        'Type': ['Large Metal', 'Large Metal', 'Small Metal', 'Large Metal'], # Note: Case difference
        'Colour': ['Silver', 'Silver', 'Black', 'Silver'], # Colour is not used by LMP
        'Graphic': [dummy_graphic_name, 'NonExistent.png', 'SomeGraphic.png', dummy_graphic_name],
        'Line_1': ['In Loving Memory', 'Forever In Our Hearts', 'Pet Angel', 'Gone But Not Forgotten'],
        'Line_2': ['Name One', 'Name Two', 'Buddy', 'Name Three'],
        'Line_3': ['1950-2020', '1960-2021', '2010-2022', '1970-2023']
    }
    test_df = pd.DataFrame(sample_data)

    print(f"Initial test DataFrame:\n{test_df}")

    # Process the orders
    # The processor itself filters for 'type' == 'large metal'
    processor.process_orders(test_df)

    print(f"Test finished. Check '{test_output_dir}' for generated SVGs and CSVs.")
    print("Expected output: SVGs for LM001, LM002, LM003 (3 orders).")
    print(f"Graphic '{dummy_graphic_name}' should be attempted for LM001 and LM003.")
    print("Graphic 'NonExistent.png' for LM002 should be skipped gracefully.")

    # Basic cleanup (optional, for local testing)
    # import shutil
    # shutil.rmtree(test_output_dir)
    # shutil.rmtree(test_graphics_dir)
    # print("Cleaned up test directories.")

import os
import base64
import pandas as pd
import svgwrite
from coloured_small_stakes_template_processor import ColouredSmallStakesTemplateProcessor
import sys
# Ensure core utilities can be found by adding the parent directory of '002 D2C WRITER' to sys.path
# This assumes 'core' is a sibling directory to '002 D2C WRITER' at the project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import add_multiline_text

class BaseMetalProcessor(ColouredSmallStakesTemplateProcessor):
    def __init__(self, metal_type_name, mem_w, mem_h, first_arg_from_gui, output_dir_from_gui):
        # first_arg_from_gui is graphics_path when called by main_gui_qt_clean.py for these types
        actual_graphics_path = first_arg_from_gui
        actual_output_dir = output_dir_from_gui

        super().__init__(template_path=None,
                         output_dir=actual_output_dir,
                         graphics_path=actual_graphics_path)

        self.metal_type_name = str(metal_type_name).lower().strip()
        self.mem_w = mem_w
        self.mem_h = mem_h

        # Calculate batch_size (number of items that fit in a row on the page)
        page_w = 480 # Standard page width in mm
        if self.mem_w > 0:
            self.batch_size = page_w // self.mem_w
        else:
            self.batch_size = 1 # Avoid division by zero, default to 1 if mem_w is invalid
        if self.batch_size == 0: # Ensure at least one item if it's very wide
             self.batch_size = 1

    def process_orders(self, df):
        df = df.copy()
        # Ensure column names are lowercase for consistent access
        df.columns = [col.lower() for col in df.columns]

        # Normalize 'type' column for consistent filtering
        if 'type' in df.columns:
            df['type'] = df['type'].astype(str).str.strip().str.lower()
        else:
            print(f"Warning: 'type' column not found in DataFrame for {self.metal_type_name} processor.")
            return # Or handle as an error / empty filtered list

        # Filter orders for the specific metal type
        filtered = df[df['type'] == self.metal_type_name]
        print(f"Processing for type: '{self.metal_type_name}'. Initial orders: {len(df)}, Filtered rows: {len(filtered)}")

        if filtered.empty:
            print(f"No orders found for type '{self.metal_type_name}'.")
            return

        batch_num = 1
        for start_idx in range(0, len(filtered), self.batch_size):
            batch_orders = filtered.iloc[start_idx:start_idx + self.batch_size]
            if not batch_orders.empty:
                # Generate a unique part of the filename based on the metal type
                type_filename_part = self.metal_type_name.replace(' ', '_')
                svg_out_path = os.path.join(
                    self.output_dir,
                    f"{type_filename_part}_batch_{batch_num:03d}.svg"
                )
                self.populate_svg(batch_orders, svg_out_path)

                csv_out_path = os.path.splitext(svg_out_path)[0] + ".csv"
                try:
                    batch_orders.to_csv(csv_out_path, index=False, encoding="utf-8-sig")
                    print(f"Wrote batch CSV: {csv_out_path}")
                except Exception as e:
                    print(f"Error writing CSV {csv_out_path}: {e}")
                batch_num += 1

    def populate_svg(self, batch_orders, output_svg_path):
        page_w = 480  # SVG page width in mm
        page_h = 290  # SVG page height in mm

        dwg = svgwrite.Drawing(
            filename=output_svg_path,
            size=(f"{page_w}mm", f"{page_h}mm"),
            viewBox=f"0 0 {page_w} {page_h}"
        )

        # Use instance variables for memorial dimensions
        mem_w = self.mem_w
        mem_h = self.mem_h
        corner_r = 6 # Standard corner radius

        # Grid calculation based on current batch_size (items per row)
        # For metal processors, it's typically a single row.
        grid_cols = self.batch_size
        grid_rows = 1

        # Ensure items fit; this should ideally be handled by batch_size calculation in __init__
        if grid_cols * mem_w > page_w:
            grid_cols = page_w // mem_w
            if grid_cols == 0 and mem_w > 0 : grid_cols = 1 # if item is wider than page ensure one is still processed
            elif mem_w == 0: grid_cols =1


        grid_total_w = grid_cols * mem_w
        grid_total_h = grid_rows * mem_h

        # Position the grid at the bottom-right of the page
        grid_start_x = page_w - grid_total_w
        grid_start_y = page_h - grid_total_h

        for idx, (_, order) in enumerate(batch_orders.iterrows()):
            if idx >= grid_cols: # Only process items that fit in the row
                break

            # Items are filled right-to-left in a single row
            col_idx = grid_cols - 1 - idx
            x = grid_start_x + col_idx * mem_w
            y = grid_start_y # Since grid_rows is 1

            dwg.add(dwg.rect(
                insert=(x, y),
                size=(mem_w, mem_h),
                rx=corner_r, ry=corner_r,
                fill='none',
                stroke='red', # Changed from blue to red to match original
                stroke_width=0.1
            ))

            # Graphic handling
            # Ensure 'graphic' column exists and is processed correctly
            raw_graphic_name = str(order.get('graphic', '')).strip()
            graphic_filename = raw_graphic_name

            # Specific SKU override for graphic (example from LargeMetalProcessor)
            # This could be generalized or moved to subclasses if different metal types have different special SKUs
            sku = str(order.get('sku', '')).strip()
            if sku == 'M0634S - CAT - RAINBOW BRIDGE': # This is likely specific to small stakes
                graphic_filename = 'Small Rainbow Bridge.png'
            else:
                # Logic for "Small " prefix - consider if this is universal for all metal types
                # If not, this might need to be adjusted or made configurable per subclass.
                if raw_graphic_name and not raw_graphic_name.lower().startswith('small '):
                    graphic_filename = 'Small ' + raw_graphic_name

            if graphic_filename and self.graphics_path: # Ensure graphics_path is not None
                graphic_path = os.path.join(self.graphics_path, graphic_filename)
                if os.path.exists(graphic_path):
                    # embed_image is inherited from ColouredSmallStakesTemplateProcessor
                    embedded_image = self.embed_image(graphic_path)
                    if embedded_image:
                        dwg.add(dwg.image(
                            href=embedded_image,
                            insert=(x, y), # Adjust if graphic shouldn't fill the whole item
                            size=(mem_w, mem_h), # Or specific graphic dimensions
                            preserveAspectRatio='xMidYMid meet'
                        ))
                else:
                    print(f"Warning: Graphic file not found: {graphic_path} for SKU {sku}")
            elif raw_graphic_name: # Graphic name provided but no graphics_path
                 print(f"Warning: Graphics path not set, cannot load graphic '{graphic_filename}' for SKU {sku}")


            # Text placement
            font_family = "Georgia"
            center_x = x + mem_w / 2
            center_y = y + (mem_h / 2)

            line_1_text = str(order.get('line_1', ''))
            # check_grammar_and_typos(line_1_text) # Consider if this is desired for all
            line_1_lines = split_line_to_fit(line_1_text, 30) # Max chars might need to vary by mem_w
            dwg.add(add_multiline_text(dwg, line_1_lines, insert=(center_x, center_y - 15), font_size="3.33pt", font_family=font_family, anchor="middle", fill="black"))

            line_2_text = str(order.get('line_2', ''))
            # check_grammar_and_typos(line_2_text)
            line_2_lines = split_line_to_fit(line_2_text, 30)
            dwg.add(add_multiline_text(dwg, line_2_lines, insert=(center_x, center_y), font_size="2.5mm", font_family=font_family, anchor="middle", fill="black"))

            line_3_text = str(order.get('line_3', ''))
            # check_grammar_and_typos(line_3_text)
            line_3_lines = split_line_to_fit(line_3_text, 30)
            dwg.add(add_multiline_text(dwg, line_3_lines, insert=(center_x, center_y + 10), font_size="3.33pt", font_family=font_family, anchor="middle", fill="black"))

        # UV printer reference blue square (bottom right of page)
        blue_size = 0.1
        dwg.add(dwg.rect(insert=(page_w - blue_size, page_h - blue_size), size=(blue_size, blue_size), fill='blue'))

        try:
            dwg.save()
            print(f"Wrote batch SVG: {output_svg_path}")
        except Exception as e:
            print(f"Error saving SVG {output_svg_path}: {e}")

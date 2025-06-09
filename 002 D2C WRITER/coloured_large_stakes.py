import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import draw_rounded_rect, add_multiline_text

class ColouredLargeStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'COLOURED_LARGE_STAKES'
        # SVG/page dimensions (from codebase conventions)
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.viewbox_width = 1662
        self.viewbox_height = 1095
        # Memorial geometry (from SVG)
        self.memorial_width_px = 755.42004
        self.memorial_height_px = 453.1008
        self.corner_radius_px = 22.012239
        self.stroke_width = 0.378046
        # Text sizes (from SVG or design)
        self.line1_size_pt = 45.33  # e.g. "In Loving Memory Of"
        self.line2_size_pt = 66.67  # Name
        self.line3_size_pt = 32     # Additional lines
        # Grid layout (2x2)
        self.grid_cols = 2
        self.grid_rows = 2
        self.batch_size = self.grid_cols * self.grid_rows
        # Offsets and spacing (from SVG)
        self.x_offset_px = 150.59
        self.y_offset_px = 641.97
        self.memorial_spacing_x_px = 755.80
        self.memorial_spacing_y_px = 453.10

    def process_orders(self, df):
        # Input `df` is assumed to be pre-filtered for this processor's category.
        # Normalize column names (often done in MemorialBase or should be first step)
        df.columns = [col.upper().strip() for col in df.columns] # Assuming this processor expects uppercase

        # Ensure essential columns exist and perform type conversions if needed
        # Example: (ensure these match expected case from processor logic)
        if 'TYPE' in df.columns:
            df['TYPE'] = df['TYPE'].astype(str).str.strip() # No .lower() if expecting specific case
        else:
            df['TYPE'] = ''
        if 'COLOUR' in df.columns:
            df['COLOUR'] = df['COLOUR'].astype(str).str.strip() # No .lower()
        else:
            df['COLOUR'] = ''
        # Add other necessary columns if they might be missing and are used later

        # The original filtering logic is removed. df is now df_to_process.
        df_to_process = df

        if df_to_process.empty:
            print(f"No eligible orders for {self.CATEGORY} processor.")
            return

        batch_num = 1
        for start_idx in range(0, len(df_to_process), self.batch_size):
            batch_orders = df_to_process.iloc[start_idx:start_idx + self.batch_size]
            if not batch_orders.empty:
                print(f"\nProcessing Coloured Large Stake batch {batch_num}...")
                orders_dict = batch_orders.to_dict('records')
                self.create_memorial_svg(orders_dict, batch_num)
                self.create_batch_csv(orders_dict, batch_num, self.CATEGORY)
                batch_num += 1

    def create_memorial_svg(self, orders, batch_num):
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}_No Jig.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        print(f"Creating SVG file: {filepath}")
        dwg = svgwrite.Drawing(
            filepath,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.viewbox_width} {self.viewbox_height}"
        )
        positions = [
            # bottom right, bottom left, top right, top left
            (self.x_offset_px + self.memorial_spacing_x_px, self.y_offset_px),
            (self.x_offset_px, self.y_offset_px),
            (self.x_offset_px + self.memorial_spacing_x_px, self.y_offset_px - self.memorial_spacing_y_px),
            (self.x_offset_px, self.y_offset_px - self.memorial_spacing_y_px),
        ]
        for idx, order in enumerate(orders):
            if idx >= 4:
                break
            x, y = positions[idx]
            print(f"Adding memorial {idx+1} at position ({x}, {y})")
            self.add_memorial(dwg, x, y, order)
        # Add reference point (blue pixel in bottom right)
        # Move blue reference square down by 0.05mm (convert mm to px using viewbox_height/page_height_mm)
        blue_square_x = self.viewbox_width - 0.38
        blue_square_y = self.viewbox_height - 0.38 + (0.05 * self.viewbox_height / self.page_height_mm)
        dwg.add(dwg.rect(
            insert=(blue_square_x, blue_square_y),
            size=(0.38, 0.38),
            fill="blue"
        ))
        print(f"Saving SVG file to: {filepath}")
        dwg.save()
        print(f"SVG file saved successfully")

    def add_memorial(self, dwg, x, y, order):
        default_slot_stroke_color = 'red' # Current default
        slot_stroke_color = default_slot_stroke_color
        is_attention_order = False

        # Handle potential case variations for keys from order dictionary
        order_colour_val = order.get('COLOUR', order.get('colour', ''))
        order_type_val = order.get('TYPE', order.get('type', ''))

        order_colour_lower = str(order_colour_val).lower()
        order_type_lower = str(order_type_val).lower()

        if order_colour_lower in ['marble', 'stone']:
            is_attention_order = True

        if order_type_lower == 'large plaque' or order_type_lower == 'regular plaque':
            is_attention_order = True

        if is_attention_order:
            slot_stroke_color = 'yellow'

        # Draw rounded rectangle for the memorial
        dwg.add(draw_rounded_rect(
            dwg,
            insert=(x, y),
            size=(self.memorial_width_px, self.memorial_height_px),
            rx=self.corner_radius_px,
            ry=self.corner_radius_px,
            fill='white',  # Could be changed based on COLOUR
            stroke=slot_stroke_color, # MODIFIED HERE
            stroke_width=self.stroke_width
        ))
        # --- Embed graphic if present (logic from RegularStakesProcessor) ---
        graphic_filename = order.get('GRAPHIC')
        if graphic_filename:
            graphic_path = os.path.join(self.graphics_path, str(graphic_filename))
            print(f"Looking for graphic: {graphic_path}")
            if os.path.exists(graphic_path):
                print(f"Found graphic: {graphic_path}")
                embedded_image = self.embed_image(graphic_path)
                if embedded_image:
                    # Center the image in the memorial rectangle
                    dwg.add(dwg.image(
                        href=embedded_image,
                        insert=(x, y),
                        size=(self.memorial_width_px, self.memorial_height_px)
                    ))
                else:
                    print(f"Failed to embed graphic")
            else:
                print(f"Warning: Graphic not found: {graphic_path}")
        # Place text fields (assume LINE_1, LINE_2, LINE_3)
        # Adjust these positions as needed
        center_x = x + self.memorial_width_px / 2
        # Example vertical offsets for text lines
        # If THEME is 'Islamic', move Line 1 and Line 2 down by 40mm (converted to px)
        theme = str(order.get('THEME', '')).strip().lower()
        y1_offset = 80
        y2_offset = 180
        line2_size_pt = self.line2_size_pt
        if theme == 'islamic':
            px_per_mm = self.viewbox_width / self.page_width_mm
            y1_offset += 40 * px_per_mm  # Move Line 1 down by 40mm
            y2_offset += 30 * px_per_mm  # Move Line 2 down by 30mm (40mm - 10mm)
            line2_size_pt = self.line2_size_pt * 0.5  # Reduce Line 2 size by 50%
        y1 = y + y1_offset
        y2 = y + y2_offset
        y3 = y + 260  # Line 3 unchanged
        # Use shared SVG utility for multi-line text. For now, treat each line as a single-item list for compatibility.
        # Line 1: wrap and grammar check
        line1 = order.get('LINE_1', '')
        check_grammar_and_typos(line1)  # Grammar check (optional: handle result)
        line1_lines = split_line_to_fit(str(line1), 30)
        dwg.add(add_multiline_text(
            dwg,
            line1_lines,
            insert=(center_x, y1),
            font_size=f"{self.line1_size_pt}px",
            font_family="Georgia",
            anchor="middle",
            fill="black"
        ))
        # Line 2: wrap and grammar check
        line2 = order.get('LINE_2', '')
        check_grammar_and_typos(line2)
        line2_lines = split_line_to_fit(str(line2), 30)
        dwg.add(add_multiline_text(
            dwg,
            line2_lines,
            insert=(center_x, y2),
            font_size=f"{line2_size_pt}px",
            font_family="Georgia",
            anchor="middle",
            fill="black"
        ))
        # Line 3: wrap and grammar check
        line3 = order.get('LINE_3', '')
        check_grammar_and_typos(line3)
        line3_lines = split_line_to_fit(str(line3), 30)
        dwg.add(add_multiline_text(
            dwg,
            line3_lines,
            insert=(center_x, y3),
            font_size=f"{self.line3_size_pt}px",
            font_family="Georgia",
            anchor="middle",
            fill="black"
        ))
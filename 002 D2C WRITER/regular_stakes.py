import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import draw_rounded_rect, add_multiline_text
from datetime import datetime
from pathlib import Path

class RegularStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'regular_stakes' # Updated CATEGORY
        self.grid_cols = 3
        self.grid_rows = 3
        self.batch_size = self.grid_cols * self.grid_rows

        # Conversion factors
        self.px_per_mm = 1 / 0.26458333333
        self.pt_to_mm = 0.2645833333

        # Memorial and page dimensions
        self.memorial_width_mm = 140
        self.memorial_height_mm = 90
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.memorial_width_px = self.memorial_width_mm * self.px_per_mm
        self.memorial_height_px = self.memorial_height_mm * self.px_per_mm
        self.page_width_px = self.page_width_mm * self.px_per_mm
        self.page_height_px = self.page_height_mm * self.px_per_mm

        # Centering offsets
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows
        self.x_offset_mm = (self.page_width_mm - grid_width_mm) / 2
        self.y_offset_mm = (self.page_height_mm - grid_height_mm) / 2
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

        # Text sizes (in points)
        self.line1_size_pt = 17 * 1.2  # Increased by 20%
        self.line2_size_pt = 25 * 1.2
        self.line3_size_pt = 12 * 1.1

        # Stroke width and corner radius
        self.stroke_width = 0.1 * self.px_per_mm
        self.corner_radius_px = 6 * self.px_per_mm


    def process_orders(self, orders):
        # Input `orders` (or `df`) is assumed to be pre-filtered for this processor's category.
        print("[DEBUG] Entered RegularStakesProcessor.process_orders")
        if isinstance(orders, list):
            df = pd.DataFrame(orders)
        else:
            df = orders.copy()

        df.columns = [col.lower().strip() for col in df.columns]
        if 'type' in df.columns:
            df['type'] = df['type'].astype(str).str.strip().str.lower()
        if 'colour' in df.columns:
            df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        if 'decorationtype' not in df.columns:
            print("Warning: 'decorationtype' column not found in input orders. Please ensure order_pipeline.py was run after updating SKULIST.csv.")
            df['decorationtype'] = ''
        else:
            df['decorationtype'] = df['decorationtype'].astype(str).str.strip().str.lower()

        print(f"Columns after normalization: {list(df.columns)}")
        print(df.head())

        # The initial filtering based on type, colour, and decorationtype is removed.
        # The input DataFrame `df` is assumed to be pre-filtered.

        # Expand rows by number-of-items - this should still be done on the input df
        expanded_rows = []
        for _, row in df.iterrows(): # Iterate over the input df
            try:
                qty = int(row.get('number-of-items', 1))
                qty = max(qty, 1) # Ensure qty is at least 1
            except (ValueError, TypeError): # Catch potential errors if 'number-of-items' is not a valid number
                qty = 1
            for _ in range(qty):
                expanded_rows.append(row.copy())

        if not expanded_rows: # If df was empty or only had invalid qtys
            print("No rows to process after expansion.")
            return

        df_to_process = pd.DataFrame(expanded_rows)

        # Ensure relevant columns are consistently typed and cased for further processing, if not already.
        # These were previously applied to df_expanded, now apply to df_to_process.
        if 'type' in df_to_process.columns:
            df_to_process['type'] = df_to_process['type'].astype(str).str.strip().str.lower()
        if 'colour' in df_to_process.columns:
            df_to_process['colour'] = df_to_process['colour'].astype(str).str.strip().str.lower()
        if 'decorationtype' in df_to_process.columns:
            df_to_process['decorationtype'] = df_to_process['decorationtype'].astype(str).str.strip().str.lower()
        if 'sku' in df_to_process.columns:
            df_to_process['sku'] = df_to_process['sku'].astype(str).str.strip().str.lower()

        # Internal sorting logic (e.g., by color_priority) can remain if it's for processing order within the category.
        color_priority = {'copper': 0, 'gold': 1, 'silver': 2, 'stone': 3, 'marble': 4}
        if 'colour' in df_to_process.columns:
            df_to_process['color_priority'] = df_to_process['colour'].map(color_priority)
            df_to_process = df_to_process.sort_values('color_priority')

        # The photo SKU exclusion logic is removed as it's part of the initial broad category filtering.

        print(f"[DEBUG] DataFrame ready for batching (RegularStakesProcessor): {len(df_to_process)} rows")
        print(f"Sample data: {df_to_process[['order-id', 'sku', 'colour', 'decorationtype']].head() if not df_to_process.empty else 'DataFrame is empty'}")

        batch_num = 1
        total = len(df_to_process) # Use df_to_process
        print(f"[DEBUG] self.batch_size: {self.batch_size}")
        print(f"[DEBUG] total rows to process: {total}")

        if not isinstance(self.batch_size, int) or self.batch_size <= 0:
            print("[WARNING] batch_size is invalid (<=0 or not int), defaulting to processing all in one batch.")
            # Fallback or error handling for invalid batch_size can be added here
            # For now, let's assume if batch_size is invalid, it processes all as one batch if total > 0
            current_batch_size = total if total > 0 else 1 # Avoid division by zero if total is 0
        else:
            current_batch_size = self.batch_size

        for start_idx in range(0, total, current_batch_size):
            end_idx = min(start_idx + current_batch_size, total)
            print(f"[DEBUG] Batch indices: start_idx={start_idx}, end_idx={end_idx}")
            batch_orders = df_to_process.iloc[start_idx:end_idx] # Use df_to_process
            print(f"\nProcessing Regular Stake batch {batch_num}: rows {start_idx} to {end_idx-1} (batch size: {len(batch_orders)})")
            if not batch_orders.empty:
                orders_dict = batch_orders.to_dict('records')
                print(f"Batch {batch_num} first order text fields: line_1={orders_dict[0].get('line_1')}, line_2={orders_dict[0].get('line_2')}, line_3={orders_dict[0].get('line_3')}")
                self.create_memorial_svg(orders_dict, batch_num)
                self.create_batch_csv(orders_dict, batch_num, self.CATEGORY)
                batch_num += 1



    def create_memorial_svg(self, orders, batch_num, output_path=None):
        if orders:
            print(f"Batch {batch_num} first order text fields: line_1={orders[0].get('line_1')}, line_2={orders[0].get('line_2')}, line_3={orders[0].get('line_3')}")

        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S') # Added timestamp
        if output_path is None:
            filename = f"{self.CATEGORY}_{timestamp_str}_{batch_num:03d}.svg" # Updated filename
            output_path = os.path.join(self.OUTPUT_DIR, filename)

        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )

        for idx in range(self.batch_size):
            row = idx // self.grid_cols
            col = idx % self.grid_cols

            x = self.x_offset_px + (col * self.memorial_width_px)
            y = self.y_offset_px + (row * self.memorial_height_px)

            default_slot_stroke_color = 'red'
            slot_stroke_color = default_slot_stroke_color
            is_attention_order = False

            if idx < len(orders): # Check if there is an order for this slot
                current_order_for_attention_check = orders[idx]
                order_colour_lower = str(current_order_for_attention_check.get('colour', '')).lower()
                order_type_lower = str(current_order_for_attention_check.get('type', '')).lower()

                if order_colour_lower in ['marble', 'stone']:
                    is_attention_order = True

                if order_type_lower == 'regular plaque':
                    is_attention_order = True

                if is_attention_order:
                    slot_stroke_color = 'yellow'
            # If no order for this slot, it will use default_slot_stroke_color ('red')

            dwg.add(dwg.rect(
                insert=(x, y),
                size=(self.memorial_width_px, self.memorial_height_px),
                rx=self.corner_radius_px, # Use instance attribute
                ry=self.corner_radius_px, # Use instance attribute
                fill='none',
                stroke=slot_stroke_color, # MODIFIED HERE
                stroke_width=self.stroke_width # Use instance attribute
            ))

            if idx < len(orders):
                order = orders[idx]
                print(f"SVG Batch {batch_num}, Cell {idx}: order-id={order.get('order-id')}, sku={order.get('sku')}, line_1={order.get('line_1')}")
                # Use shared utility for grammar/typo checks
                for field in ['line_1', 'line_2', 'line_3']:
                    check_grammar_and_typos(order.get(field, ''))

                # --- SKU-specific logic for OM008021 ---
                # If the SKU is OM008021, always use the special graphic file from the hardcoded path.
                if str(order.get('sku', '')).upper() == 'OM008021':
                    graphic_path = r'G:/My Drive/001 NBNE/001 M/M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM/001 Design/002 MUTOH/002 AUTODESIGN/OM008021.png'
                    print(f"Using special graphic for OM008021: {graphic_path}")
                    if os.path.exists(graphic_path):
                        embedded_image = self.embed_image(graphic_path)
                        if embedded_image:
                            dwg.add(dwg.image(
                                href=embedded_image,
                                insert=(x, y),
                                size=(self.memorial_width_px, self.memorial_height_px)
                            ))
                        else:
                            print(f"Failed to embed OM008021 graphic")
                    else:
                        print(f"Warning: OM008021 graphic not found: {graphic_path}")
                # --- Standard logic for other SKUs ---
                elif order.get('graphic'):
                    graphic_path = os.path.join(self.graphics_path, str(order['graphic']))
                    print(f"Looking for graphic: {graphic_path}")
                    if os.path.exists(graphic_path):
                        print(f"Found graphic: {graphic_path}")
                        embedded_image = self.embed_image(graphic_path)
                        if embedded_image:
                            dwg.add(dwg.image(
                                href=embedded_image,
                                insert=(x, y),
                                size=(self.memorial_width_px, self.memorial_height_px)
                            ))
                        else:
                            print(f"Failed to embed graphic")
                    else:
                        print(f"Warning: Graphic not found: {graphic_path}")

                center_x = x + (self.memorial_width_px / 2)

                # Handle text lines with improved nan checking
                for line_num, (key, y_pos, font_size) in enumerate([
                    ('line_1', 28, self.line1_size_pt),
                    ('line_2', 45, self.line2_size_pt)
                ]):
                    value = order.get(key)
                    if value is not None and not (isinstance(value, float) and pd.isna(value)):
                        dwg.add(dwg.text(
                            str(value),
                            insert=(center_x, y + (y_pos * self.px_per_mm)),
                            font_size=f"{font_size * self.pt_to_mm}mm",
                            font_family="Georgia",
                            text_anchor="middle",
                            fill="black"
                        ))
                    else:
                        print(f"Warning: Missing text in {key} for order {order.get('order_id', 'Unknown')}")

                # Improved handling for LINE_3 (text box logic with tspan and robust line spacing)
                value = order.get('line_3')
                if value is not None and not (isinstance(value, float) and pd.isna(value)):
                    line3_text = str(value).strip()
                    if line3_text:  # Only process if there's actual text
                        lines = line3_text.split('\n')
                        font_mm = self.line3_size_pt * self.pt_to_mm
                        char_width_mm = 0.5 * font_mm
                        max_line_mm = self.memorial_width_mm * 0.6
                        max_chars = int(max_line_mm / char_width_mm)
                        split_lines = []
                        for l in lines:
                            if l.strip():  # Only process non-empty lines
                                split_lines.extend(split_line_to_fit(l, max_chars))
                        
                        if split_lines:  # Only continue if we have lines to display
                            if len(split_lines) == 1:
                                split_lines = split_line_to_fit(split_lines[0], 30)
                            split_lines = split_lines[:5]
                            
                            # --- Conditional font size logic for Line 3 ---
                            total_chars = sum(len(line) for line in split_lines)
                            if 10 <= total_chars <= 30:
                                line3_font_size_pt = self.line1_size_pt
                            elif 31 <= total_chars <= 90:
                                line3_font_size_pt = self.line1_size_pt * 0.9
                            else:
                                line3_font_size_pt = self.line3_size_pt

                            # SVG <text> with <tspan>s for each line, robust line spacing
                            line3_text_element = dwg.text(
                                "",
                                insert=(center_x, y + (57 * self.px_per_mm)),
                                font_size=f"{line3_font_size_pt * self.pt_to_mm}mm",
                                font_family="Georgia",
                                text_anchor="middle",
                                fill="black"
                            )
                            for line_idx, line in enumerate(split_lines):
                                # For all lines after the first, use 1.2em for robust line spacing
                                if line_idx == 0:
                                    dy_val = "0"
                                else:
                                    dy_val = "1.2em"
                                tspan = dwg.tspan(
                                    line.strip(),
                                    x=[center_x],
                                    dy=[dy_val]
                                )
                                line3_text_element.add(tspan)
                            dwg.add(line3_text_element)
                else:
                    print(f"Warning: Missing text in LINE_3 for order {order.get('ORDER_ID', 'Unknown')}")

        # Add reference point (0.1mm blue square) in bottom right corner
        ref_size_px = 0.1 * self.px_per_mm
        x_pos = self.page_width_px - ref_size_px
        y_pos = self.page_height_px - ref_size_px

        # Example of using shared SVG utility for rounded rect (if desired elsewhere):
        # dwg.add(draw_rounded_rect(dwg, insert=(x_pos, y_pos), size=(ref_size_px, ref_size_px), rx=0, ry=0, fill='blue', stroke='none', stroke_width=0))
        dwg.add(dwg.rect(
            insert=(x_pos, y_pos),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))

        dwg.save()
        return dwg

    # Overridden create_batch_csv with timestamp logic (but not ATTENTION_FLAG yet)
    def create_batch_csv(self, orders, batch_num, category):
        """Create CSV file for the batch with specified category prefix, using a timestamp."""
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')

        svg_reference_filename = f"{category}_{timestamp_str}_{batch_num:03d}.svg"
        csv_filename = f"{category}_{timestamp_str}_{batch_num:03d}.csv"
        design_file_ref = f"{category}_{timestamp_str}_{batch_num:03d}"

        filepath = os.path.join(self.OUTPUT_DIR, csv_filename)

        all_keys = set()
        for order in orders:
            all_keys.update([k.upper() for k in order.keys()])

        preferred_columns = [
            'SVG FILE', 'DESIGN FILE', 'ORDER-ID', 'ORDER-ITEM-ID', 'SKU', 'NUMBER-OF-ITEMS',
            'TYPE', 'COLOUR', 'GRAPHIC', 'LINE_1', 'LINE_2', 'LINE_3', 'THEME',
            'ATTENTION_FLAG', 'WARNINGS' # Added ATTENTION_FLAG
        ]
        extra_columns = [col for col in all_keys if col.upper() not in [pc.upper() for pc in preferred_columns]]
        columns = preferred_columns + sorted(list(set(extra_columns)))

        data = []
        for order in orders:
            row = {}
            row['SVG FILE'] = svg_reference_filename
            row['DESIGN FILE'] = design_file_ref

            # Populate ATTENTION_FLAG
            attention_messages = []
            order_colour_lower = str(order.get('colour', '')).lower()
            order_type_lower = str(order.get('type', '')).lower()

            if order_colour_lower in ['marble', 'stone']:
                attention_messages.append(f"RARE_COLOUR: {str(order.get('colour','')).upper()}")

            if order_type_lower == 'regular plaque':
                type_display = order.get('type', 'Regular Plaque')
                attention_messages.append(f"TYPE: {type_display}")

            row['ATTENTION_FLAG'] = "; ".join(attention_messages)

            for col_header in columns:
                if col_header in ['SVG FILE', 'DESIGN FILE', 'ATTENTION_FLAG']: # Skip already populated
                    continue
                val = order.get(col_header.lower(), order.get(col_header, order.get(col_header.upper(), '')))
                if col_header == 'NUMBER-OF-ITEMS' and val == '':
                    val = order.get('number-of-items', '')
                row[col_header] = val

            row['WARNINGS'] = MemorialBase.generate_warnings(order) # Calls MemorialBase static method
            data.append(row)

        df = pd.DataFrame(data)
        if not df.empty:
            final_df_columns = [col for col in columns if col in df.columns]
            if final_df_columns:
                 df = df[final_df_columns]

        df.to_csv(filepath, index=False, encoding="utf-8")
        print(f"Generated CSV: {filepath}")

    import sys

if __name__ == "__main__":
    # Usage: python regular_stakes.py <output_dir> <graphics_path>
    import sys
    import pandas as pd
    import os
    from pathlib import Path

    output_dir = sys.argv[1] if len(sys.argv) > 1 else "SVG_OUTPUT"
    graphics_path = sys.argv[2] if len(sys.argv) > 2 else "G:/My Drive/001 NBNE/001 M/M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM/001 Design/002 MUTOH/002 AUTODESIGN"

    orders_txt = str(Path(__file__).parent.parent / "001 AMAZON DATA DOWNLOAD" / "output.txt")
    if not os.path.exists(orders_txt):
        print(f"Error: {orders_txt} does not exist. Please run order processing first.")
        sys.exit(1)

    orders = pd.read_csv(orders_txt, sep='\t', encoding='utf-8')
    print(f"Loaded columns: {list(orders.columns)}")
    print(orders.head())
    processor = RegularStakesProcessor(graphics_path, output_dir)
    processor.process_orders(orders)
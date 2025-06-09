import os
import svgwrite
import pandas as pd
from memorial_base import MemorialBase
# Assuming text_utils and svg_utils might be needed later, import them from core.processors
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
# from core.processors.svg_utils import draw_rounded_rect, add_multiline_text

class ColouredHeartStakesProcessor(MemorialBase):
    # Path data for the heart shape (extracted from the 'd' attribute of path867-2 in the template)
    # The original path starts with 'm 1192.2452,299.64632'.
    # To make it relative to (0,0) if placed at the top-left of its own bounding box,
    # we'd need to find the min_x, min_y of the original path and subtract them.
    # For now, let's store the original path and handle translation during drawing.
    # Or, more simply, assume the blue rectangle's top-left is the (0,0) for the local heart drawing.
    # Original rect30 x="1152.9476", y="315.23886"
    # Original path starts "m 1192.2452,299.64632"
    # Relative path start: m (1192.2452 - 1152.9476), (299.64632 - 315.23886)
    # Relative path start: m 39.2976, -15.59254
    # This relative path can then be used when drawing each heart at its target x,y.

    HEART_PATH_D = "m 39.2976,-15.59254 c -2.4217,-0.0127 -4.8418,0.23512 -7.3792,0.73886 -11.8567,2.35385 -22.321,10.41601 -27.8728,21.4748 -3.8511,7.67115 -4.8915,15.6114 -3.364,25.67697 1.9721,12.99516 8.6953,24.41118 21.4306,36.38936 16.6595,16.61323 44.4944,45.61949 47.6645,45.61949 h 0.3598 c 3.1701,0 31.0051,-29.00626 47.6645,-45.61949 12.7353,-11.97818 19.4585,-23.3942 21.4306,-36.38936 1.5275,-10.06557 0.4871,-18.00582 -3.364,-25.67697 -5.5518,-11.05879 -16.0161,-19.12095 -27.8728,-21.4748 -2.5374,-0.50374 -4.9575,-0.75161 -7.3792,-0.73886 -3.1135,0.0164 -6.2292,0.46357 -9.5988,1.34986 -7.5522,1.98636 -15.0423,6.73007 -20.0796,12.7172 -0.3779,0.44914 -0.7177,0.83885 -0.9806,1.13 -0.2629,-0.29115 -0.6027,-0.68087 -0.9806,-1.13 -5.0373,-5.98714 -12.5274,-10.73084 -20.0796,-12.7172 -3.3696,-0.88629 -6.4853,-1.33345 -9.5988,-1.34986 z"
    # The above path is already relative to the top-left of the original blue bounding box based on calculation.
    # Original blue box: width="139.91298" height="89.8256"
    # These dimensions are in SVG units from the template, which used 'mm' as document units.
    # We will use these as the basis for self.memorial_width_mm and self.memorial_height_mm.

    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = "heart_stakes_graphic_coloured" # Corrected category name

        # Dimensions from the reference blue rectangle in the SVG template
        self.memorial_width_mm = 139.913
        self.memorial_height_mm = 89.826

        # Update pixel dimensions based on these specific mm values
        # self.memorial_width_px = int(self.memorial_width_mm * self.px_per_mm) # To be removed
        # self.memorial_height_px = int(self.memorial_height_mm * self.px_per_mm) # To be removed

        # Page layout for batches (e.g., 3 hearts per page, similar to template)
        # The template page size is 480mm x 330mm.
        # Let's try to fit 3 across. (480 / 140 approx 3 with some spacing)
        self.grid_cols = 3
        self.grid_rows = 1 # For a single row of 3 hearts
        self.batch_size = self.grid_cols * self.grid_rows

        # Override page dimensions if different from MemorialBase default or to match template
        self.page_width_mm = 480
        self.page_height_mm = 330 # As per template
        # self.page_width_px = int(self.page_width_mm * self.px_per_mm) # To be removed
        # self.page_height_px = int(self.page_height_mm * self.px_per_mm) # To be removed

        # Offset calculations for bottom-right placement
        margin_mm = 1.0
        grid_actual_width_mm = self.memorial_width_mm * self.grid_cols
        grid_actual_height_mm = self.memorial_height_mm * self.grid_rows

        self.x_offset_mm = self.page_width_mm - grid_actual_width_mm - margin_mm
        self.y_offset_mm = self.page_height_mm - grid_actual_height_mm - margin_mm

        # self.x_offset_px = int(self.x_offset_mm * self.px_per_mm) # To be removed
        # self.y_offset_px = int(self.y_offset_mm * self.px_per_mm) # To be removed

        # Define font sizes (in points, will be converted to mm/px in drawing method)
        # These are examples, adjust based on visual testing.
        self.line1_font_pt = 10
        self.line2_font_pt = 14
        self.line3_font_pt = 8

        # Placeholder for relative text positions [x_factor, y_factor] of memorial size
        # (e.g., [0.5, 0.3] means centered horizontally, 30% from top for line 1)
        self.line1_rel_pos = [0.5, 0.3] # Relative to memorial bounding box
        self.line2_rel_pos = [0.5, 0.5]
        self.line3_rel_pos = [0.5, 0.7]
        self.graphic_rel_bbox = [0.25, 0.25, 0.5, 0.3] # Relative [x, y, width, height] for graphic placeholder

    def process_orders(self, orders):
        # Input `orders` DataFrame is assumed to be pre-filtered for this processor's category.
        self.log(f"[{self.CATEGORY}] process_orders called with {len(orders)} orders.")

        if not isinstance(orders, pd.DataFrame):
            self.log(f"[{self.CATEGORY}] Input 'orders' is not a DataFrame. Aborting.")
            return
        if orders.empty:
            self.log(f"[{self.CATEGORY}] Input 'orders' DataFrame is empty. Nothing to process.")
            return

        df = orders.copy()

        # Normalize column names
        df.columns = [col.lower().strip() for col in df.columns]

        # Ensure essential columns exist and perform basic type conversions
        required_cols = ['order-id', 'sku', 'line_1', 'line_2', 'line_3', 'graphic', 'number-of-items']
        for col in required_cols:
            if col not in df.columns:
                self.log(f"[{self.CATEGORY}] Warning: Required column '{col}' not found. Orders may not process correctly.")
                df[col] = '' # Add as empty string to prevent key errors later if logic expects it

        df['number-of-items'] = pd.to_numeric(df.get('number-of-items', 1), errors='coerce').fillna(1).astype(int)
        df.loc[df['number-of-items'] <= 0, 'number-of-items'] = 1 # Ensure quantity is at least 1

        # Expand rows by number-of-items
        expanded_rows = []
        for _, row in df.iterrows():
            qty = row.get('number-of-items', 1)
            for _ in range(qty):
                expanded_rows.append(row.copy())

        if not expanded_rows:
            self.log(f"[{self.CATEGORY}] No rows after expansion. Nothing to process.")
            return

        df_expanded = pd.DataFrame(expanded_rows)
        self.log(f"[{self.CATEGORY}] Total items after expansion: {len(df_expanded)}.")

        # Batch processing
        batch_num = 1
        total_items = len(df_expanded)

        for start_idx in range(0, total_items, self.batch_size):
            end_idx = min(start_idx + self.batch_size, total_items)
            batch_df = df_expanded.iloc[start_idx:end_idx]

            if batch_df.empty:
                continue

            self.log(f"[{self.CATEGORY}] Processing batch {batch_num}: {len(batch_df)} items (indices {start_idx}-{end_idx-1}).")

            # Convert batch DataFrame to list of dicts for SVG and CSV methods
            batch_orders_list_of_dicts = batch_df.to_dict('records')

            # Call SVG creation (to be fully implemented in the next step)
            self.create_memorial_svg(batch_orders_list_of_dicts, batch_num)

            # Call CSV creation (to be fully implemented in a later step)
            self.create_batch_csv(batch_orders_list_of_dicts, batch_num, self.CATEGORY)

            batch_num += 1

        self.log(f"[{self.CATEGORY}] Finished processing all batches.")

    # Add a simple log method to the class for now if not inheriting one that prints
    def log(self, message):
        print(message)

    def create_memorial_svg(self, orders_in_batch, batch_num):
        # Ensure necessary imports are at the top of the file:
        # import svgwrite # Already imported at the top of the file
        # import os # Already imported at the top of the file
        import sys # Ensure sys is imported for path manipulation
        # For simplicity in subtask, direct import if text_utils is in core.processors
        # Assuming 'core' is a sibling directory to '002 D2C WRITER' or PYTHONPATH is set up
        # If the script is run from within '002 D2C WRITER', '..' goes to parent, then 'core'
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos


        self.log(f"[{self.CATEGORY}] Creating SVG for batch {batch_num}, {len(orders_in_batch)} items.")

        svg_filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        output_path = os.path.join(self.OUTPUT_DIR, svg_filename)

        # Use mm for viewBox and size
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_mm} {self.page_height_mm}"
        )

        for idx, order_dict in enumerate(orders_in_batch):
            if idx >= self.batch_size:
                break

            # Use mm for item positioning
            item_x_mm = self.x_offset_mm + (idx % self.grid_cols) * self.memorial_width_mm
            item_y_mm = self.y_offset_mm + (idx // self.grid_cols) * self.memorial_height_mm

            stake_group = dwg.g(transform=f"translate({item_x_mm}, {item_y_mm})")

            stake_group.add(dwg.path(
                d=self.HEART_PATH_D,
                stroke=svgwrite.rgb(255, 0, 0, '%'), # Red
                fill='none',
                stroke_width=0.1 # Interpreted as 0.1mm
            ))

            graphic_filename = order_dict.get('graphic', '')
            if graphic_filename and isinstance(graphic_filename, str) and graphic_filename.strip():
                graphic_full_path = os.path.join(self.graphics_path, graphic_filename.strip())
                if os.path.exists(graphic_full_path):
                    embedded_graphic_data = self.embed_image(graphic_full_path)
                    if embedded_graphic_data:
                        gfx_x_mm = self.memorial_width_mm * self.graphic_rel_bbox[0]
                        gfx_y_mm = self.memorial_height_mm * self.graphic_rel_bbox[1]
                        gfx_width_mm = self.memorial_width_mm * self.graphic_rel_bbox[2]
                        gfx_height_mm = self.memorial_height_mm * self.graphic_rel_bbox[3]

                        stake_group.add(dwg.image(
                            href=embedded_graphic_data,
                            insert=(gfx_x_mm, gfx_y_mm),
                            size=(gfx_width_mm, gfx_height_mm), # Use mm
                            preserveAspectRatio='xMidYMid meet'
                        ))
                else:
                    self.log(f"[{self.CATEGORY}] Graphic not found: {graphic_full_path} for order {order_dict.get('order-id')}")

            texts = {
                'line_1': {'text': str(order_dict.get('line_1', '')), 'pt': self.line1_font_pt, 'rel_y': self.line1_rel_pos[1]},
                'line_2': {'text': str(order_dict.get('line_2', '')), 'pt': self.line2_font_pt, 'rel_y': self.line2_rel_pos[1]},
                'line_3': {'text': str(order_dict.get('line_3', '')), 'pt': self.line3_font_pt, 'rel_y': self.line3_rel_pos[1]},
            }

            text_center_x_mm = self.memorial_width_mm * 0.5

            for key, val in texts.items():
                if val['text'].strip():
                    check_grammar_and_typos(val['text'])
                    font_size_mm = val['pt'] * self.pt_to_mm
                    abs_y_mm = self.memorial_height_mm * val['rel_y']

                    # Estimate max_chars using mm dimensions (more intuitive)
                    # Approx char width in mm: font_size_mm * 0.5 or 0.6
                    char_width_estimate_mm = font_size_mm * 0.5
                    effective_text_width_mm = self.memorial_width_mm * 0.7 # Allow text to use 70% of heart width
                    max_chars_per_line = int(effective_text_width_mm / char_width_estimate_mm) if char_width_estimate_mm > 0 else 25


                    processed_lines = []
                    for input_line in val['text'].split('\n'):
                        for sub_line in input_line.split('\\n'):
                           for s_line in sub_line.splitlines():
                                wrapped = split_line_to_fit(s_line, max_chars_per_line)
                                processed_lines.extend(wrapped)

                    num_lines = len(processed_lines)
                    line_height_mm = font_size_mm * 1.2 # 1.2em line spacing in mm

                    block_start_y_mm = abs_y_mm - ((num_lines - 1) * line_height_mm / 2)

                    text_element = dwg.text("",
                        insert=(text_center_x_mm, block_start_y_mm),
                        font_family="Georgia",
                        font_size=f"{font_size_mm}mm", # Explicitly use mm
                        fill="black",
                        text_anchor="middle"
                    )
                    for line_idx, line_content in enumerate(processed_lines):
                        # dy for tspan can be in 'em' or absolute units like 'mm'
                        # Using 'em' is generally better for multi-line text within a text block
                        dy_val = "1.2em" if line_idx > 0 else "0"
                        tspan = dwg.tspan(line_content.strip(), x=[text_center_x_mm], dy=[dy_val])
                        text_element.add(tspan)
                    stake_group.add(text_element)

            dwg.add(stake_group)

        # Add reference point using mm
        ref_size_mm = 0.1
        ref_x_mm = self.page_width_mm - ref_size_mm
        ref_y_mm = self.page_height_mm - ref_size_mm
        dwg.add(dwg.rect(insert=(ref_x_mm, ref_y_mm), size=(ref_size_mm, ref_size_mm), fill='blue'))

        try:
            dwg.save()
            self.log(f"[{self.CATEGORY}] SVG file saved: {output_path}")
        except Exception as e:
            self.log(f"[{self.CATEGORY}] Error saving SVG file {output_path}: {e}")

    def create_batch_csv(self, orders_in_batch, batch_num, category_name):
        # Ensure necessary imports are at the top of the file:
        # import os # Already imported
        # import pandas as pd # Already imported
        # from memorial_base import MemorialBase # Already inherited

        self.log(f"[{self.CATEGORY}] Creating CSV for batch {batch_num}, {len(orders_in_batch)} items.")

        # Filename generation using self.date_str from MemorialBase
        svg_reference_filename = f"{category_name}_{self.date_str}_{batch_num:03d}.svg"
        csv_filename = f"{category_name}_{self.date_str}_{batch_num:03d}.csv"
        design_file_ref = f"{category_name}_{self.date_str}_{batch_num:03d}"
        filepath = os.path.join(self.OUTPUT_DIR, csv_filename)

        # Column Definition
        # Collect all unique keys from orders_in_batch to ensure all data can be captured if needed
        all_order_keys = set()
        if orders_in_batch: # Ensure there are orders to process
            for order in orders_in_batch:
                if isinstance(order, dict):
                    all_order_keys.update(k.upper() for k in order.keys())

        preferred_columns = [
            'SVG FILE', 'DESIGN FILE', 'ORDER-ID', 'ORDER-ITEM-ID', 'SKU',
            'NUMBER-OF-ITEMS', 'TYPE', 'COLOUR', 'GRAPHIC',
            'LINE_1', 'LINE_2', 'LINE_3', 'THEME', # Assuming 'THEME' might be relevant
            # 'IMAGE_PATH' is not typically for graphic stakes, but can be included if some hearts might use it
            'ATTENTION_FLAG', 'WARNINGS'
        ]

        # Combine preferred columns with any other keys found in the data
        # Ensuring preferred columns come first and maintain their order
        extra_columns = sorted(list(all_order_keys - set(p.upper() for p in preferred_columns)))
        final_columns = preferred_columns + extra_columns

        data_for_csv = []
        for order_dict in orders_in_batch:
            if not isinstance(order_dict, dict):
                self.log(f"[{self.CATEGORY}] Warning: order_dict is not a dictionary. Skipping. {type(order_dict)}")
                continue

            row_dict = {}
            row_dict['SVG FILE'] = svg_reference_filename
            row_dict['DESIGN FILE'] = design_file_ref

            # Populate ATTENTION_FLAG
            # Using similar logic to RegularStakesProcessor for consistency
            attention_messages = []
            order_colour_lower = str(order_dict.get('colour', '')).lower()
            # For Heart Stakes, specific attention flags might differ, adjust as needed.
            # Example: Checking for rare colours if applicable for coloured hearts.
            if order_colour_lower in ['marble', 'stone']: # If these are considered rare for hearts
                attention_messages.append(f"RARE_COLOUR: {str(order_dict.get('colour','')).upper()}")

            # Add other heart-specific attention flags if any
            # e.g., if order_dict.get('TYPE', '').lower() == 'special_heart_type':
            #    attention_messages.append("Special Heart Type")
            row_dict['ATTENTION_FLAG'] = "; ".join(attention_messages) if attention_messages else ""


            # Populate WARNINGS using MemorialBase static method
            row_dict['WARNINGS'] = MemorialBase.generate_warnings(order_dict)

            # Populate other columns
            for col_header in final_columns:
                if col_header not in row_dict: # Avoid overwriting SVG FILE, DESIGN FILE, etc.
                    # Try various casings for robustness, falling back to empty string
                    val = order_dict.get(col_header.lower(),                           order_dict.get(col_header.upper(),                           order_dict.get(col_header.title(), '')))
                    row_dict[col_header] = val

            data_for_csv.append(row_dict)

        if not data_for_csv:
            self.log(f"[{self.CATEGORY}] No data to write to CSV for batch {batch_num}.")
            return

        # DataFrame Creation and Save
        try:
            df = pd.DataFrame(data_for_csv)

            # Ensure all columns from final_columns are present in the DataFrame, adding if missing
            for col in final_columns:
                if col not in df.columns:
                    df[col] = "" # Add missing columns as empty strings

            df = df[final_columns] # Reorder/select columns to match final_columns list

            df.to_csv(filepath, index=False, encoding="utf-8-sig")
            self.log(f"[{self.CATEGORY}] CSV file saved: {filepath}")
        except Exception as e:
            self.log(f"[{self.CATEGORY}] Error saving CSV file {filepath}: {e}")

# Example of how to use (for testing, not part of the class itself)
if __name__ == '__main__':
    # This section would be for testing the processor independently.
    # For now, it's just a placeholder.
    print("ColouredHeartStakesProcessor defined.")
    # mock_graphics_path = "path/to/graphics"
    # mock_output_dir = "SVG_OUTPUT_HEART_TEST"
    # os.makedirs(mock_output_dir, exist_ok=True)
    # processor = ColouredHeartStakesProcessor(mock_graphics_path, mock_output_dir)
    # print(f"Initialized {processor.CATEGORY} processor.")
    # print(f"Memorial size: {processor.memorial_width_mm}mm x {processor.memorial_height_mm}mm")
    # print(f"Page size: {processor.page_width_mm}mm x {processor.page_height_mm}mm")
    # print(f"Grid: {processor.grid_cols}x{processor.grid_rows}")
    # print(f"Offsets: x={processor.x_offset_mm}mm, y={processor.y_offset_mm}mm")

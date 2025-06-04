import os
import svgwrite
import pandas as pd
from datetime import datetime # Keep for potential use in filename generation
from pathlib import Path

from core.processors.base import ProcessorBase
from core.processors import register_processor
from core.processors.text_utils import TextUtils # Assuming TextUtils class
from core.processors.svg_utils import SVGUtils # Assuming SVGUtils class
from .text_utils import create_batch_csv # Changed to import from local text_utils

class RegularStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = TextUtils() # Initialize TextUtils
        self.svg_utils = SVGUtils()   # Initialize SVGUtils

        # Constants from original class (might need refactoring or be part of SVGUtils)
        self.CATEGORY = 'COLOUR' # Used in original filename, might need to be dynamic
        self.grid_cols = 3
        self.grid_rows = 3
        self.batch_size = self.grid_cols * self.grid_rows # Page generation logic

        # Conversion factors
        self.px_per_mm = 1 / 0.26458333333
        self.pt_to_mm = 0.2645833333

        # Memorial and page dimensions (specific to this processor's output format)
        self.memorial_width_mm = 140
        self.memorial_height_mm = 90
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.memorial_width_px = self.memorial_width_mm * self.px_per_mm
        self.memorial_height_px = self.memorial_height_mm * self.px_per_mm
        self.page_width_px = self.page_width_mm * self.px_per_mm
        self.page_height_px = self.page_height_mm * self.px_per_mm

        # Centering offsets for page grid
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows
        self.x_offset_mm = (self.page_width_mm - grid_width_mm) / 2
        self.y_offset_mm = (self.page_height_mm - grid_height_mm) / 2
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

        # Text sizes (in points)
        self.line1_size_pt = 17 * 1.2
        self.line2_size_pt = 25 * 1.2
        self.line3_size_pt = 12 * 1.1

        # Stroke width and corner radius
        self.stroke_width = 0.1 * self.px_per_mm
        self.corner_radius_px = 6 * self.px_per_mm

        # Date string for batch naming (from MemorialBase)
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")


    def is_applicable(self, order_data: pd.Series) -> bool:
        """
        Checks if this processor is applicable for the given order.
        Applicable if type is 'regular stake', decorationtype is 'graphic',
        and colour is not 'black'.
        """
        order_type = str(order_data.get('type', '')).strip().lower()
        decoration_type = str(order_data.get('decorationtype', '')).strip().lower()
        colour = str(order_data.get('colour', '')).strip().lower()

        return (order_type == 'regular stake' and
                decoration_type == 'graphic' and
                colour != 'black')

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        """
        Processes the given order data and generates SVG file(s).
        The input order_data is already filtered by is_applicable.
        """
        print("[DEBUG] Entered RegularStakesProcessor.process")

        # Update instance paths if they differ (though typically set in __init__)
        self.output_dir = output_dir
        self.graphics_path = graphics_path
        os.makedirs(self.output_dir, exist_ok=True)

        if order_data.empty:
            print("No orders to process for RegularStakesProcessor.")
            return

        # Columns are already lowercased by the main application or should be
        # df = order_data.copy() # order_data is already a DataFrame

        # Expand rows by number-of-items - this logic should apply per order
        # For now, assuming process is called for a batch that is already expanded or handled one-by-one.
        # If process is called for individual items, expansion might not be needed here.
        # The current design implies process gets a DataFrame of applicable orders.
        # If an order has qty > 1, it should appear multiple times in order_data or be handled by caller.
        # For simplicity, let's assume each row in order_data is one item to generate.

        # The original code had complex filtering and sorting.
        # The new model is that `order_data` passed to `process` is *already* filtered.
        # Sorting for batching might still be relevant if generating multi-item SVGs.

        # The original `process_orders` batched items into 9-per-page SVGs.
        # This `process` method should adapt that.

        df_to_process = order_data.copy()

        # Sorting by color_priority was part of batching in original code
        allowed_colours_map = {'copper': 0, 'gold': 1, 'silver': 2, 'stone': 3, 'marble': 4} # Others get NaN
        df_to_process['color_priority'] = df_to_process['colour'].map(allowed_colours_map)
        df_to_process = df_to_process.sort_values('color_priority').reset_index(drop=True)


        batch_num = 1
        total_items = len(df_to_process)

        if total_items == 0:
            print("No applicable Regular Stakes orders after internal filtering/preparation.")
            return

        for start_idx in range(0, total_items, self.batch_size):
            end_idx = min(start_idx + self.batch_size, total_items)
            current_batch_df = df_to_process.iloc[start_idx:end_idx]

            if not current_batch_df.empty:
                orders_for_svg = current_batch_df.to_dict('records')

                # Define a unique filename for the batch SVG
                # Example: regular_stakes_20231027_153000_batch_001.svg
                # If processing single items, filename should be per-item.
                # The current structure implies batching into pages.

                # For single file processing (if batch_size is 1 or called per item)
                if len(orders_for_svg) == 1:
                    order = orders_for_svg[0]
                    order_id = str(order.get('order-id', 'NO_ID')).strip()
                    sku = str(order.get('sku', 'NO_SKU')).strip()
                    graphic_val = str(order.get('graphic', 'NO_GRAPHIC')).strip().replace('.png', '')
                    filename = f"REGULAR_{order_id}_{sku}_{graphic_val}.svg"
                    # Create a "page" SVG with just one item
                    self._create_memorial_page_svg(orders_for_svg, batch_num, filename)
                else: # Batch processing into a page
                    page_filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"
                    self._create_memorial_page_svg(orders_for_svg, batch_num, page_filename)

                create_batch_csv(orders_for_svg, batch_num, self.CATEGORY, self.output_dir, self.date_str)
                print(f"Processed batch {batch_num} for Regular Stakes.")
                batch_num += 1

    def _create_memorial_page_svg(self, orders_in_batch: list, batch_number: int, filename: str):
        """
        Creates a single SVG page with multiple memorials from the batch.
        orders_in_batch: A list of order dictionaries for the current page.
        batch_number: The current batch number (for logging).
        filename: The desired filename for the SVG.
        """
        output_path = os.path.join(self.output_dir, filename)

        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )

        for idx_in_page in range(len(orders_in_batch)): # Iterate only for actual orders in batch
            order_item = orders_in_batch[idx_in_page]

            row_on_page = idx_in_page // self.grid_cols
            col_on_page = idx_in_page % self.grid_cols

            x_pos = self.x_offset_px + (col_on_page * self.memorial_width_px)
            y_pos = self.y_offset_px + (row_on_page * self.memorial_height_px)

            # Draw placeholder rect for the item slot (optional, for debugging)
            dwg.add(dwg.rect(
                insert=(x_pos, y_pos),
                size=(self.memorial_width_px, self.memorial_height_px),
                rx=self.corner_radius_px,
                ry=self.corner_radius_px,
                fill='none',
                stroke='grey', # Changed from red to grey
                stroke_width=self.stroke_width / 2 # Thinner
            ))

            # --- Apply graphic ---
            # TODO: self.embed_image was from MemorialBase. This needs to be SVGUtils.embed_image or similar.
            # For now, assuming self.svg_utils.embed_image(path) exists.
            graphic_filename = str(order_item.get('graphic', '')).strip()
            if graphic_filename:
                # Special handling for OM008021 (if still needed, though is_applicable should filter it out if it's B&W)
                # This processor is for COLOUR regular stakes. OM008021 might be B&W.
                # The original logic had a hardcoded G: drive path which is not portable.
                # Assuming graphics are found via self.graphics_path
                if graphic_filename.upper() == 'OM008021.PNG' or graphic_filename.upper() == 'OM008021':
                     # This SKU might need special handling or its own processor if rules are complex.
                     # For now, treat as a regular graphic if found in graphics_path.
                     pass # Let it be handled by the generic graphic logic below.

                graphic_full_path = os.path.join(self.graphics_path, graphic_filename)
                if os.path.exists(graphic_full_path):
                    try:
                        # Assuming svg_utils.embed_image returns base64 encoded string
                        embedded_image_data = self.svg_utils.embed_image(graphic_full_path)
                        if embedded_image_data:
                            dwg.add(dwg.image(
                                href=embedded_image_data,
                                insert=(x_pos, y_pos),
                                size=(self.memorial_width_px, self.memorial_height_px)
                            ))
                        else:
                            print(f"Warning: Failed to embed graphic {graphic_filename} for order {order_item.get('order-id')}")
                    except Exception as e:
                        print(f"Error embedding graphic {graphic_filename}: {e}")
                else:
                    print(f"Warning: Graphic file not found: {graphic_full_path} for order {order_item.get('order-id')}")

            # --- Add Text ---
            center_x_abs = x_pos + (self.memorial_width_px / 2)

            for line_key, y_offset_mm, font_size_pt, max_chars_override in [
                ('line_1', 28, self.line1_size_pt, None),
                ('line_2', 45, self.line2_size_pt, None),
                ('line_3', 57, self.line3_size_pt, 30) # line_3 has special multiline logic
            ]:
                text_content = str(order_item.get(line_key, '')).strip()
                if not text_content: # Skip empty lines
                    continue

                # Grammar/Typo check (from TextUtils)
                # text_content = self.text_utils.check_grammar_and_typos(text_content) # Assuming this method exists

                font_family = "Georgia" # TODO: Make configurable or part of TextUtils
                fill_color = "black"    # TODO: Make configurable

                if line_key == 'line_3':
                    # Special multiline handling for line_3
                    font_size_mm = font_size_pt * self.pt_to_mm
                    char_width_approx_mm = 0.5 * font_size_mm # Rough estimation
                    max_line_width_mm = self.memorial_width_mm * 0.6 # 60% of memorial width

                    # Use max_chars_override if provided (e.g. 30 for single line before splitting)
                    # otherwise calculate based on available width
                    effective_max_chars = max_chars_override if max_chars_override else int(max_line_width_mm / char_width_approx_mm)

                    lines_to_draw = self.text_utils.split_line_to_fit_multiline(text_content, effective_max_chars, 5) # Max 5 lines for line_3

                    # Conditional font size for Line 3 based on original logic
                    total_chars_line3 = sum(len(line) for line in lines_to_draw)
                    if 10 <= total_chars_line3 <= 30 and len(lines_to_draw) <=2 : # Adjusted logic
                        current_font_size_pt = self.line1_size_pt
                    elif 31 <= total_chars_line3 <= 90 and len(lines_to_draw) <=3: # Adjusted logic
                        current_font_size_pt = self.line1_size_pt * 0.9
                    else:
                        current_font_size_pt = font_size_pt # Default line3_size_pt

                    if lines_to_draw:
                        self.svg_utils.add_multiline_text(
                            dwg, lines_to_draw,
                            insert_x=center_x_abs, insert_y=(y_pos + y_offset_mm * self.px_per_mm),
                            font_size_mm=(current_font_size_pt * self.pt_to_mm),
                            font_family=font_family, text_anchor="middle", fill=fill_color
                        )
                else: # line_1, line_2 (single line centered)
                     self.svg_utils.add_text(
                         dwg, text_content,
                         insert_x=center_x_abs, insert_y=(y_pos + y_offset_mm * self.px_per_mm),
                         font_size_mm=(font_size_pt * self.pt_to_mm),
                         font_family=font_family, text_anchor="middle", fill=fill_color
                     )

        # Add reference point (bottom right corner of the page)
        ref_size_px = 0.1 * self.px_per_mm
        dwg.add(dwg.rect(
            insert=(self.page_width_px - ref_size_px, self.page_height_px - ref_size_px),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))

        try:
            dwg.save(pretty=True) # pretty=True for readable SVG
            print(f"SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving SVG {output_path}: {e}")

# Register the processor
register_processor("regular_stakes", RegularStakesProcessor)

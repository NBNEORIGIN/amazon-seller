import os
import svgwrite
import pandas as pd
from datetime import datetime # For self.date_str, similar to MemorialBase

from core.processors.base import ProcessorBase
from core.processors import register_processor
from . import text_utils # Changed to module import
from . import svg_utils   # Changed to module import
# Removed specific create_batch_csv import, will use text_utils.create_batch_csv

class BWStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = text_utils # Assign module
        self.svg_utils = svg_utils     # Assign module

        self.CATEGORY = 'B&W' # Used for filename generation
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Constants for page layout - these were implicitly part of MemorialBase or set there
        # It's better to define them here if they are specific to this processor's output format
        self.px_per_mm = 1 / 0.26458333333
        self.pt_to_mm = 0.2645833333
        self.memorial_width_mm = 140
        self.memorial_height_mm = 90
        self.page_width_mm = 439.8  # Standard page width for 3 memorials
        self.page_height_mm = 289.9 # Standard page height (can fit more rows if needed)

        self.memorial_width_px = self.memorial_width_mm * self.px_per_mm
        self.memorial_height_px = self.memorial_height_mm * self.px_per_mm
        self.page_width_px = self.page_width_mm * self.px_per_mm
        self.page_height_px = self.page_height_mm * self.px_per_mm

        # B&W stakes are typically 3 in a row on the top of the page
        self.grid_cols = 3
        self.grid_rows = 1 # Typically only one row for B&W stakes on a page.
                           # If more are needed, this can be adjusted, or multiple pages generated.
        self.batch_size = self.grid_cols * self.grid_rows # Max 3 items per SVG page

        # Centering offsets for the grid on the page
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows # Only one row high
        self.x_offset_mm = (self.page_width_mm - grid_width_mm) / 2
        self.y_offset_mm = (self.page_height_mm - grid_height_mm) / 2 # This will center the single row
        # If strictly top row, y_offset_mm could be a fixed small margin.
        # For now, using the same centering logic as regular_stakes for flexibility.
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

        # Text sizes (in points) - ensure these match desired output for B&W
        self.line1_size_pt = 17 * 1.2
        self.line2_size_pt = 25 * 1.2
        self.line3_size_pt = 12 * 1.1


    def is_applicable(self, order_data: pd.Series) -> bool:
        order_type = str(order_data.get('type', '')).strip().lower()
        decoration_type = str(order_data.get('decorationtype', '')).strip().lower()
        colour = str(order_data.get('colour', '')).strip().lower()

        return (order_type == 'regular stake' and
                decoration_type == 'graphic' and
                colour == 'black')

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        self.output_dir = output_dir # Update in case it's different from __init__
        self.graphics_path = graphics_path
        os.makedirs(self.output_dir, exist_ok=True)

        if order_data.empty:
            print("[BW DEBUG] No B&W stakes to process.")
            return

        # Ensure 'graphic' column exists and handle NaN, as it's critical for B&W stakes
        if 'graphic' not in order_data.columns:
            print("[BW DEBUG] 'graphic' column missing. Cannot process B&W stakes.")
            return

        # Filter out orders where graphic is NaN, as B&W stakes rely on graphics
        # This was done in the original `bw_stakes` after expansion.
        df_to_process = order_data[order_data['graphic'].notna()].copy()

        if df_to_process.empty:
            print("[BW DEBUG] No B&W stakes with valid graphic data to process.")
            return

        print(f"[BW DEBUG] Processing {len(df_to_process)} B&W Stakes orders.")

        batch_num = 1
        total_items = len(df_to_process)

        for start_idx in range(0, total_items, self.batch_size): # self.batch_size is 3 for B&W
            end_idx = min(start_idx + self.batch_size, total_items)
            current_batch_df = df_to_process.iloc[start_idx:end_idx]

            if not current_batch_df.empty:
                orders_for_svg = current_batch_df.to_dict('records')

                # Filename generation
                # If processing single items (e.g. from "Create Design for Selected")
                if len(orders_for_svg) == 1:
                    order = orders_for_svg[0]
                    order_id = str(order.get('order-id', 'NO_ID')).strip()
                    sku = str(order.get('sku', 'NO_SKU')).strip()
                    graphic_val = str(order.get('graphic', 'NO_GRAPHIC')).strip().replace('.png', '')
                    filename = f"BW_STAKE_{order_id}_{sku}_{graphic_val}.svg"
                else: # Batch processing into a page
                    filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"

                self._create_memorial_page_svg(orders_for_svg, filename)

                self.text_utils.create_batch_csv(orders_for_svg, batch_num, self.CATEGORY, self.output_dir, self.date_str)
                print(f"Processed B&W batch {batch_num}.")
                batch_num += 1

    def _create_memorial_page_svg(self, orders_in_batch: list, filename: str):
        output_path = os.path.join(self.output_dir, filename)

        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )

        # Process up to 3 memorials, always in the top row (row_on_page = 0)
        for idx_in_page, order_item in enumerate(orders_in_batch):
            if idx_in_page >= self.batch_size: # Max 3 items for B&W stakes page layout
                break

            row_on_page = 0  # Always top row for this layout
            col_on_page = idx_in_page

            x_pos = self.x_offset_px + (col_on_page * self.memorial_width_px)
            y_pos = self.y_offset_px + (row_on_page * self.memorial_height_px) # y_offset_px should place it in the top part

            # Add memorial outline (optional, for alignment check)
            dwg.add(dwg.rect(
                insert=(x_pos, y_pos),
                size=(self.memorial_width_px, self.memorial_height_px),
                rx=(6 * self.px_per_mm), ry=(6 * self.px_per_mm), # Corner radius
                fill='none', stroke='grey', stroke_width=(0.1 * self.px_per_mm / 2)
            ))

            graphic_filename = str(order_item.get('graphic', '')).strip()
            if graphic_filename: # Graphic is expected for B&W stakes
                graphic_full_path = os.path.join(self.graphics_path, graphic_filename)
                if os.path.exists(graphic_full_path):
                    try:
                        # Assuming svg_utils.embed_image handles conversion to base64
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
            else:
                 print(f"Warning: Missing graphic for B&W stake, order {order_item.get('order-id')}")

            center_x_abs = x_pos + (self.memorial_width_px / 2)

            # Text lines (similar to RegularStakesProcessor, ensure TextUtils methods are robust)
            for line_key, y_offset_mm, font_size_pt, max_chars_override in [
                ('line_1', 28, self.line1_size_pt, None),
                ('line_2', 45, self.line2_size_pt, None),
                ('line_3', 57, self.line3_size_pt, 30)
            ]:
                text_content = str(order_item.get(line_key, '')).strip()
                if not text_content: continue

                font_family = "Georgia"
                fill_color = "black"

                if line_key == 'line_3':
                    font_size_mm = font_size_pt * self.pt_to_mm
                    char_width_approx_mm = 0.5 * font_size_mm
                    max_line_width_mm = self.memorial_width_mm * 0.6
                    effective_max_chars = max_chars_override if max_chars_override else int(max_line_width_mm / char_width_approx_mm)

                    # Use self.text_utils.wrap_text or similar from TextUtils for line splitting
                    # Original BWStakes used self.wrap_text - assuming this is now in TextUtils
                    # For now, let's use a placeholder similar to regular_stakes
                    lines_to_draw = self.text_utils.split_line_to_fit_multiline(text_content, effective_max_chars, 5)


                    total_chars_line3 = sum(len(line) for line in lines_to_draw)
                    if 10 <= total_chars_line3 <= 30 and len(lines_to_draw) <=2 :
                        current_font_size_pt = self.line1_size_pt
                    elif 31 <= total_chars_line3 <= 90 and len(lines_to_draw) <=3:
                        current_font_size_pt = self.line1_size_pt * 0.9
                    else:
                        current_font_size_pt = font_size_pt

                    if lines_to_draw:
                        self.svg_utils.add_multiline_text(
                            dwg, lines_to_draw,
                            insert_x=center_x_abs, insert_y=(y_pos + y_offset_mm * self.px_per_mm),
                            font_size_mm=(current_font_size_pt * self.pt_to_mm),
                            font_family=font_family, text_anchor="middle", fill=fill_color
                        )
                else:
                     self.svg_utils.add_text(
                         dwg, text_content,
                         insert_x=center_x_abs, insert_y=(y_pos + y_offset_mm * self.px_per_mm),
                         font_size_mm=(font_size_pt * self.pt_to_mm),
                         font_family=font_family, text_anchor="middle", fill=fill_color
                     )

        # Add reference point (bottom right of the page)
        ref_size_px = 0.1 * self.px_per_mm
        # Original y_pos for ref point was: (289.8 - 0.011) * self.px_per_mm - ref_size_px
        # Using self.page_height_px for consistency
        dwg.add(dwg.rect(
            insert=(self.page_width_px - ref_size_px, self.page_height_px - ref_size_px),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))

        try:
            dwg.save(pretty=True)
            print(f"B&W Stake SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving B&W SVG {output_path}: {e}")

# Register the processor
register_processor("bw_stakes", BWStakesProcessor)

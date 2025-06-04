import os
import svgwrite
import pandas as pd
from datetime import datetime
import traceback # For more detailed error logging

from core.processors.base import ProcessorBase
from core.processors import register_processor
from . import text_utils # Changed to module import
from . import svg_utils   # Changed to module import
# Removed specific create_batch_csv import, will use text_utils.create_batch_csv

class ColouredLargePhotoStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        self.graphics_path = graphics_path # General graphics, less used here
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = text_utils # Assign module
        self.svg_utils = svg_utils     # Assign module

        self.CATEGORY = 'COLOURED_LARGE_PHOTO_STAKES'
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Constants from original, px_per_mm seems to be a local override or fallback
        self.px_per_mm = 3.78 # Specific to this processor's context in original file
        self.pt_to_mm = 0.3528 # Standard pt to mm

        # Item dimensions for Coloured Large Photo Stakes
        self.memorial_width_mm = 200
        self.memorial_height_mm = 120
        self.corner_radius_mm = 6

        # Photo dimensions and margins (in mm)
        self.photo_width_mm = 50.5
        self.photo_height_mm = 68.8
        self.photo_clip_width_mm = 50.378
        self.photo_clip_height_mm = 68.901
        self.photo_border_stroke_mm = 3.65
        self.photo_outline_stroke_mm = 0.5
        self.photo_corner_radius_mm = 6
        self.photo_left_margin_mm = 7.7
        self.text_right_shift_mm = 30 # Gap from photo to text area

        # Convert dimensions to pixels using self.px_per_mm
        self.memorial_width_px = self.memorial_width_mm * self.px_per_mm
        self.memorial_height_px = self.memorial_height_mm * self.px_per_mm
        self.corner_radius_px = self.corner_radius_mm * self.px_per_mm

        self.photo_width_px = self.photo_width_mm * self.px_per_mm
        self.photo_height_px = self.photo_height_mm * self.px_per_mm
        self.photo_clip_width_px = self.photo_clip_width_mm * self.px_per_mm
        self.photo_clip_height_px = self.photo_clip_height_mm * self.px_per_mm
        self.photo_border_stroke_px = self.photo_border_stroke_mm * self.px_per_mm
        self.photo_outline_stroke_px = self.photo_outline_stroke_mm * self.px_per_mm
        self.photo_corner_radius_px = self.photo_corner_radius_mm * self.px_per_mm
        self.photo_left_margin_px = self.photo_left_margin_mm * self.px_per_mm
        self.text_right_shift_px = self.text_right_shift_mm * self.px_per_mm

        # Page dimensions (assuming similar to other multi-item pages if not specified)
        # The original __init__ used self.page_width_mm etc. from MemorialBase.
        # Let's use typical A4-like dimensions for now if batching, adjust if needed.
        # From regular_stakes: page_width_mm = 439.8, page_height_mm = 289.9
        # These might need to be defined in a shared config or base if common.
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.page_width_px = self.page_width_mm * self.px_per_mm
        self.page_height_px = self.page_height_mm * self.px_per_mm

        # Grid layout (2x2 for 4 items per page)
        self.grid_cols = 2
        self.grid_rows = 2
        self.batch_size = self.grid_cols * self.grid_rows

        # Alignment (original was right and bottom of page)
        grid_total_width_px = self.memorial_width_px * self.grid_cols
        grid_total_height_px = self.memorial_height_px * self.grid_rows
        self.x_offset_px = self.page_width_px - grid_total_width_px # Align grid to right
        self.y_offset_px = self.page_height_px - grid_total_height_px # Align grid to bottom
        # Consider adding a small margin from page edge if needed.

        # Text sizes (pt)
        self.line1_size_pt = 17
        self.line2_size_pt = 25
        self.line3_size_pt = 12 # From original line_3 rendering: 12 * self.pt_to_mm

    def is_applicable(self, order_data: pd.Series) -> bool:
        order_type = str(order_data.get('type', '')).strip().lower()
        decoration_type = str(order_data.get('decorationtype', '')).strip().lower()
        colour = str(order_data.get('colour', '')).strip().lower()

        # Ensure it's a coloured photo stake (not black)
        # Allowed colours from original: ['copper', 'gold', 'silver', 'stone', 'marble']
        is_coloured = colour in ['copper', 'gold', 'silver', 'stone', 'marble']

        return (order_type == 'large stake' and
                decoration_type == 'photo' and
                is_coloured and # Explicitly check for allowed colours
                pd.notna(order_data.get('image_path')) and str(order_data.get('image_path')).strip() != '')

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        self.output_dir = output_dir
        # self.graphics_path is for general assets; image_path comes from order_data
        os.makedirs(self.output_dir, exist_ok=True)

        if order_data.empty:
            print("No Coloured Large Photo Stakes orders to process.")
            return

        # Already filtered by is_applicable, which includes image_path check
        df_to_process = order_data.copy()
        print(f"Processing {len(df_to_process)} Coloured Large Photo Stakes.")

        batch_num = 1
        total_items = len(df_to_process)

        for start_idx in range(0, total_items, self.batch_size): # self.batch_size is 4
            end_idx = min(start_idx + self.batch_size, total_items)
            current_batch_df = df_to_process.iloc[start_idx:end_idx]

            if not current_batch_df.empty:
                orders_for_svg_page = current_batch_df.to_dict('records')

                if len(orders_for_svg_page) == 1:
                    order = orders_for_svg_page[0]
                    order_id = str(order.get('order-id', 'NO_ID')).strip()
                    sku = str(order.get('sku', 'NO_SKU')).strip()
                    filename = f"CL_PHOTO_STAKE_{order_id}_{sku}.svg"
                else:
                    filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"

                self._create_memorial_page_svg(orders_for_svg_page, filename)
                self.text_utils.create_batch_csv(orders_for_svg_page, batch_num, self.CATEGORY, self.output_dir, self.date_str)
                batch_num += 1

    def _add_item_to_svg_page(self, dwg, x_item_start: float, y_item_start: float, order_details: dict):
        """Adds a single Coloured Large Photo Stake item to the SVG drawing."""
        try:
            # Memorial outline (overall item boundary)
            self.svg_utils.draw_rounded_rect(dwg, insert=(x_item_start, y_item_start),
                                             size=(self.memorial_width_px, self.memorial_height_px),
                                             rx=self.corner_radius_px, ry=self.corner_radius_px,
                                             fill='none', stroke='black', stroke_width=1) # Thin black outline for item

            # Photo area calculations
            photo_frame_x = x_item_start + self.photo_left_margin_px
            photo_frame_y = y_item_start + (self.memorial_height_px - self.photo_height_px) / 2 # Vertically center photo area

            # Photo background/placeholder rectangle (e.g., white)
            self.svg_utils.draw_rounded_rect(dwg, insert=(photo_frame_x, photo_frame_y),
                                             size=(self.photo_width_px, self.photo_height_px), # Use photo_width_px for visual frame
                                             rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px,
                                             fill='white', stroke='black', stroke_width=self.photo_outline_stroke_px)

            # Clipping path for the photo
            clip_id = f"clip_clp_{x_item_start}_{y_item_start}_{order_details.get('order-id','id')}"
            clip_path = dwg.defs.add(dwg.clipPath(id=clip_id))
            clip_path.add(dwg.rect(insert=(photo_frame_x, photo_frame_y), # Clip to the visual photo area
                                   size=(self.photo_width_px, self.photo_height_px),
                                   rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px))

            # Embed the actual photo image
            image_path_str = str(order_details.get('image_path', '')).strip()
            if image_path_str and os.path.exists(image_path_str):
                embedded_image_data = self.svg_utils.embed_image(image_path_str)
                if embedded_image_data:
                    dwg.add(dwg.image(href=embedded_image_data, insert=(photo_frame_x, photo_frame_y),
                                      size=(self.photo_width_px, self.photo_height_px),
                                      clip_path=f'url(#{clip_id})', preserveAspectRatio='xMidYMid slice'))
            else:
                print(f"Warning: Image path not found or invalid: {image_path_str} for order {order_details.get('order-id')}")

            # Photo border (drawn on top of the photo, if distinct from the placeholder above)
            # The original 'draw_rounded_rect' for border was after the blue outline in `add_photo_memorial`.
            # Here, we rely on the placeholder rect's stroke or add another one if thicker/different.
            # The original also had a `photo_border_stroke_px`.
            # Let's ensure a visible border as per original:
            dwg.add(dwg.rect(insert=(photo_frame_x, photo_frame_y), size=(self.photo_width_px, self.photo_height_px),
                             rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px,
                             fill='none', stroke='black', stroke_width=self.photo_border_stroke_px))


            # Text area calculations
            text_area_x_start = photo_frame_x + self.photo_width_px + self.text_right_shift_px
            text_area_width = x_item_start + self.memorial_width_px - text_area_x_start - self.photo_left_margin_px # Adjust for right margin
            text_center_x = text_area_x_start + text_area_width / 2

            # Text lines
            line_y_offsets_mm = {'line_1': 28, 'line_2': 45, 'line_3': 57} # mm from item top to text baseline
            font_sizes = {'line_1': self.line1_size_pt, 'line_2': self.line2_size_pt, 'line_3': 12} # pt

            for line_key in ['line_1', 'line_2', 'line_3']:
                text_content = str(order_details.get(line_key, '')).strip()
                if text_content:
                    y_abs_px = y_item_start + (line_y_offsets_mm[line_key] * self.px_per_mm)
                    font_size_final_pt = font_sizes[line_key]

                    if line_key == 'line_3':
                        # Use TextUtils for potentially multi-line text:
                        lines = self.text_utils.split_line_to_fit_multiline(text_content, max_chars_per_line=30, max_lines=2) # Example values
                        self.svg_utils.add_multiline_text(dwg, lines, insert_x=text_center_x, insert_y=y_abs_px,
                                                          font_size_pt=font_size_final_pt, font_family="Georgia",
                                                          text_anchor="middle", fill="black", line_spacing_factor=1.2)
                    else: # Single line text
                        self.svg_utils.add_text(dwg, text_content, insert_x=text_center_x, insert_y=y_abs_px,
                                                font_size_pt=font_size_final_pt, font_family="Georgia",
                                                text_anchor="middle", fill="black")
        except Exception as e:
            print(f"Error in _add_item_to_svg_page for order {order_details.get('order-id', 'unknown')}: {e}\n{traceback.format_exc()}")


    def _create_memorial_page_svg(self, orders_on_page: list, filename: str):
        output_path = os.path.join(self.output_dir, filename)
        dwg = svgwrite.Drawing(filename=output_path, size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                               viewBox=f"0 0 {self.page_width_px} {self.page_height_px}")

        for idx, order_item_details in enumerate(orders_on_page):
            if idx >= self.batch_size: break # Max 4 items for this 2x2 grid

            row_on_page = idx // self.grid_cols
            col_on_page = idx % self.grid_cols

            item_area_x = self.x_offset_px + (col_on_page * self.memorial_width_px)
            item_area_y = self.y_offset_px + (row_on_page * self.memorial_height_px)

            self._add_item_to_svg_page(dwg, item_area_x, item_area_y, order_item_details)

        # Add reference point (standard, from MemorialBase)
        self.svg_utils.add_reference_point(dwg, self.page_width_px, self.page_height_px, self.px_per_mm)
        try:
            dwg.save(pretty=True)
            print(f"Coloured Large Photo Stake SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving Coloured Large Photo Stake SVG {output_path}: {e}\n{traceback.format_exc()}")

# Register the processor
register_processor("coloured_large_photo_stakes", ColouredLargePhotoStakesProcessor)
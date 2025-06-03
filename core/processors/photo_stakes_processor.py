import os
import svgwrite
# import base64 # Will be handled by SVGUtils
import pandas as pd
from datetime import datetime

from core.processors.base import ProcessorBase
from core.processors import register_processor
from core.processors.text_utils import TextUtils
from core.processors.svg_utils import SVGUtils

class PhotoStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        self.graphics_path = graphics_path # Path to general graphics, not usually used by photo stakes
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = TextUtils()
        self.svg_utils = SVGUtils()

        self.CATEGORY = 'PHOTO'
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Constants for page layout & photo item design
        self.px_per_mm = 3.78  # Standard fallback, should be confirmed or made configurable
        self.pt_to_mm = 0.3528

        # Overall item dimensions (the "stake" or "plaque" area)
        self.memorial_width_mm = 140 # Width of the entire photo stake item area
        self.memorial_height_mm = 90 # Height of the entire photo stake item area
        self.memorial_width_px = self.memorial_width_mm * self.px_per_mm
        self.memorial_height_px = self.memorial_height_mm * self.px_per_mm

        # Page dimensions (for batching multiple items onto one SVG page)
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.page_width_px = self.page_width_mm * self.px_per_mm
        self.page_height_px = self.page_height_mm * self.px_per_mm

        # Photo specific dimensions (within the memorial item area)
        self.photo_width_mm = 50.5
        self.photo_height_mm = 68.8
        self.photo_clip_width_mm = 50.378 # Slightly different for clipping?
        self.photo_clip_height_mm = 68.901
        self.photo_border_stroke_mm = 3.65
        self.photo_outline_stroke_mm = 0.1 # Thin outline for the photo itself
        self.photo_corner_radius_mm = 6
        self.photo_left_margin_mm = 7.7 # Margin from left of memorial area to photo
        self.text_right_shift_mm = 30  # Gap between photo and text area start

        # Convert photo specific dimensions to pixels
        self.photo_width_px = self.photo_width_mm * self.px_per_mm
        self.photo_height_px = self.photo_height_mm * self.px_per_mm
        self.photo_clip_width_px = self.photo_clip_width_mm * self.px_per_mm
        self.photo_clip_height_px = self.photo_clip_height_mm * self.px_per_mm
        self.photo_border_stroke_px = self.photo_border_stroke_mm * self.px_per_mm
        self.photo_outline_stroke_px = self.photo_outline_stroke_mm * self.px_per_mm
        self.photo_corner_radius_px = self.photo_corner_radius_mm * self.px_per_mm
        self.photo_left_margin_px = self.photo_left_margin_mm * self.px_per_mm
        self.text_right_shift_px = self.text_right_shift_mm * self.px_per_mm

        # Page grid layout (Photo stakes are often 3 per page)
        self.grid_cols = 3
        self.grid_rows = 1 # Typically one row for this processor.
        self.batch_size = self.grid_cols * self.grid_rows

        # Centering offsets for the grid on the page
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows
        self.x_offset_px = (self.page_width_px - (grid_width_mm * self.px_per_mm)) / 2
        self.y_offset_px = (self.page_height_px - (grid_height_mm * self.px_per_mm)) / 2

        # Text sizes (in points)
        self.line1_size_pt = 17
        self.line2_size_pt = 25
        self.line3_size_pt = 13 # Specific to photo stakes text area

    def is_applicable(self, order_data: pd.Series) -> bool:
        # Applicable if 'decorationtype' is 'photo' and 'colour' is not 'black'.
        # Assumes 'image_path' will be present and valid for these orders.
        decoration_type = str(order_data.get('decorationtype', '')).strip().lower()
        colour = str(order_data.get('colour', '')).strip().lower()
        # Additional check for image_path might be good here or in process()
        # has_image = pd.notna(order_data.get('image_path')) and str(order_data.get('image_path')).strip() != ''

        return (decoration_type == 'photo' and colour != 'black')

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        self.output_dir = output_dir
        # self.graphics_path is set in __init__ but less relevant here as images come from 'image_path'
        os.makedirs(self.output_dir, exist_ok=True)

        if order_data.empty:
            print("No Photo Stakes orders to process.")
            return

        # Ensure 'image_path' exists and filter out rows with missing/empty image_path
        if 'image_path' not in order_data.columns:
            print("Error: 'image_path' column missing in order data for PhotoStakesProcessor.")
            return

        df_to_process = order_data[order_data['image_path'].notna() & (order_data['image_path'].astype(str).str.strip() != '')].copy()

        if df_to_process.empty:
            print("No Photo Stakes orders with valid image_path to process.")
            return

        print(f"Processing {len(df_to_process)} Photo Stakes orders.")

        batch_num = 1
        total_items = len(df_to_process)

        for start_idx in range(0, total_items, self.batch_size):
            end_idx = min(start_idx + self.batch_size, total_items)
            current_batch_df = df_to_process.iloc[start_idx:end_idx]

            if not current_batch_df.empty:
                orders_for_svg_page = current_batch_df.to_dict('records')

                if len(orders_for_svg_page) == 1: # Single item processing
                    order = orders_for_svg_page[0]
                    order_id = str(order.get('order-id', 'NO_ID')).strip()
                    sku = str(order.get('sku', 'NO_SKU')).strip()
                    # graphic_val = Path(str(order.get('image_path', 'NO_IMG'))).stem # Use image filename stem
                    filename = f"PHOTO_STAKE_{order_id}_{sku}.svg" # Simpler name for single photo
                else: # Batch page
                    filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"

                self._create_memorial_page_svg(orders_for_svg_page, filename)
                # self._create_batch_csv(...) # If CSVs per page are needed
                batch_num += 1

    def _add_photo_item_to_svg(self, dwg, x_item_offset: float, y_item_offset: float, order_details: dict):
        """Adds a single photo stake item to the SVG drawing at the given item offset."""
        try:
            # Photo frame and image placement (relative to x_item_offset, y_item_offset)
            photo_area_x = x_item_offset + self.photo_left_margin_px
            photo_area_y = y_item_offset + (self.memorial_height_px - self.photo_height_px) / 2 # Centered vertically

            clip_id = f"clip_{x_item_offset}_{y_item_offset}_{order_details.get('order-id','id')}" # Unique clip ID
            clip_path = dwg.defs.add(dwg.clipPath(id=clip_id))
            clip_path.add(dwg.rect(
                insert=(photo_area_x, photo_area_y), # Clipping rectangle at photo position
                size=(self.photo_clip_width_px, self.photo_clip_height_px),
                rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px
            ))

            # Draw photo border (acts as the visual frame)
            dwg.add(dwg.rect(
                insert=(photo_area_x, photo_area_y),
                size=(self.photo_width_px, self.photo_height_px),
                rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px,
                fill='none', stroke='black', stroke_width=self.photo_border_stroke_px
            ))

            # Embed image using SVGUtils
            image_path_str = str(order_details.get('image_path', '')).strip()
            if image_path_str and os.path.exists(image_path_str):
                embedded_image_data = self.svg_utils.embed_image(image_path_str)
                if embedded_image_data:
                    dwg.add(dwg.image(
                        href=embedded_image_data,
                        insert=(photo_area_x, photo_area_y), # Position image within its frame
                        size=(self.photo_width_px, self.photo_height_px), # Display size of image
                        clip_path=f'url(#{clip_id})'
                    ))
                else:
                    print(f"Warning: Failed to embed image {image_path_str} for order {order_details.get('order-id')}")
            else:
                print(f"Warning: Image path not found or invalid: {image_path_str} for order {order_details.get('order-id')}")

            # Text area layout (to the right of the photo)
            text_area_start_x = photo_area_x + self.photo_width_px + self.text_right_shift_px
            # text_area_width = self.memorial_width_px - (text_area_start_x - x_item_offset) - self.photo_left_margin_px # Adjust width if needed
            text_center_x = text_area_start_x + (self.memorial_width_px - (photo_area_x + self.photo_width_px + self.text_right_shift_px - x_item_offset) - self.photo_left_margin_px) / 2


            # Add text lines using TextUtils for consistency
            line_y_offsets_mm = {'line_1': 28, 'line_2': 45, 'line_3': 62}
            font_sizes_pt = {'line_1': self.line1_size_pt, 'line_2': self.line2_size_pt, 'line_3': self.line3_size_pt}

            for line_key in ['line_1', 'line_2', 'line_3']:
                text_content = str(order_details.get(line_key, '')).strip()
                if text_content:
                    y_pos_abs = y_item_offset + (line_y_offsets_mm[line_key] * self.px_per_mm)
                    # For photo stakes, text is usually single line and centered in its allocated text area.
                    # If multi-line or complex wrapping is needed for photo stake text, TextUtils should handle it.
                    self.svg_utils.add_text(dwg, text_content,
                                            insert_x=text_center_x, insert_y=y_pos_abs,
                                            font_size_mm=(font_sizes_pt[line_key] * self.pt_to_mm),
                                            font_family="Georgia", text_anchor="middle", fill="black")
        except Exception as e:
            print(f"Error in _add_photo_item_to_svg for order {order_details.get('order-id', 'unknown')}: {e}")


    def _create_memorial_page_svg(self, orders_on_page: list, filename: str):
        output_path = os.path.join(self.output_dir, filename)
        dwg = svgwrite.Drawing(filename=output_path, size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                               viewBox=f"0 0 {self.page_width_px} {self.page_height_px}")

        for idx, order_item_details in enumerate(orders_on_page):
            if idx >= self.batch_size: break # Should not exceed batch_size (e.g., 3)

            row_on_page = idx // self.grid_cols
            col_on_page = idx % self.grid_cols

            # Calculate top-left (x,y) for this specific item's area on the page
            item_area_x = self.x_offset_px + (col_on_page * self.memorial_width_px)
            item_area_y = self.y_offset_px + (row_on_page * self.memorial_height_px)

            # Optional: Draw a boundary for the entire item area (useful for debugging layout)
            # dwg.add(dwg.rect(insert=(item_area_x, item_area_y), size=(self.memorial_width_px, self.memorial_height_px),
            #                  fill='none', stroke='lightgrey', stroke_width=0.5))

            self._add_photo_item_to_svg(dwg, item_area_x, item_area_y, order_item_details)

        # Add reference point for printer alignment
        ref_size_px = 0.1 * self.px_per_mm
        dwg.add(dwg.rect(insert=(self.page_width_px - ref_size_px, self.page_height_px - ref_size_px),
                         size=(ref_size_px, ref_size_px), fill='blue'))
        try:
            dwg.save(pretty=True)
            print(f"Photo Stake SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving Photo Stake SVG {output_path}: {e}")

# Register the processor
register_processor("photo_stakes", PhotoStakesProcessor)

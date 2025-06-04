import os
import svgwrite
import pandas as pd
from .base import ProcessorBase
from . import register_processor
from .svg_utils import draw_rounded_rect, add_multiline_text # Assuming these are sufficient for svgwrite
from .text_utils import create_batch_csv # Changed to import from local text_utils
# We'll need to ensure svg_utils has embed_image and add_reference_point,
# and text_utils has split_line_to_fit and check_grammar_and_typos.

class BWLargePhotoStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path, output_dir):
        # Store paths directly, no super().__init__ needed for ProcessorBase if it doesn't have one
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.CATEGORY = 'B&W_LARGE_PHOTO_STAKES'
        from datetime import datetime
        self.date_str = datetime.now().strftime("%Y%m%d")

        # Standard page setup (A4-like, but specific pixel dimensions from original)
        self.px_per_mm = 3.7795275591  # Standard DPI for SVG (96 DPI)
        self.page_width_mm = 210
        self.page_height_mm = 297
        self.page_width_px = int(self.page_width_mm * self.px_per_mm)
        self.page_height_px = int(self.page_height_mm * self.px_per_mm)

        # Memorial dimensions for large stakes
        self.memorial_width_mm = 200
        self.memorial_height_mm = 120
        self.corner_radius_mm = 6

        # Photo dimensions and margins (in mm)
        self.photo_width_mm = 50.5
        self.photo_height_mm = 68.8
        self.photo_clip_width_mm = 50.378
        self.photo_clip_height_mm = 68.901
        # self.photo_border_stroke_mm = 3.65 # This was for the thick border, not used in B&W photo?
        self.photo_outline_stroke_mm = 0.5 # For the blue outline in original, not used here.
        self.photo_corner_radius_mm = 6
        self.photo_left_margin_mm = 7.7
        self.text_right_shift_mm = 30 # Shift text area relative to photo end

        # Convert dimensions to pixels
        self.memorial_width_px = int(self.memorial_width_mm * self.px_per_mm)
        self.memorial_height_px = int(self.memorial_height_mm * self.px_per_mm)
        self.corner_radius_px = int(self.corner_radius_mm * self.px_per_mm)

        self.photo_width_px = int(self.photo_width_mm * self.px_per_mm)
        self.photo_height_px = int(self.photo_height_mm * self.px_per_mm)
        self.photo_clip_width_px = int(self.photo_clip_width_mm * self.px_per_mm)
        self.photo_clip_height_px = int(self.photo_clip_height_mm * self.px_per_mm)
        # self.photo_border_stroke_px = int(self.photo_border_stroke_mm * self.px_per_mm)
        self.photo_corner_radius_px = int(self.photo_corner_radius_mm * self.px_per_mm)
        self.photo_left_margin_px = int(self.photo_left_margin_mm * self.px_per_mm)
        self.text_right_shift_px = int(self.text_right_shift_mm * self.px_per_mm)

        # Grid layout (1x2, meaning 2 items per page, side-by-side)
        self.grid_cols = 2
        self.grid_rows = 1
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows

        # Align to right and bottom of page
        self.x_offset_mm = self.page_width_mm - grid_width_mm
        self.y_offset_mm = self.page_height_mm - grid_height_mm
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

        # Text sizes (pt) - convert to mm for svgwrite consistency if needed, or use as is if svg_utils handles pt
        self.line1_size_pt = 17
        self.line2_size_pt = 25
        self.line3_size_pt = 12 # From original for line 3

        # Initialize utilities - assuming they are in the same directory
        from . import svg_utils # Relative import
        from . import text_utils # Relative import
        self.svg_utils = svg_utils
        self.text_utils = text_utils

    def is_applicable(self, order_data: pd.Series) -> bool:
        # Normalize column names from order_data (which might be mixed case)
        order_data_lower = order_data.rename(index=str.lower)

        colour = str(order_data_lower.get('colour', '')).strip().lower()
        type_ = str(order_data_lower.get('type', '')).strip().lower()
        decorationtype = str(order_data_lower.get('decorationtype', '')).strip().lower()

        # Check for 'photo_path' or 'image_path'
        photo_path = order_data_lower.get('photo_path', order_data_lower.get('image_path', pd.NA))

        return (colour == 'black' and
                'large stake' in type_ and
                decorationtype == 'photo' and
                pd.notna(photo_path) and str(photo_path).strip() != '')

    def _add_photo_item_to_svg(self, dwg, x_pos, y_pos, order_item):
        # order_item is a Pandas Series
        # Add memorial outline (thin black line)
        dwg.add(draw_rounded_rect(
            dwg, # svgwrite drawing object
            insert=(x_pos, y_pos),
            size=(self.memorial_width_px, self.memorial_height_px),
            rx=self.corner_radius_px,
            ry=self.corner_radius_px,
            fill='none', # B&W, so no fill
            stroke='black',
            stroke_width=1 # Thin outline
        ))

        # Photo area setup
        photo_frame_x = x_pos + self.photo_left_margin_px
        photo_frame_y = y_pos + (self.memorial_height_px - self.photo_height_px) / 2

        # Clipping rectangle for the photo
        clip_rect_x = photo_frame_x + (self.photo_width_px - self.photo_clip_width_px) / 2
        clip_rect_y = photo_frame_y + (self.photo_height_px - self.photo_clip_height_px) / 2

        clip_id = f'clip_{self.CATEGORY}_{x_pos}_{y_pos}'.replace('.', '_') # Ensure ID is valid
        clip_path_obj = dwg.defs.add(dwg.clipPath(id=clip_id))
        clip_path_obj.add(dwg.rect(
            insert=(clip_rect_x, clip_rect_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px
        ))

        # Embed the photo (B&W, so no thick border like coloured version)
        # Image path can be 'photo_path' or 'image_path'
        image_path_val = order_item.get('photo_path', order_item.get('image_path', None))

        if pd.notna(image_path_val) and str(image_path_val).strip():
            full_image_path = os.path.join(self.graphics_path, str(image_path_val).replace('\\', os.sep).lstrip('/\\'))
            if not os.path.isabs(str(image_path_val)): # If original path was relative
                 full_image_path = os.path.join(self.graphics_path, str(image_path_val).replace('\\', os.sep).lstrip('/\\'))
            else: # If original path was absolute
                 full_image_path = str(image_path_val)

            # Use svg_utils.embed_image, assuming it handles B&W conversion or expects pre-converted
            # For B&W, the image itself should ideally be B&W.
            # The original processor didn't explicitly convert to B&W here.
            self.svg_utils.embed_image(
                dwg,
                full_image_path,
                insert=(photo_frame_x, photo_frame_y), # Position the image within the frame
                size=(self.photo_width_px, self.photo_height_px), # Display size of image
                clip_path_id=clip_id
            )
        else:
            # Placeholder if no image
            dwg.add(dwg.rect(
                insert=(photo_frame_x, photo_frame_y),
                size=(self.photo_width_px, self.photo_height_px),
                fill='#cccccc', # Light grey placeholder
                stroke='black',
                stroke_width=0.5
            ))
            dwg.add(dwg.text("No Image", insert=(photo_frame_x + 10, photo_frame_y + 20), fill='black'))


        # Text area setup
        text_area_start_x = photo_frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_px - (text_area_start_x - x_pos) - self.photo_left_margin_px # some right margin
        text_center_x = text_area_start_x + text_area_width / 2

        # Add text lines using text_utils and svg_utils
        # Ensure font sizes are handled correctly by svg_utils (e.g., converted to mm or px)
        pt_to_mm = 0.352778 # Conversion factor

        if pd.notna(order_item.get('line_1')):
            self.text_utils.check_grammar_and_typos(str(order_item['line_1']))
            lines = self.text_utils.split_line_to_fit(str(order_item['line_1']), 30) # Max chars for line 1
            # Assuming add_multiline_text handles font size in pt or mm as per its design
            # The original used "Georgia" font.
            self.svg_utils.add_multiline_text(dwg, lines,
                                              insert=(text_center_x, y_pos + (28 * self.px_per_mm)),
                                              font_size=f"{self.line1_size_pt * pt_to_mm}mm", # Example: convert pt to mm
                                              font_family="Georgia", anchor="middle", fill="black")

        if pd.notna(order_item.get('line_2')):
            self.text_utils.check_grammar_and_typos(str(order_item['line_2']))
            lines = self.text_utils.split_line_to_fit(str(order_item['line_2']), 25) # Max chars for line 2
            self.svg_utils.add_multiline_text(dwg, lines,
                                              insert=(text_center_x, y_pos + (45 * self.px_per_mm)),
                                              font_size=f"{self.line2_size_pt * pt_to_mm}mm",
                                              font_family="Georgia", anchor="middle", fill="black")

        if pd.notna(order_item.get('line_3')):
            self.text_utils.check_grammar_and_typos(str(order_item['line_3']))
            lines = self.text_utils.split_line_to_fit(str(order_item['line_3']), 35) # Max chars for line 3
            self.svg_utils.add_multiline_text(dwg, lines,
                                              insert=(text_center_x, y_pos + (57 * self.px_per_mm)), # Adjusted y from original
                                              font_size=f"{self.line3_size_pt * pt_to_mm}mm",
                                              font_family="Georgia", anchor="middle", fill="black")

    def _create_memorial_page_svg(self, batch_orders_df: pd.DataFrame, batch_num: int):
        # batch_orders_df contains rows for this page
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.output_dir, filename)

        dwg = svgwrite.Drawing(
            filepath,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )

        # Process up to 2 memorials in a 1x2 grid (side-by-side)
        for idx, (_, order_row) in enumerate(batch_orders_df.iterrows()):
            if idx >= self.grid_cols * self.grid_rows: # Max 2 items
                break

            # Calculate position for each item in the grid
            # Grid is 1 row, 2 columns, aligned to page bottom-right
            # Items are populated right-to-left, bottom-to-top (though only 1 row here)
            col_idx = (self.grid_cols - 1) - (idx % self.grid_cols) # For right-to-left
            row_idx = (self.grid_rows - 1) - (idx // self.grid_cols) # For bottom-to-top

            item_x = self.x_offset_px + col_idx * self.memorial_width_px
            item_y = self.y_offset_px + row_idx * self.memorial_height_px

            self._add_photo_item_to_svg(dwg, item_x, item_y, order_row)

        # Add reference point if the utility exists
        if hasattr(self.svg_utils, 'add_reference_point'):
            self.svg_utils.add_reference_point(dwg)

        dwg.save()
        print(f"Generated SVG: {filepath}")

        # Create batch CSV if the utility exists
        # This call was originally here, but it's better to call it from the process method
        # if hasattr(self, '_create_batch_csv'): # Check if method exists
        #      self._create_batch_csv(batch_orders_df.to_dict('records'), batch_num, self.CATEGORY)


    # Removed local _create_batch_csv method, will use utility from core.utils

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str):
        # Ensure paths are updated if different from __init__ (they should be the same)
        self.output_dir = output_dir
        self.graphics_path = graphics_path
        os.makedirs(self.output_dir, exist_ok=True)

        # Filter for applicable orders (although GUI should pre-filter, double check)
        applicable_df = order_data[order_data.apply(self.is_applicable, axis=1)].copy()

        if applicable_df.empty:
            print(f"No applicable orders found for {self.CATEGORY} processor.")
            return

        # Normalize column names to lowercase for processing consistency
        applicable_df.columns = [col.lower() for col in applicable_df.columns]

        # Ensure 'photo_path' is preferred, fallback to 'image_path'
        if 'photo_path' not in applicable_df.columns and 'image_path' in applicable_df.columns:
            applicable_df['photo_path'] = applicable_df['image_path']
        elif 'photo_path' in applicable_df.columns and 'image_path' in applicable_df.columns:
            applicable_df['photo_path'] = applicable_df['photo_path'].fillna(applicable_df['image_path'])
        elif 'photo_path' not in applicable_df.columns and 'image_path' not in applicable_df.columns:
            # If neither exists, create an empty photo_path column to avoid errors
            applicable_df['photo_path'] = pd.NA


        items_per_page = self.grid_cols * self.grid_rows # Should be 2 for this processor

        batch_num = 1
        for i in range(0, len(applicable_df), items_per_page):
            batch_df = applicable_df.iloc[i:i + items_per_page]
            if not batch_df.empty:
                self._create_memorial_page_svg(batch_df, batch_num)
                create_batch_csv(batch_df.to_dict('records'), batch_num, self.CATEGORY, self.output_dir, self.date_str)
                batch_num += 1

        print(f"{self.CATEGORY} processing complete. {len(applicable_df)} orders processed into {batch_num-1} file(s).")

# Register the processor
register_processor("bw_large_photo_stakes", BWLargePhotoStakesProcessor)

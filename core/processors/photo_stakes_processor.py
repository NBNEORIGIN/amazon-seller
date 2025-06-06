import os
import svgwrite
# import base64 # Will be handled by SVGUtils
import pandas as pd
from datetime import datetime

from core.processors.base import ProcessorBase
from core.processors import register_processor
from . import text_utils # Changed to module import
from . import svg_utils   # Changed to module import

class PhotoStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        # Standard setup for base class and utilities
        # super().__init__(graphics_path, output_dir) # Call super if ProcessorBase has __init__
        # If ProcessorBase.__init__ handles these, remove direct assignment below
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True) # Ensure output dir exists

        from . import text_utils # Assuming these are in the same directory
        from . import svg_utils
        self.text_utils = text_utils
        self.svg_utils = svg_utils

        from datetime import datetime
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S") # Timestamp for filenames

        self.CATEGORY = 'PHOTO_STAKES' # Specific category name

        # --- Page and Grid Layout (to match regular_stakes for red bounding boxes) ---
        # Conversion factors (using values from user's sample for consistency within this processor)
        self.px_per_mm = 3.78
        self.pt_to_mm = 0.3528

        # Dimensions of one item slot (the "red box")
        self.item_slot_width_mm = 140
        self.item_slot_height_mm = 90
        self.item_slot_width_px = self.item_slot_width_mm * self.px_per_mm
        self.item_slot_height_px = self.item_slot_height_mm * self.px_per_mm

        # Overall Page dimensions (A4-like, from regular_stakes)
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.page_width_px = int(self.page_width_mm * self.px_per_mm)
        self.page_height_px = int(self.page_height_mm * self.px_per_mm)

        # Grid layout (3x3 items per page)
        self.grid_cols = 3
        self.grid_rows = 3
        self.batch_size = self.grid_cols * self.grid_rows

        # Centering offsets for the entire 3x3 grid on the page
        grid_total_width_mm = self.item_slot_width_mm * self.grid_cols
        grid_total_height_mm = self.item_slot_height_mm * self.grid_rows
        self.x_offset_page_px = int(((self.page_width_mm - grid_total_width_mm) / 2) * self.px_per_mm)
        self.y_offset_page_px = int(((self.page_height_mm - grid_total_height_mm) / 2) * self.px_per_mm)

        # Properties for the "red bounding box" of each item slot
        self.item_slot_corner_radius_px = 6 * self.px_per_mm # from regular_stakes
        self.item_slot_stroke_width_px = 0.1 * self.px_per_mm # from regular_stakes

        # --- Dimensions for the Photo Element within an item slot (from user's sample) ---
        # This refers to the visible photo area, its black mask, and its clipping path.
        self.photo_visible_width_mm = 50.5
        self.photo_visible_height_mm = 68.8
        self.photo_visible_width_px = int(self.photo_visible_width_mm * self.px_per_mm)
        self.photo_visible_height_px = int(self.photo_visible_height_mm * self.px_per_mm)

        # Corner radius for the photo's border, mask, and clip path
        self.photo_corner_radius_mm = 6
        self.photo_corner_radius_px = int(self.photo_corner_radius_mm * self.px_per_mm)

        # Black border around the photo
        self.photo_black_border_stroke_mm = 3.65
        self.photo_black_border_stroke_px = self.photo_black_border_stroke_mm * self.px_per_mm

        # Placement of the photo element (including its border) within the item slot
        # The photo element is centered vertically.
        # Its left edge has a margin from the left of the item slot.
        self.photo_element_left_margin_mm = 7.7
        self.photo_element_left_margin_px = int(self.photo_element_left_margin_mm * self.px_per_mm)

        # The total width of the photo element including its thick border:
        # Visible photo + half border on left + half border on right
        # However, svg stroke is usually centered on the path. So if photo_visible_width_px is the path,
        # the border extends outwards and inwards by photo_black_border_stroke_px / 2.
        # Let's define the path for the border rectangle:
        self.photo_border_rect_width_px = self.photo_visible_width_px
        self.photo_border_rect_height_px = self.photo_visible_height_px

        # Text positioning (relative to the photo element)
        # The sample's `text_right_shift_mm = 30` seemed to be from photo start to text area center.
        # Let's define a clear space between the right edge of the photo's black border and start of text area.
        self.space_photo_to_text_mm = 10
        self.space_photo_to_text_px = int(self.space_photo_to_text_mm * self.px_per_mm)

        # Font sizes (from user's sample script for photo stakes)
        self.line1_font_size_pt = 17
        self.line2_font_size_pt = 25
        self.line3_font_size_pt = 13

    def is_applicable(self, order_data: pd.Series) -> bool:
        order_data_lower = order_data.rename(index=str.lower) # Ensure case-insensitivity for column names

        type_ = str(order_data_lower.get('type', '')).strip().lower()
        colour = str(order_data_lower.get('colour', '')).strip().lower()
        graphic = str(order_data_lower.get('graphic', '')).strip().lower() # From sample's process_orders
        decorationtype = str(order_data_lower.get('decorationtype', '')).strip().lower()
        image_path = str(order_data_lower.get('image_path', '')).strip() # Check for image_path

        # Criteria from the sample script's process_orders filter:
        allowed_types = ['regular stake'] # Sample used 'regular stake'
        allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble'] # Sample had 'gold' twice, corrected here

        type_is_valid = type_ in allowed_types
        colour_is_valid = colour in allowed_colours

        # Photo condition: either 'graphic' field is 'photo' OR 'decorationtype' is 'photo'
        is_photo_product = (graphic == 'photo' or decorationtype == 'photo')

        has_valid_image_path = bool(image_path) # True if not empty string

        return type_is_valid and colour_is_valid and is_photo_product and has_valid_image_path

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str):
        self.output_dir = output_dir
        self.graphics_path = graphics_path # Ensure instance variables are current
        os.makedirs(self.output_dir, exist_ok=True)

        # order_data is already pre-filtered by is_applicable by the main GUI loop.
        if order_data.empty:
            print(f"[{self.CATEGORY}] No orders passed initial is_applicable check.")
            return

        df = order_data.copy()
        df.columns = [col.lower().strip() for col in df.columns] # Normalize columns

        # 1. Expand rows by 'number-of-items'
        expanded_rows = []
        for _, row_series in df.iterrows(): # Iterate over Series
            try:
                qty = int(row_series.get('number-of-items', 1))
                qty = max(qty, 1)
            except (ValueError, TypeError):
                qty = 1
            for _ in range(qty):
                expanded_rows.append(row_series.copy())

        if not expanded_rows:
            print(f"[{self.CATEGORY}] No orders after quantity expansion.")
            return

        # Convert list of Series back to DataFrame
        processed_orders_df = pd.DataFrame(expanded_rows)

        # Reset index for iloc to work consistently in batching
        processed_orders_df.reset_index(drop=True, inplace=True)

        # (Optional: Add any specific sorting for photo stakes here if needed)
        # For now, no specific sorting beyond initial filtering is applied.

        # Batching logic
        # self.batch_size is set in __init__ (e.g., 9 for 3x3 grid)
        batch_num = 1
        total_items = len(processed_orders_df)

        print(f"[{self.CATEGORY}] Processing {total_items} photo stake items in batches of {self.batch_size}.")

        for i in range(0, total_items, self.batch_size):
            batch_df = processed_orders_df.iloc[i:i + self.batch_size]
            if not batch_df.empty:
                orders_dict_list = batch_df.to_dict('records')

                # Define filename for the SVG page (batch)
                # Using self.date_str (YYYYMMDD_HHMMSS) and self.CATEGORY from __init__
                page_filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"

                self._create_memorial_page_svg(orders_dict_list, page_filename) # Removed batch_num from here as filename is now full

                self.text_utils.create_batch_csv(
                    orders_dict_list,
                    batch_num,
                    self.CATEGORY,
                    self.output_dir,
                    self.date_str # Pass the consistent date_str from __init__
                )
                batch_num += 1

        print(f"[{self.CATEGORY}] processing complete. {total_items} items processed into {batch_num - 1} SVG/CSV file(s).")

    def _add_photo_item_to_svg_slot(self, dwg, order_item_data: pd.Series, slot_x_px: float, slot_y_px: float):
        """
        Draws a single photo stake item within the given slot coordinates.
        (slot_x_px, slot_y_px) is the top-left of the red bounding box for this item.
        """
        try:
            # --- Photo Element Positioning ---
            # Photo element (mask, photo, border) is positioned with a left margin within the slot,
            # and centered vertically within the slot.

            # Top-left X for the photo's black border rectangle
            photo_border_rect_x = slot_x_px + self.photo_element_left_margin_px
            # Top-left Y for the photo's black border rectangle (vertically centered)
            photo_border_rect_y = slot_y_px + (self.item_slot_height_px - self.photo_border_rect_height_px) / 2

            # --- 1. Black Mask (Background for Photo) ---
            # This is drawn first, same size and shape as the photo's visible area.
            # The sample script used photo_clip_width/height for the mask.
            # Let's use photo_visible_width/height_px as defined in __init__.
            dwg.add(dwg.rect(
                insert=(photo_border_rect_x, photo_border_rect_y), # Mask position matches photo visible area
                size=(self.photo_visible_width_px, self.photo_visible_height_px),
                rx=self.photo_corner_radius_px,
                ry=self.photo_corner_radius_px,
                fill='black',
                stroke='none' # No stroke for the mask itself
            ))

            # --- 2. Clipping Path for Photo ---
            # Clip path dimensions should match the photo's visible area *inside* the border.
            # If photo_black_border_stroke_px is centered on the edge of photo_border_rect_width/height_px,
            # then the visible area for the photo content is effectively the same.
            # The sample script used photo_clip_width/height for both mask and clip rect,
            # and photo_width/height for the image itself and its border.
            # Let's assume self.photo_visible_width/height_px is the area the image should fill.

            clip_id = f"photo_clip_{order_item_data.get('order-item-id', 'item')}_{slot_x_px}_{slot_y_px}".replace('.', '_')
            clip_path = dwg.defs.add(dwg.clipPath(id=clip_id))
            clip_path.add(dwg.rect(
                insert=(photo_border_rect_x, photo_border_rect_y),
                size=(self.photo_visible_width_px, self.photo_visible_height_px),
                rx=self.photo_corner_radius_px,
                ry=self.photo_corner_radius_px
            ))

            # --- 3. Photo Image ---
            image_file_name = str(order_item_data.get('image_path', '')).strip()
            if image_file_name:
                # Construct full path, assuming image_path is relative to graphics_path (e.g., "images/myphoto.jpg")
                # If image_file_name is already an absolute path from a previous step, os.path.join handles it.
                # The order_pipeline usually puts just the filename in 'image_path'.
                # The GUI then prepends "images/" before it hits the old processor system.
                # For now, assume image_file_name is just the filename.jpg and it's in an "images" subfolder of graphics_path
                # However, user's sample script takes `image_path` directly. Let's use that.
                # It implies `image_path` column should contain `images/xxxxx.jpg`.

                # If image_file_name from DataFrame is "images/xxxx.jpg", then
                # graphics_path is "C:/.../assets/graphics"
                # full_image_path becomes "C:/.../assets/graphics/images/xxxx.jpg"
                # This seems correct if SKULIST/pipeline stores it as "images/xxxx.jpg" in image_path column.
                # If image_path is just "xxxx.jpg", then we might need an "images" subfolder.
                # The sample script did: `norm_path = os.path.normpath(photo_path.strip())`
                # and `os.path.exists(norm_path)`. This implies `photo_path` was absolute or relative to CWD.
                # The GUI `process_orders` sets `images_dir = os.path.join(app_dir, "images")`
                # and `order_pipeline.process_amazon_orders` uses this.
                # The output df from order_pipeline has 'image_path' as the *full path* to the downloaded image in the local "images" folder.

                full_image_path = image_file_name # Assuming image_path column contains the full, absolute path.

                if os.path.exists(full_image_path):
                    self.svg_utils.embed_image(
                        dwg,
                        image_path=full_image_path,
                        insert=(photo_border_rect_x, photo_border_rect_y),
                        size=(self.photo_visible_width_px, self.photo_visible_height_px),
                        clip_path_id=clip_id
                        # defs=dwg.defs # if pixelated style is desired via svg_utils
                    )
                else:
                    print(f"Warning: Photo image file not found: {full_image_path} for order {order_item_data.get('order-id')}")
                    # Optionally draw a placeholder for missing image
                    dwg.add(dwg.rect(insert=(photo_border_rect_x, photo_border_rect_y), size=(self.photo_visible_width_px, self.photo_visible_height_px), fill='grey', stroke='red', rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px))
                    dwg.add(dwg.text("Img Missing", insert=(photo_border_rect_x + self.photo_visible_width_px/2, photo_border_rect_y + self.photo_visible_height_px/2), text_anchor="middle", fill="white", font_size="10px"))
            else:
                print(f"Warning: No image_path provided for order {order_item_data.get('order-id')}")
                dwg.add(dwg.rect(insert=(photo_border_rect_x, photo_border_rect_y), size=(self.photo_visible_width_px, self.photo_visible_height_px), fill='#e0e0e0', stroke='black', rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px))
                dwg.add(dwg.text("No Path", insert=(photo_border_rect_x + self.photo_visible_width_px/2, photo_border_rect_y + self.photo_visible_height_px/2), text_anchor="middle", fill="black", font_size="10px"))


            # --- 4. Black Border ---
            # This is drawn on top of the photo (or where the photo would be).
            # Its path aligns with the photo's visible area.
            dwg.add(dwg.rect(
                insert=(photo_border_rect_x, photo_border_rect_y),
                size=(self.photo_border_rect_width_px, self.photo_border_rect_height_px), # Uses visible width/height for path
                rx=self.photo_corner_radius_px,
                ry=self.photo_corner_radius_px,
                fill='none',
                stroke='black',
                stroke_width=self.photo_black_border_stroke_px
            ))

            # --- 5. Text Placement ---
            # Text area starts to the right of the photo element (including its border).
            # The sample used `text_right_shift_mm` from the *start* of the photo area.
            # Let's calculate text area relative to the right edge of the photo's black border.
            # Right edge of photo border: photo_border_rect_x + self.photo_border_rect_width_px

            text_area_start_x = photo_border_rect_x + self.photo_border_rect_width_px + self.space_photo_to_text_px

            # Calculate width of text area: from text_area_start_x to right edge of slot, minus a margin.
            slot_right_edge_x = slot_x_px + self.item_slot_width_px
            text_area_right_margin_px = self.photo_element_left_margin_px # Use same margin as photo on left
            text_area_width_px = slot_right_edge_x - text_area_start_x - text_area_right_margin_px

            # Center of the text area for text-anchor="middle"
            text_area_center_x = text_area_start_x + (text_area_width_px / 2)

            # Max characters per line for text wrapping (estimate)
            # Use a smaller font (e.g., line3 font size) for a rough estimate of char width
            font_size_for_wrap_mm = self.line3_font_size_pt * self.pt_to_mm
            char_width_approx_mm = 0.5 * font_size_for_wrap_mm # Rough heuristic
            max_chars = int((text_area_width_px / self.px_per_mm) / char_width_approx_mm)
            if max_chars <= 0: max_chars = 10 # Ensure it's a positive number

            # Text line Y positions (example, relative to slot_y_px, needs adjustment based on font sizes and desired layout)
            # The sample script had specific Y offsets.
            # Let's use relative positioning within the text area or slot height.
            # For vertical centering of text block: (self.item_slot_height_px - total_text_height) / 2
            # For now, using fixed y offsets from sample, adjusted for slot_y_px
            line_y_offsets_mm = {
                'line_1': 28, # mm from top of item slot (from sample)
                'line_2': 45, # mm
                'line_3': 62  # mm
            }
            font_sizes_pt = {
                'line_1': self.line1_font_size_pt,
                'line_2': self.line2_font_size_pt,
                'line_3': self.line3_font_size_pt
            }

            for line_key in ['line_1', 'line_2', 'line_3']:
                text_content = str(order_item_data.get(line_key, '')).strip()
                if text_content:
                    # text_content = self.text_utils.check_grammar_and_typos(text_content) # Optional
                    wrapped_lines = self.text_utils.split_line_to_fit_multiline(text_content, max_chars_per_line=max_chars, max_lines=3) # Max 3 lines for any field here

                    if wrapped_lines:
                        current_font_size_pt = font_sizes_pt[line_key]
                        font_size_for_svg = f"{current_font_size_pt * self.pt_to_mm:.2f}mm"
                        # Note: svg_utils.add_multiline_text expects font_size string with units.
                        # If it was changed to take font_size_mm as float, this would be:
                        # font_size_mm_val = current_font_size_pt * self.pt_to_mm

                        # Calculate Y position for this text block
                        # The y_offset_mm is from the top of the item slot
                        abs_y_pos = slot_y_px + (line_y_offsets_mm[line_key] * self.px_per_mm)

                        self.svg_utils.add_multiline_text(
                            dwg,
                            lines=wrapped_lines,
                            insert=(text_area_center_x, abs_y_pos),
                            font_size=font_size_for_svg, # Pass as string with units
                            font_family="Georgia", # From sample
                            anchor="middle",
                            fill="black" # From sample
                        )
        except Exception as e:
            print(f"Error in _add_photo_item_to_svg_slot for order {order_item_data.get('order-id', 'N/A')}: {e}")
            import traceback
            traceback.print_exc()

    def _create_memorial_page_svg(self, orders_on_page: list, filename: str):
        output_path = os.path.join(self.output_dir, filename)
        dwg = svgwrite.Drawing(filename=output_path, size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                               viewBox=f"0 0 {self.page_width_px} {self.page_height_px}")

        for idx, order_item_details_dict in enumerate(orders_on_page):
            if idx >= self.batch_size: break # Should not exceed batch_size (e.g., 3)

            row_on_page = idx // self.grid_cols
            col_on_page = idx % self.grid_cols

            # Calculate top-left (x,y) for this specific item's area on the page
            # These are coordinates for the "red box" (item slot)
            item_slot_x = self.x_offset_page_px + (col_on_page * self.item_slot_width_px)
            item_slot_y = self.y_offset_page_px + (row_on_page * self.item_slot_height_px)

            # Draw the red bounding box for the slot (from regular_stakes)
            dwg.add(dwg.rect(insert=(item_slot_x, item_slot_y),
                             size=(self.item_slot_width_px, self.item_slot_height_px),
                             rx=self.item_slot_corner_radius_px, ry=self.item_slot_corner_radius_px,
                             fill='none', stroke='red', stroke_width=self.item_slot_stroke_width_px))

            # Convert dict to pd.Series for _add_photo_item_to_svg_slot if it expects Series
            # However, the new _add_photo_item_to_svg_slot uses .get() so dict is fine.
            self._add_photo_item_to_svg_slot(dwg, order_item_details_dict, item_slot_x, item_slot_y)

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

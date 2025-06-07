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
        # super().__init__(graphics_path, output_dir) # If ProcessorBase has __init__
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        from . import text_utils
        from . import svg_utils
        self.text_utils = text_utils
        self.svg_utils = svg_utils

        from datetime import datetime
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.CATEGORY = 'large_photo_stakes' # New category name

        # --- Page and Grid Layout ---
        # Conversion factors (can be consistent or specific per processor if needed)
        self.px_per_mm = 3.78 # Using a common one, adjust if precision demands regular_stakes' value
        self.pt_to_mm = 0.3528

        # Item Slot Dimensions (Larger: 200mm x 120mm, 6mm radius corners)
        self.item_slot_width_mm = 200
        self.item_slot_height_mm = 120
        self.item_slot_width_px = self.item_slot_width_mm * self.px_per_mm
        self.item_slot_height_px = self.item_slot_height_mm * self.px_per_mm
        self.item_slot_corner_radius_mm = 6
        self.item_slot_corner_radius_px = self.item_slot_corner_radius_mm * self.px_per_mm

        # Page dimensions (same as other processors, e.g., 439.8mm x 289.9mm)
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.page_width_px = int(self.page_width_mm * self.px_per_mm)
        self.page_height_px = int(self.page_height_mm * self.px_per_mm)

        # Grid layout (2x2 items per page)
        self.grid_cols = 2
        self.grid_rows = 2
        self.batch_size = self.grid_cols * self.grid_rows # 4 items

        # Centering offsets for the 2x2 grid on the page
        grid_total_width_mm = self.item_slot_width_mm * self.grid_cols
        grid_total_height_mm = self.item_slot_height_mm * self.grid_rows
        self.x_offset_page_px = int(((self.page_width_mm - grid_total_width_mm) / 2) * self.px_per_mm)
        self.y_offset_page_px = int(((self.page_height_mm - grid_total_height_mm) / 2) * self.px_per_mm)

        # Stroke for the "red bounding box" (can be thin, as it's a guide)
        self.item_slot_stroke_width_px = 0.1 * self.px_per_mm

        # --- Internal Photo Element Dimensions (Scaled for 200x120mm item) ---
        # Original photo_stakes item slot was ~140x90mm. New is 200x120mm.
        # Width scale: 200/140 = ~1.428
        # Height scale: 120/90 = ~1.333
        # Use an average scale or prioritize width for photo aspect ratio. Let's use width scale for now.
        # Or, better, define a desired photo width as a portion of the new item_slot_width.
        # E.g., photo area takes ~36% of the 140mm width in photo_stakes (50.5mm / 140mm).
        # New photo width = 0.36 * 200mm = 72mm.

        self.photo_visible_width_mm = 72 # Approx 0.36 * 200mm
        # Maintain aspect ratio of original photo (50.5 w / 68.8 h = ~0.734)
        self.photo_visible_height_mm = self.photo_visible_width_mm / (50.5 / 68.8)
        self.photo_visible_width_px = int(self.photo_visible_width_mm * self.px_per_mm)
        self.photo_visible_height_px = int(self.photo_visible_height_mm * self.px_per_mm)

        # Corner radius for the photo's border, mask, and clip path (scaled or new value)
        # Original was 6mm for a 50mm wide photo. Scale it: 6mm * (72/50.5) = ~8.5mm
        self.photo_corner_radius_mm = 8.5
        self.photo_corner_radius_px = int(self.photo_corner_radius_mm * self.px_per_mm)

        # Black border around the photo (scaled)
        # Original was 3.65mm. Scale it: 3.65mm * (72/50.5) = ~5.2mm
        self.photo_black_border_stroke_mm = 5.2
        self.photo_black_border_stroke_px = self.photo_black_border_stroke_mm * self.px_per_mm

        self.photo_border_rect_width_px = self.photo_visible_width_px # Path for border aligns with visible photo
        self.photo_border_rect_height_px = self.photo_visible_height_px

        # Placement of the photo element (left margin, scaled)
        # Original was 7.7mm for 140mm item. (7.7 / 140 = ~5.5% margin)
        # New margin = 0.055 * 200mm = 11mm
        self.photo_element_left_margin_mm = 11
        self.photo_element_left_margin_px = int(self.photo_element_left_margin_mm * self.px_per_mm)

        # Space between photo and text area (scaled)
        # Original was 10mm for 140mm item. Let's scale by width: 10 * (200/140) = ~14mm
        self.space_photo_to_text_mm = 14
        self.space_photo_to_text_px = int(self.space_photo_to_text_mm * self.px_per_mm)

        # Font sizes (scaled up from photo_stakes_processor)
        # Original: L1=17pt, L2=25pt, L3=13pt.
        # General scaling factor (e.g., average of width/height scales, ~1.38, or just a chosen factor like 1.3)
        scale_factor_font = 1.3
        self.line1_font_size_pt = int(17 * scale_factor_font)
        self.line2_font_size_pt = int(25 * scale_factor_font)
        self.line3_font_size_pt = int(13 * scale_factor_font)

    def is_applicable(self, order_data: pd.Series) -> bool:
        order_data_lower = order_data.rename(index=str.lower) # Ensure case-insensitivity for column names

        type_ = str(order_data_lower.get('type', '')).strip().lower()
        colour = str(order_data_lower.get('colour', '')).strip().lower()
        graphic = str(order_data_lower.get('graphic', '')).strip().lower() # From sample's process_orders
        decorationtype = str(order_data_lower.get('decorationtype', '')).strip().lower()
        image_path = str(order_data_lower.get('image_path', '')).strip() # Check for image_path

        # Specific for Coloured Large Photo Stakes
        is_correct_type = type_ in ['large stake', 'large plaque']

        allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble'] # Coloured, non-black/slate
        is_correct_colour = colour in allowed_colours

        # Photo condition: either 'graphic' field is 'photo' OR 'decorationtype' is 'photo'
        is_photo_product = (graphic == 'photo' or decorationtype == 'photo')

        has_valid_image_path = bool(image_path) # True if not empty string

        return is_correct_type and is_correct_colour and is_photo_product and has_valid_image_path

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

        processed_orders_df = pd.DataFrame(expanded_rows)
        processed_orders_df.reset_index(drop=True, inplace=True)

        # self.batch_size is 4, set in __init__ for the 2x2 grid
        batch_num = 1
        total_items = len(processed_orders_df)

        print(f"[{self.CATEGORY}] Processing {total_items} items in batches of {self.batch_size}.")

        for i in range(0, total_items, self.batch_size):
            batch_df = processed_orders_df.iloc[i:i + self.batch_size]
            if not batch_df.empty:
                orders_dict_list = batch_df.to_dict('records')
                page_filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"

                self._create_memorial_page_svg(orders_dict_list, page_filename)

                self.text_utils.create_batch_csv(
                    orders_dict_list, batch_num, self.CATEGORY,
                    self.output_dir, self.date_str
                )
                batch_num += 1

        print(f"[{self.CATEGORY}] processing complete. {total_items} items processed into {batch_num - 1} file(s).")

    def _add_large_photo_item_to_svg_slot(self, dwg, order_item_data: pd.Series, slot_x_px: float, slot_y_px: float):
        """
        Draws a single coloured large photo stake item within the given slot coordinates.
        (slot_x_px, slot_y_px) is the top-left of the red bounding box (200x120mm) for this item.
        This method is similar to _add_photo_item_to_svg_slot in photo_stakes_processor,
        but uses the dimensions defined in this class's __init__ for larger items.
        """
        try:
            # --- Photo Element Positioning (within the 200x120mm slot) ---
            # Photo element (mask, photo, border) is positioned with a left margin,
            # and centered vertically within the slot.

            # Top-left X for the photo's black border rectangle
            # self.photo_element_left_margin_px was defined in __init__
            photo_border_rect_x = slot_x_px + self.photo_element_left_margin_px

            # Top-left Y for the photo's black border rectangle (vertically centered within item slot)
            # self.photo_border_rect_height_px was defined in __init__ (scaled from photo_visible_height_px)
            photo_border_rect_y = slot_y_px + (self.item_slot_height_px - self.photo_border_rect_height_px) / 2

            # --- 1. Black Mask (Background for Photo) ---
            # Uses self.photo_visible_width_px, self.photo_visible_height_px from __init__
            dwg.add(dwg.rect(
                insert=(photo_border_rect_x, photo_border_rect_y), # Mask position matches photo visible area
                size=(self.photo_visible_width_px, self.photo_visible_height_px),
                rx=self.photo_corner_radius_px, # Scaled in __init__
                ry=self.photo_corner_radius_px,
                fill='black',
                stroke='none' # No stroke for the mask itself
            ))

            # --- 2. Clipping Path for Photo ---
            clip_id = f"large_photo_clip_{order_item_data.get('order-item-id', 'item')}_{slot_x_px}_{slot_y_px}".replace('.', '_')
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
                full_image_path = image_file_name # Assuming image_path column contains a usable path

                if os.path.exists(full_image_path):
                    self.svg_utils.embed_image(
                        dwg,
                        image_path=full_image_path,
                        insert=(photo_border_rect_x, photo_border_rect_y),
                        size=(self.photo_visible_width_px, self.photo_visible_height_px),
                        clip_path_id=clip_id
                    )
                else:
                    print(f"Warning: Photo image file not found: {full_image_path} for order {order_item_data.get('order-id')}")
                    dwg.add(dwg.rect(insert=(photo_border_rect_x, photo_border_rect_y), size=(self.photo_visible_width_px, self.photo_visible_height_px), fill='grey', stroke='red', rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px))
                    dwg.add(dwg.text("Img Missing", insert=(photo_border_rect_x + self.photo_visible_width_px/2, photo_border_rect_y + self.photo_visible_height_px/2), text_anchor="middle", fill="white", font_size="12px")) # Slightly larger font for larger stake
            else:
                print(f"Warning: No image_path provided for order {order_item_data.get('order-id')}")
                dwg.add(dwg.rect(insert=(photo_border_rect_x, photo_border_rect_y), size=(self.photo_visible_width_px, self.photo_visible_height_px), fill='#e0e0e0', stroke='black', rx=self.photo_corner_radius_px, ry=self.photo_corner_radius_px))
                dwg.add(dwg.text("No Path", insert=(photo_border_rect_x + self.photo_visible_width_px/2, photo_border_rect_y + self.photo_visible_height_px/2), text_anchor="middle", fill="black", font_size="12px"))


            # --- 4. Black Border ---
            # Uses self.photo_border_rect_width/height_px and self.photo_black_border_stroke_px from __init__
            dwg.add(dwg.rect(
                insert=(photo_border_rect_x, photo_border_rect_y),
                size=(self.photo_border_rect_width_px, self.photo_border_rect_height_px),
                rx=self.photo_corner_radius_px,
                ry=self.photo_corner_radius_px,
                fill='none',
                stroke='black',
                stroke_width=self.photo_black_border_stroke_px
            ))

            # --- 5. Text Placement ---
            # Text area starts to the right of the photo element's border.
            # self.space_photo_to_text_px was defined in __init__
            text_area_start_x = photo_border_rect_x + self.photo_border_rect_width_px + self.space_photo_to_text_px

            slot_right_edge_x = slot_x_px + self.item_slot_width_px
            # Use a scaled version of the photo's left margin for the text area's right margin
            text_area_right_margin_px = self.photo_element_left_margin_px
            text_area_width_px = slot_right_edge_x - text_area_start_x - text_area_right_margin_px

            text_area_center_x = text_area_start_x + (text_area_width_px / 2)

            # Max characters per line for text wrapping (estimate, scaled)
            # Using line3 font size (smallest) for char width estimation. Scaled font sizes in __init__.
            font_size_for_wrap_mm = self.line3_font_size_pt * self.pt_to_mm
            char_width_approx_mm = 0.5 * font_size_for_wrap_mm
            max_chars = int((text_area_width_px / self.px_per_mm) / char_width_approx_mm) if char_width_approx_mm > 0 else 15
            if max_chars <= 0: max_chars = 15

            # Text line Y positions (relative to slot_y_px).
            # These need to be appropriate for the 120mm item height and scaled fonts.
            # Let's adapt the relative positions from photo_stakes (28, 45, 62mm from top of 90mm item)
            # Proportionally: (28/90)*120 = 37.3mm, (45/90)*120 = 60mm, (62/90)*120 = 82.6mm
            line_y_offsets_mm = {
                'line_1': 37,
                'line_2': 60,
                'line_3': 83
            }
            font_sizes_pt = { # These are already scaled in __init__
                'line_1': self.line1_font_size_pt,
                'line_2': self.line2_font_size_pt,
                'line_3': self.line3_font_size_pt
            }

            for line_key in ['line_1', 'line_2', 'line_3']:
                text_content = str(order_item_data.get(line_key, '')).strip()
                if text_content:
                    # text_content = self.text_utils.check_grammar_and_typos(text_content) # Optional
                    wrapped_lines = self.text_utils.split_line_to_fit_multiline(text_content, max_chars_per_line=max_chars, max_lines=3)

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
            print(f"Error in _add_large_photo_item_to_svg_slot for order {order_item_data.get('order-id', 'N/A')}: {e}")
            import traceback
            traceback.print_exc()

    def _create_memorial_page_svg(self, orders_on_page: list, filename: str):
        output_path = os.path.join(self.output_dir, filename)
        dwg = svgwrite.Drawing(filename=output_path, size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                               viewBox=f"0 0 {self.page_width_px} {self.page_height_px}")

        for idx, order_item_details_dict in enumerate(orders_on_page):
            if idx >= self.batch_size: break # Max 4 items for this 2x2 grid

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
            self._add_large_photo_item_to_svg_slot(dwg, order_item_details_dict, item_slot_x, item_slot_y)

        # Add reference point for printer alignment
        self.svg_utils.add_reference_point(dwg, self.page_width_px, self.page_height_px, self.px_per_mm)
        try:
            dwg.save(pretty=True)
            print(f"Coloured Large Photo Stake SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving Coloured Large Photo Stake SVG {output_path}: {e}\n{traceback.format_exc()}")

# Register the processor
register_processor("coloured_large_photo_stakes", ColouredLargePhotoStakesProcessor)
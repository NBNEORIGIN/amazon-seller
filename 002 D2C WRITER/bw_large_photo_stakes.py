import os
import svgwrite
import base64 # Added for embed_image
import pandas as pd # Added for pd.isna
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from memorial_base import MemorialBase # Assumed to provide self.px_per_mm, self.pt_to_mm, etc.
from core.processors.text_utils import split_line_to_fit # Keep check_grammar_and_typos if desired
from core.processors.svg_utils import draw_rounded_rect, add_multiline_text

class BWLargePhotoStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'large_stakes_photo_bw' # Updated category name
        
        # Overall memorial dimensions
        self.memorial_width_mm = 200
        self.memorial_height_mm = 120
        # self.corner_radius_mm = 6 # This is for the main item bounding box, often drawn in create_memorial_svg

        # Photo area dimensions and position (derived from user's SVG)
        self.photo_area_x_mm = 13.02
        self.photo_area_y_mm = 9.28
        self.photo_width_mm = 65.18
        self.photo_height_mm = 90.59
        self.photo_corner_radius_mm = 5.4
        self.photo_border_stroke_mm = 1 # Example stroke for photo frame, adjust as needed

        # Convert photo dimensions to pixels
        self.photo_area_x_px = int(self.photo_area_x_mm * self.px_per_mm)
        self.photo_area_y_px = int(self.photo_area_y_mm * self.px_per_mm)
        self.photo_width_px = int(self.photo_width_mm * self.px_per_mm)
        self.photo_height_px = int(self.photo_height_mm * self.px_per_mm)
        self.photo_corner_radius_px = int(self.photo_corner_radius_mm * self.px_per_mm)
        self.photo_border_stroke_px = int(self.photo_border_stroke_mm * self.px_per_mm)

        # Text layout parameters (to the right of the photo)
        self.text_margin_from_photo_mm = 10 # Gap between photo and text area
        self.text_area_margin_right_mm = 10 # Margin on the far right of the text area

        self.text_area_x_mm = self.photo_area_x_mm + self.photo_width_mm + self.text_margin_from_photo_mm
        self.text_area_width_mm = self.memorial_width_mm - self.text_area_x_mm - self.text_area_margin_right_mm

        self.text_area_x_px = int(self.text_area_x_mm * self.px_per_mm)
        self.text_area_width_px = int(self.text_area_width_mm * self.px_per_mm)

        # Font sizes (using PhotoStakesProcessor values as defaults)
        self.line1_size_pt = 17
        self.line2_size_pt = 25
        self.line3_size_pt = 13
        self.text_wrap_chars = 35 # Approx char count for wrapping text lines

        # Grid layout for placing items on the page (e.g., 2 items per SVG)
        self.grid_cols = 2 # Number of items horizontally
        self.grid_rows = 1 # Number of items vertically
        
        # Calculate offsets for the grid on the page (align to bottom-right)
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows
        
        self.x_offset_mm = self.page_width_mm - grid_width_mm
        self.y_offset_mm = self.page_height_mm - grid_height_mm
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

    def embed_image(self, image_path): # Standard embed_image
        try:
            # Determine MIME type based on extension
            ext = os.path.splitext(image_path)[1].lower()
            if ext == ".jpg" or ext == ".jpeg":
                mime_type = "image/jpeg"
            elif ext == ".png":
                mime_type = "image/png"
            else: # Add more types if needed or default
                print(f"Warning: Unsupported image type for embedding: {ext} for {image_path}")
                return None

            with open(image_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('ascii')
            return f'data:{mime_type};base64,{encoded}'
        except Exception as e:
            print(f"embed_image failed for {image_path}: {e}")
            return None

    def add_photo_memorial(self, dwg, x_item_offset, y_item_offset, order):
        # x_item_offset, y_item_offset are the top-left of the current 200x120 memorial slot

        # Photo frame and position within the item slot
        # Photo is placed relative to the item slot's top-left (x_item_offset, y_item_offset)
        frame_x_abs = x_item_offset + self.photo_area_x_px
        frame_y_abs = y_item_offset + self.photo_area_y_px

        # Draw photo border (simple rectangle)
        dwg.add(dwg.rect(
            insert=(frame_x_abs, frame_y_abs),
            size=(self.photo_width_px, self.photo_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='none', # Or a light fill if needed
            stroke='black',
            stroke_width=self.photo_border_stroke_px
        ))

        # Define clip path for the photo (rectangular)
        clip_id = f"clip_{order.get('order-item-id', 'default')}_{x_item_offset}_{y_item_offset}"
        clip_path_rect = dwg.rect(
            insert=(frame_x_abs, frame_y_abs),
            size=(self.photo_width_px, self.photo_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px
        )
        if dwg.defs is None: dwg.defs = dwg.g()

        # Check if clip_path_id already exists to avoid duplicates (optional but good practice)
        existing_clip_path = None
        if dwg.defs.elements:
            for el_val in dwg.defs.elements:
                if hasattr(el_val, 'attribs') and el_val.attribs.get('id') == clip_id:
                    existing_clip_path = el_val; break
        if not existing_clip_path:
            clip_path = dwg.defs.add(dwg.clipPath(id=clip_id))
            clip_path.add(clip_path_rect)

        # Embed photo
        photo_path_str = str(order.get('photo_path', '')).strip()
        actual_photo_path = ""
        if photo_path_str:
            if os.path.isabs(photo_path_str): actual_photo_path = photo_path_str
            elif photo_path_str.lower().startswith("images"): actual_photo_path = os.path.normpath(photo_path_str)
            elif self.graphics_path: actual_photo_path = os.path.join(self.graphics_path, photo_path_str)
            else: actual_photo_path = photo_path_str

        if actual_photo_path and os.path.exists(actual_photo_path):
            photo_data = self.embed_image(actual_photo_path)
            if photo_data:
                dwg.add(dwg.image(
                    href=photo_data,
                    insert=(frame_x_abs, frame_y_abs),
                    size=(self.photo_width_px, self.photo_height_px),
                    clip_path=f'url(#{clip_id})'
                ))
            else: print(f"Warning: Could not embed photo data for {actual_photo_path}")
        else: print(f"Warning: Photo file not found at {actual_photo_path} for SKU {order.get('sku')}")

        # Text placement (to the right of the photo)
        text_start_x_abs = x_item_offset + self.text_area_x_px
        text_center_x_abs = text_start_x_abs + (self.text_area_width_px / 2)

        # Vertical positions for text lines (example: distribute within photo height)
        # These need to be relative to y_item_offset
        line_y_start_abs = y_item_offset + self.photo_area_y_px # Align top of text area with top of photo

        # Line 1
        line1_text = str(order.get('line_1', ''))
        line1_lines = split_line_to_fit(line1_text, self.text_wrap_chars)
        # Adjust y for line1 based on its content, e.g., start 20% down the photo height
        y_pos_l1 = line_y_start_abs + (self.photo_height_px * 0.2)
        dwg.add(add_multiline_text(dwg, line1_lines, insert=(text_center_x_abs, y_pos_l1), font_size=f"{self.line1_size_pt * self.pt_to_mm}mm", font_family="Georgia", anchor="middle", fill="black"))

        # Line 2 (center of photo height)
        line2_text = str(order.get('line_2', ''))
        line2_lines = split_line_to_fit(line2_text, self.text_wrap_chars)
        y_pos_l2 = line_y_start_abs + (self.photo_height_px * 0.5)
        dwg.add(add_multiline_text(dwg, line2_lines, insert=(text_center_x_abs, y_pos_l2), font_size=f"{self.line2_size_pt * self.pt_to_mm}mm", font_family="Georgia", anchor="middle", fill="black"))

        # Line 3 (e.g., 80% down the photo height)
        line3_text = str(order.get('line_3', ''))
        line3_lines = split_line_to_fit(line3_text, self.text_wrap_chars)
        y_pos_l3 = line_y_start_abs + (self.photo_height_px * 0.8)
        dwg.add(add_multiline_text(dwg, line3_lines, insert=(text_center_x_abs, y_pos_l3), font_size=f"{self.line3_size_pt * self.pt_to_mm}mm", font_family="Georgia", anchor="middle", fill="black"))

    def create_memorial_svg(self, orders_in_batch_dicts, batch_num):
        # orders_in_batch_dicts is a list of order dictionaries
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)

        dwg = svgwrite.Drawing(
            filepath,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )

        for idx, order_dict in enumerate(orders_in_batch_dicts):
            if idx >= self.grid_cols * self.grid_rows: # Max items per SVG page
                break

            # Calculate top-left (x,y) for the current memorial slot on the page
            # Assumes items are filled right-to-left, bottom row first (if multiple rows)
            # For single row (self.grid_rows = 1):
            item_col_idx = self.grid_cols - 1 - (idx % self.grid_cols) # right to left
            item_row_idx = self.grid_rows - 1 - (idx // self.grid_cols) # bottom up (relevant if grid_rows > 1)

            x = self.x_offset_px + item_col_idx * (self.memorial_width_mm * self.px_per_mm)
            y = self.y_offset_px + item_row_idx * (self.memorial_height_mm * self.px_per_mm)

            # Draw main bounding box for the memorial item
            # Determine stroke color based on attention flags (example from PhotoStakesProcessor)
            is_attention_order = False
            order_colour_lower = str(order_dict.get('colour', '')).lower()
            order_type_lower = str(order_dict.get('type', '')).lower()
            if order_colour_lower in ['marble', 'stone']: is_attention_order = True
            if order_type_lower == 'large plaque' or order_type_lower == 'regular plaque': is_attention_order = True

            slot_stroke_color = 'yellow' if is_attention_order else '#ff0000' # Default red, yellow for attention

            dwg.add(dwg.rect(
                insert=(x, y),
                size=(self.memorial_width_mm * self.px_per_mm, self.memorial_height_mm * self.px_per_mm),
                rx=6 * self.px_per_mm, # Example corner radius
                ry=6 * self.px_per_mm,
                fill='none',
                stroke=slot_stroke_color,
                stroke_width=0.1 * self.px_per_mm
            ))

            self.add_photo_memorial(dwg, x, y, order_dict) # Pass the offsets and order data

        self.add_reference_point(dwg) # From MemorialBase
        dwg.save()
        print(f"Saved SVG: {filepath}")
        return dwg # Not strictly necessary to return but can be useful

    def process_orders(self, df):
        df.columns = [col.lower() for col in df.columns]
        if 'photo_path' not in df.columns:
            if 'image_path' in df.columns:
                df['photo_path'] = df['image_path']
            else:
                df['photo_path'] = pd.NA # Use pd.NA for missing data
        else:
            if 'image_path' in df.columns:
                # Fill missing photo_path only if image_path is present and photo_path is NA
                df['photo_path'] = df['photo_path'].fillna(df['image_path'])

        # Filter for B&W large photo stakes
        # Ensure all columns used in filter exist and are of correct type for string operations
        df['colour'] = df.get('colour', pd.Series(dtype='str')).astype(str).str.lower()
        df['type'] = df.get('type', pd.Series(dtype='str')).astype(str).str.lower()
        df['decorationtype'] = df.get('decorationtype', pd.Series(dtype='str')).astype(str).str.lower()
        df['photo_path'] = df.get('photo_path', pd.Series(dtype='str')).astype(str).str.strip()

        filtered_stakes = df[
            (df['colour'] == 'black') &
            (df['type'].str.contains('large stake', case=False, na=False)) &
            (df['decorationtype'] == 'photo') &
            (df['photo_path'].notna() & (df['photo_path'] != ''))
        ].copy()

        if filtered_stakes.empty:
            print(f"No orders found for {self.CATEGORY} after filtering.")
            return

        # Process in batches (self.grid_cols * self.grid_rows items per SVG page)
        batch_size = self.grid_cols * self.grid_rows
        batch_num = 1
        for start_idx in range(0, len(filtered_stakes), batch_size):
            batch_orders_df = filtered_stakes.iloc[start_idx:start_idx + batch_size]
            if not batch_orders_df.empty:
                self.create_memorial_svg(batch_orders_df.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders_df.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1
import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import draw_rounded_rect, add_multiline_text

class BWLargePhotoStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'B&W_LARGE_PHOTO_STAKES'
        
        # Override memorial dimensions for large stakes
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
        self.text_right_shift_mm = 30
        
        # Convert dimensions to pixels
        self.memorial_width_px = int(self.memorial_width_mm * self.px_per_mm)
        self.memorial_height_px = int(self.memorial_height_mm * self.px_per_mm)
        self.corner_radius_px = int(self.corner_radius_mm * self.px_per_mm)
        
        # Convert photo dimensions to pixels
        self.photo_width_px = int(self.photo_width_mm * self.px_per_mm)
        self.photo_height_px = int(self.photo_height_mm * self.px_per_mm)
        self.photo_clip_width_px = int(self.photo_clip_width_mm * self.px_per_mm)
        self.photo_clip_height_px = int(self.photo_clip_height_mm * self.px_per_mm)
        self.photo_border_stroke_px = int(self.photo_border_stroke_mm * self.px_per_mm)
        self.photo_outline_stroke_px = int(self.photo_outline_stroke_mm * self.px_per_mm)
        self.photo_corner_radius_px = int(self.photo_corner_radius_mm * self.px_per_mm)
        self.photo_left_margin_px = int(self.photo_left_margin_mm * self.px_per_mm)
        self.text_right_shift_px = int(self.text_right_shift_mm * self.px_per_mm)
        
        # Calculate grid layout (1x2)
        self.grid_cols = 2
        self.grid_rows = 1
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows
        
        # Align to right and bottom of page
        self.x_offset_mm = self.page_width_mm - grid_width_mm
        self.y_offset_mm = self.page_height_mm - grid_height_mm
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)
        # Text sizes (pt)
        self.line1_size_pt = 17
        self.line2_size_pt = 25

        # Load OM008016BW path data
        self.d_clip_ellipse_om008016bw = ""
        self.d_border_om008016bw = ""
        try:
            clip_path_file = os.path.join(os.path.dirname(__file__), '..', 'assets', '002_svg_templates', 'OM008016BW_clip_path.txt')
            border_path_file = os.path.join(os.path.dirname(__file__), '..', 'assets', '002_svg_templates', 'OM008016BW_border_path.txt')
            if os.path.exists(clip_path_file):
                with open(clip_path_file, 'r') as f:
                    self.d_clip_ellipse_om008016bw = f.read().strip()
            else:
                print(f"WARNING: OM008016BW_clip_path.txt not found at {clip_path_file}")
            if os.path.exists(border_path_file):
                with open(border_path_file, 'r') as f:
                    self.d_border_om008016bw = f.read().strip()
            else:
                print(f"WARNING: OM008016BW_border_path.txt not found at {border_path_file}")
        except Exception as e:
            print(f"ERROR: Could not load OM008016BW path data: {e}")


    def add_photo_memorial(self, dwg, x, y, order):
        is_om008016bw = (str(order.get('sku', '')).strip().upper() == 'OM008016BW')

        if is_om008016bw and self.d_clip_ellipse_om008016bw and self.d_border_om008016bw:
            # Specific logic for OM008016BW
            om_slot_group = dwg.g(transform=f"translate({x},{y})") # Slot position in pixels

            clip_path_id = f"omClip_{order.get('order-id', 'default').replace('-', '_').replace('.', '_')}_{int(x)}_{int(y)}"

            # Transform from template analysis (values are in mm)
            tx_g1_mm = -5.0270797
            ty_g1_mm = -86.4915987
            transform_g1_template_units_str = f"translate({tx_g1_mm},{ty_g1_mm})"

            # Create the clipPath definition. Contents are in mm, and will be scaled by the `template_content_group`
            # when the image (which is also in that group) is rendered.
            clip_path_def_content_group = dwg.g(transform=f"scale({self.px_per_mm})") # Scale the path to behave as if in pixel space for the clipPath def
            clip_path_def_content_group.add(dwg.path(d=self.d_clip_ellipse_om008016bw, transform=transform_g1_template_units_str))

            # Ensure dwg.defs exists
            if dwg.defs is None:
                dwg.defs = dwg.g() # SVG spec allows g for defs, svgwrite might need proper dwg.defs()

            # Check if clip path with this ID already exists
            existing_clip_path = dwg.defs.querySelector(f"#{clip_path_id}")
            if not existing_clip_path:
                 clip_path_element = dwg.clipPath(id=clip_path_id)
                 clip_path_element.add(clip_path_def_content_group)
                 dwg.defs.add(clip_path_element)


            # This group scales its children (defined in mm) by px_per_mm.
            template_content_group = om_slot_group.add(dwg.g(transform=f"scale({self.px_per_mm})"))

            # Floral Border (defined in mm, transformed by mm-based g1)
            template_content_group.add(dwg.path(d=self.d_border_om008016bw, style="fill:#000000;stroke:none;", transform=transform_g1_template_units_str))

            # Photo Embedding (defined and positioned in mm)
            photo_path_str = str(order.get('photo_path', ''))
            if photo_path_str and not pd.isna(photo_path_str):
                actual_photo_path = photo_path_str
                if not os.path.isabs(photo_path_str):
                    actual_photo_path = os.path.join(self.graphics_path, photo_path_str.replace('\\', os.sep))

                if os.path.exists(actual_photo_path):
                    photo_data = self.embed_image(actual_photo_path)
                    if photo_data:
                        img_x_mm = 15.1252413
                        img_y_mm = 16.4017223
                        img_width_mm = 67.046234
                        img_height_mm = 87.148118

                        photo_image = dwg.image(
                            href=photo_data,
                            insert=(f"{img_x_mm}mm", f"{img_y_mm}mm"),
                            size=(f"{img_width_mm}mm", f"{img_height_mm}mm")
                        )
                        photo_image.attribs['clip-path'] = f'url(#{clip_path_id})'
                        template_content_group.add(photo_image)
                    else:
                        print(f"Failed to embed photo for OM008016BW: {actual_photo_path}")
                else:
                    print(f"Warning: Photo not found for OM008016BW at {actual_photo_path}")
            else:
                print(f"Warning: No photo_path provided for OM008016BW, order ID: {order.get('order-id', 'N/A')}")

            # Red Bounding Box (defined in mm)
            rect_x_mm = 0.05
            rect_y_mm = 0.05
            rect_width_mm = 199.90007
            rect_height_mm = 119.90007
            rect_ry_mm = 5.9950037
            rect_stroke_width_mm = 0.0999334

            template_content_group.add(dwg.rect(
                insert=(f"{rect_x_mm}mm", f"{rect_y_mm}mm"),
                size=(f"{rect_width_mm}mm", f"{rect_height_mm}mm"),
                ry=f"{rect_ry_mm}mm",
                style=f"fill:none;stroke:#ff0000;stroke-width:{rect_stroke_width_mm}mm"
            ))

            dwg.add(om_slot_group)
            # Text elements are intentionally omitted for OM008016BW.

        else:
            # Original logic for other SKUs
            # Use default pixel dimensions calculated in __init__
            dwg.add(draw_rounded_rect(
            dwg,
            insert=(x, y),
            size=(self.memorial_width_px, self.memorial_height_px),
            rx=self.corner_radius_px,
            ry=self.corner_radius_px,
            fill='none',
            stroke='black',
            stroke_width=1
        ))
        
        # Add photo frame
        frame_x = x + self.photo_left_margin_px
        frame_y = y + (self.memorial_height_px - self.photo_height_px) / 2
        
        # Calculate center position for the clipping rectangle
        clip_x = frame_x + (self.photo_width_px - self.photo_clip_width_px) / 2
        clip_y = frame_y + (self.photo_height_px - self.photo_clip_height_px) / 2
        
        # Calculate text area center for the blue outline
        text_x = frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_px - (text_x - x) - self.text_right_shift_px
        text_center_x = text_x + text_area_width / 2 - (self.photo_clip_width_px / 2)
        text_center_y = y + (28 * self.px_per_mm)  # Align with line 1
        
        # Add black background rectangle for photo visibility
        # Use shared SVG utility for black background rectangle for photo
        dwg.add(draw_rounded_rect(
            dwg,
            insert=(clip_x, clip_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='black',
            stroke='none',
            stroke_width=0
        ))
        
        # Add clipping rectangle with same dimensions
        clip_rect = dwg.rect(
            insert=(clip_x, clip_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='none',
            stroke='none'
        )
        
        # Add clipping path using the rectangle
        clip_path = dwg.defs.add(dwg.clipPath(id=f'clip_{x}_{y}'))
        clip_path.add(clip_rect)
        
        # Add blue outlined rectangle centered over text
        dwg.add(dwg.rect(
            insert=(text_center_x, text_center_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='none',
            stroke='blue',
            stroke_width=self.photo_outline_stroke_px
        ))
        
        # Add photo border with thick stroke
        dwg.add(dwg.rect(
            insert=(frame_x, frame_y),
            size=(self.photo_width_px, self.photo_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='none',
            stroke='black',
            stroke_width=self.photo_border_stroke_px
        ))
        
        # Add photo if path exists
        if not pd.isna(order['photo_path']):
            # Handle both absolute and relative paths
            photo_path = order['photo_path']
            if not os.path.isabs(photo_path):
                # If path is relative, join with graphics_path
                photo_path = os.path.join(self.graphics_path, photo_path.replace('\\', os.sep))
            
            print(f"Looking for photo: {photo_path}")
            if os.path.exists(photo_path):
                print(f"Found photo: {photo_path}")
                photo_data = self.embed_image(photo_path)
                if photo_data:
                    print(f"Successfully embedded photo")
                    photo = dwg.image(
                        href=photo_data,
                        insert=(frame_x, frame_y),
                        size=(self.photo_width_px, self.photo_height_px),
                        clip_path=f'url(#clip_{x}_{y})'
                    )
                    dwg.add(photo)
                else:
                    print(f"Failed to embed photo")
            else:
                print(f"Warning: Photo not found at {photo_path}")
        
        # Add text elements
        text_x = frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_px - (text_x - x) - self.text_right_shift_px
        text_center_x = text_x + text_area_width / 2
        
        pt_to_mm = 0.352778
        if not pd.isna(order['line_1']):
            line1_y = y + (28 * self.px_per_mm)
            lines = split_line_to_fit(str(order['line_1']), 30)
            for idx, line in enumerate(lines):
                dy = 0 if idx == 0 else self.line1_size_pt * pt_to_mm * 1.3
                dwg.add(add_multiline_text(
                    dwg,
                    [line],
                    insert=(text_center_x, line1_y + dy),
                    font_size=f"{self.line1_size_pt * pt_to_mm}mm",
                    font_family="Georgia",
                    anchor="middle",
                    fill="black"
                ))
        if not pd.isna(order['line_2']):
            line2_y = y + (45 * self.px_per_mm)
            lines = split_line_to_fit(str(order['line_2']), 30)
            for idx, line in enumerate(lines):
                dy = 0 if idx == 0 else self.line2_size_pt * pt_to_mm * 1.3
                dwg.add(add_multiline_text(
                    dwg,
                    [line],
                    insert=(text_center_x, line2_y + dy),
                    font_size=f"{self.line2_size_pt * pt_to_mm}mm",
                    font_family="Georgia",
                    anchor="middle",
                    fill="black"
                ))
        if not pd.isna(order['line_3']):
            base_y = y + (57 * self.px_per_mm)
            lines = split_line_to_fit(str(order['line_3']), 30)
            for idx, line in enumerate(lines):
                dy = 0 if idx == 0 else 12 * pt_to_mm * 1.3
                dwg.add(add_multiline_text(
                    dwg,
                    [line],
                    insert=(text_center_x, base_y + dy),
                    font_size=f"{12 * pt_to_mm}mm",
                    font_family="Georgia",
                    anchor="middle",
                    fill="black"
                ))

    def create_memorial_svg(self, orders, batch_num):
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        dwg = svgwrite.Drawing(
            filepath,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )
        # Process 2 memorials in 1x2 grid
        for idx, order in enumerate(orders):
            if idx >= 2:
                break
            row = idx // self.grid_cols
            col = idx % self.grid_cols
            x = self.x_offset_px + col * self.memorial_width_px
            y = self.y_offset_px + row * self.memorial_height_px
            self.add_photo_memorial(dwg, x, y, order)
        # Add reference point
        self.add_reference_point(dwg)
        dwg.save()
        return dwg

    def process_orders(self, df):
        # Normalize column names to lowercase
        df.columns = [col.lower() for col in df.columns]
        # Ensure 'photo_path' column exists and is filled from 'image_path' if missing
        if 'photo_path' not in df.columns:
            if 'image_path' in df.columns:
                df['photo_path'] = df['image_path']
            else:
                df['photo_path'] = pd.NA
        else:
            # If photo_path exists but is empty, and image_path exists, fill missing photo_path with image_path
            if 'image_path' in df.columns:
                df['photo_path'] = df['photo_path'].combine_first(df['image_path'])
        # Filter for B&W large photo stakes
        large_photo_stakes = df[
            (df['colour'].str.lower() == 'black') & 
            (df['type'].str.contains('large stake', case=False, na=False)) &
            (df['decorationtype'].str.lower() == 'photo') &
            (df['photo_path'].notna())
        ].copy()
        # Process in batches of 2
        batch_num = 1
        for start_idx in range(0, len(large_photo_stakes), 2):
            batch_orders = large_photo_stakes.iloc[start_idx:start_idx + 2]
            if not batch_orders.empty:
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1
import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd

class BWPhotoStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'BW_PHOTO'
        # Dimensions and layout for regular stake (same as bw_stakes.py, but with photo)
        self.memorial_width_mm = 200
        self.memorial_height_mm = 120
        self.corner_radius_mm = 6
        # Photo dimensions and margins (same as photo_stakes.py)
        self.photo_width_mm = 50.5
        self.photo_height_mm = 68.8
        self.photo_clip_width_mm = 50.378
        self.photo_clip_height_mm = 68.901
        self.photo_border_stroke_mm = 3.65
        self.photo_outline_stroke_mm = 0.1
        self.photo_corner_radius_mm = 6
        self.photo_left_margin_mm = 7.7
        self.text_right_shift_mm = 30
        # Convert to pixels
        self.photo_width_px = int(self.photo_width_mm * self.px_per_mm)
        self.photo_height_px = int(self.photo_height_mm * self.px_per_mm)
        self.photo_clip_width_px = int(self.photo_clip_width_mm * self.px_per_mm)
        self.photo_clip_height_px = int(self.photo_clip_height_mm * self.px_per_mm)
        self.photo_border_stroke_px = int(self.photo_border_stroke_mm * self.px_per_mm)
        self.photo_outline_stroke_px = int(self.photo_outline_stroke_mm * self.px_per_mm)
        self.photo_corner_radius_px = int(self.photo_corner_radius_mm * self.px_per_mm)
        self.photo_left_margin_px = int(self.photo_left_margin_mm * self.px_per_mm)
        self.text_right_shift_px = int(self.text_right_shift_mm * self.px_per_mm)
        # Layout for 3 memorials in top row
        self.grid_cols = 3
        self.grid_rows = 1
        self.x_offset_mm = 0
        self.y_offset_mm = 0
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

    def add_photo_memorial(self, dwg, x, y, order):
        # Add memorial outline with rounded corners
        dwg.add(dwg.rect(
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
        clip_x = frame_x
        clip_y = frame_y
        # Draw photo rectangle
        dwg.add(dwg.rect(
            insert=(clip_x, clip_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='black'
        ))
        # Add clipping rectangle
        clip_rect = dwg.rect(
            insert=(clip_x, clip_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='none',
            stroke='none'
        )
        clip_path = dwg.defs.add(dwg.clipPath(id=f'clip_{x}_{y}'))
        clip_path.add(clip_rect)
        # Blue outline
        dwg.add(dwg.rect(
            insert=(clip_x, clip_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='none',
            stroke='blue',
            stroke_width=self.photo_outline_stroke_px
        ))
        # Photo border
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
        photo_path = order.get('image_path', '')
        if isinstance(photo_path, str) and photo_path.strip() != '' and not pd.isna(photo_path):
            if os.path.exists(photo_path):
                photo_data = self.embed_image(photo_path)
                if photo_data:
                    photo = dwg.image(
                        href=photo_data,
                        insert=(frame_x, frame_y),
                        size=(self.photo_width_px, self.photo_height_px),
                        clip_path=f'url(#clip_{x}_{y})'
                    )
                    dwg.add(photo)
        # Add text elements
        text_x = frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_px - (text_x - x) - self.text_right_shift_px
        text_center_x = text_x + text_area_width / 2
        if not pd.isna(order['line_1']):
            line1_y = y + (28 * self.px_per_mm)
            dwg.add(dwg.text(
                str(order['line_1']),
                insert=(text_center_x, line1_y),
                font_size=f"{17 * self.pt_to_mm}mm",
                font_family="Georgia",
                text_anchor="middle",
                fill="black"
            ))
        if not pd.isna(order['line_2']):
            line2_y = y + (45 * self.px_per_mm)
            dwg.add(dwg.text(
                str(order['line_2']),
                insert=(text_center_x, line2_y),
                font_size=f"{25 * self.pt_to_mm}mm",
                font_family="Georgia",
                text_anchor="middle",
                fill="black"
            ))
        if not pd.isna(order['line_3']):
            lines = self.wrap_text(str(order['line_3']))
            for line_idx, line in enumerate(lines):
                line3_y = y + ((57 + line_idx * 4) * self.px_per_mm)
                dwg.add(dwg.text(
                    line.strip(),
                    insert=(text_center_x, line3_y),
                    font_size=f"{12 * self.pt_to_mm}mm",
                    font_family="Georgia",
                    text_anchor="middle",
                    fill="black"
                ))

    def create_memorial_svg(self, orders, batch_num):
        import traceback
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)

        try:
            dwg = svgwrite.Drawing(
                filepath,
                size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
            )
            # Process 3 memorials in top row
            for idx, order in enumerate(orders):
                if idx >= 3:
                    break
                row = 0
                col = idx
                x = self.x_offset_px + (col * self.memorial_width_px)
                y = self.y_offset_px + (row * self.memorial_height_px)

                self.add_photo_memorial(dwg, x, y, order)
            # Add reference point
            self.add_reference_point(dwg)

            dwg.save()

        except Exception as e:
            tb = traceback.format_exc()


    def process_orders(self, orders):

        # Accept both DataFrame and list
        if isinstance(orders, list):
            df = pd.DataFrame(orders)
        else:
            df = orders.copy()
        df.columns = [col.lower() for col in df.columns]


        # --- Select B&W regular photo stakes ---
        bw_photo_stakes = df[
            (df['type'] == 'regular stake') &
            (df['colour'] == 'black') &
            (df['image_path'].notna()) & (df['image_path'] != '') &
            (df['decorationtype'] == 'photo')
        ].copy()


        if bw_photo_stakes.empty:
    
            return
        # Process in batches of 3 (top row)
        batch_num = 1
        for start_idx in range(0, len(bw_photo_stakes), 3):
            batch_orders = bw_photo_stakes.iloc[start_idx:start_idx + 3]
            if not batch_orders.empty:
        
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1

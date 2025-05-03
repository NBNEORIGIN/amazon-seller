import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd

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
        clip_x = frame_x + (self.photo_width_px - self.photo_clip_width_px) / 2
        clip_y = frame_y + (self.photo_height_px - self.photo_clip_height_px) / 2
        
        # Calculate text area center for the blue outline
        text_x = frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_px - (text_x - x) - self.text_right_shift_px
        text_center_x = text_x + text_area_width / 2 - (self.photo_clip_width_px / 2)
        text_center_y = y + (28 * self.px_per_mm)  # Align with line 1
        
        # Add black background rectangle for photo visibility
        dwg.add(dwg.rect(
            insert=(clip_x, clip_y),
            size=(self.photo_clip_width_px, self.photo_clip_height_px),
            rx=self.photo_corner_radius_px,
            ry=self.photo_corner_radius_px,
            fill='black'
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
            x = self.x_offset_px + (col * self.memorial_width_px)
            y = self.y_offset_px + (row * self.memorial_height_px)
            
            self.add_photo_memorial(dwg, x, y, order)
        
        # Add reference point
        self.add_reference_point(dwg)
        dwg.save()
        return dwg

    def process_orders(self, df):
        # Filter for B&W large photo stakes
        large_photo_stakes = df[
            (df['COLOUR'].str.lower() == 'black') & 
            (df['TYPE'].str.contains('Large Stake', case=False, na=False)) &
            (df['photo_path'].notna())
        ].copy()
        
        print(f"\nFound {len(large_photo_stakes)} B&W Large Photo Stakes")
        
        # Process in batches of 2
        batch_num = 1
        for start_idx in range(0, len(large_photo_stakes), 2):
            batch_orders = large_photo_stakes.iloc[start_idx:start_idx + 2]
            if not batch_orders.empty:
                print(f"\nProcessing B&W Large Photo Stakes batch {batch_num}...")
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1
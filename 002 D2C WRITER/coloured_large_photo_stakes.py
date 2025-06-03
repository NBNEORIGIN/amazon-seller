import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import draw_rounded_rect, add_multiline_text

class ColouredLargePhotoStakesProcessor(MemorialBase):
    def process_orders(self, orders):

        # Accept both DataFrame and list
        if isinstance(orders, list):
            df = pd.DataFrame(orders)
        else:
            df = orders.copy()
        df.columns = [col.lower() for col in df.columns]


        # --- Select coloured large photo stakes using 'decorationtype' field ---
        allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble']
        if 'decorationtype' not in df.columns:
            print("Warning: 'decorationtype' column not found in input orders. Please ensure order_pipeline.py was run after updating SKULIST.csv.")
            df['decorationtype'] = ''
        # Normalize relevant columns for robust filtering
        df['type'] = df['type'].astype(str).str.strip().str.lower()
        df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        df['decorationtype'] = df['decorationtype'].astype(str).str.strip().str.lower()
        allowed_colours_lower = [c.lower() for c in allowed_colours]
        # Enhanced diagnostics



        # Show why rows are excluded
        excluded_rows = []
        for idx, row in df.iterrows():
            reasons = []
            if row['type'] != 'large stake':
                reasons.append(f"type={row['type']}")
            if row['colour'] not in allowed_colours_lower:
                reasons.append(f"colour={row['colour']}")
            if pd.isna(row['image_path']) or row['image_path'] == '':
                reasons.append("missing image_path")
            if row['decorationtype'] != 'photo':
                reasons.append(f"decorationtype={row['decorationtype']}")
            if reasons:
                excluded_rows.append((idx, reasons))

        large_photo_stakes = df[
            (df['type'] == 'large stake') &
            (df['colour'].isin(allowed_colours_lower)) &
            (df['image_path'].notna()) & (df['image_path'] != '') &
            (df['decorationtype'] == 'photo')
        ].copy()
        print(f"Eligible large photo stakes: {len(large_photo_stakes)}")
        if not large_photo_stakes.empty:
            print(large_photo_stakes[['order-id','sku','type','colour','decorationtype','image_path']])
        else:
            print("No eligible large photo stakes found.")
        print(f"Rows after filtering for Large Stake, allowed colours, and DecorationType == 'photo': {len(large_photo_stakes)}")
        print(large_photo_stakes[['order-id', 'sku', 'colour', 'decorationtype']].head() if not large_photo_stakes.empty else large_photo_stakes.head())
        if large_photo_stakes.empty:
            print("No eligible coloured large photo stakes found for coloured_large_photo_stakes.py processor.")
            return
        # Process in batches of 4 (2x2 grid)
        batch_num = 1
        for start_idx in range(0, len(large_photo_stakes), 4):
            batch_orders = large_photo_stakes.iloc[start_idx:start_idx + 4]
            if not batch_orders.empty:
                print(f"\nProcessing Coloured Large Photo batch {batch_num}...")
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1

    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'COLOURED_LARGE_PHOTO_STAKES'
        
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
        
        # Calculate grid layout (2x2)
        self.grid_cols = 2
        self.grid_rows = 2
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
            fill='white',
            stroke='black',
            stroke_width=self.photo_outline_stroke_px
        ))

        # Embed photo if available
        photo_path = order.get('image_path', '')
        if isinstance(photo_path, str) and photo_path.strip() != '' and not pd.isna(photo_path):
            if os.path.exists(photo_path):
                dwg.add(dwg.image(
                    href=photo_path,
                    insert=(frame_x, frame_y),
                    size=(self.photo_width_px, self.photo_height_px),
                    preserveAspectRatio='xMidYMid slice'
                ))
            else:
                print(f"Photo not found: {photo_path}")
        
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
        
        # Calculate text area center for the blue outline
        text_x = frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_px - (text_x - x) - self.text_right_shift_px
        text_center_x = text_x + text_area_width / 2
        text_center_y = y + (28 * self.px_per_mm)  # Align with line 1

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
        
        # Add photo border using shared SVG utility
        dwg.add(draw_rounded_rect(
            dwg,
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
            dwg.add(add_multiline_text(
                dwg,
                [order.get('line_1', '')],
                insert=(text_center_x, line1_y),
                font_size=f"{self.line1_size_pt}pt",
                font_family="Georgia",
                anchor="middle",
                fill="black"
            ))
        
        if not pd.isna(order['line_2']):
            line2_y = y + (45 * self.px_per_mm)
            dwg.add(add_multiline_text(
                dwg,
                [str(order['line_2'])],
                insert=(text_center_x, line2_y),
                font_size=f"{self.line2_size_pt}pt",
                font_family="Georgia",
                anchor="middle",
                fill="black"
            ))
        
        if not pd.isna(order['line_3']):
            lines = split_line_to_fit(str(order['line_3']), 30)
            for line_idx, line in enumerate(lines):
                line3_y = y + ((57 + line_idx * 4) * self.px_per_mm)
                dwg.add(add_multiline_text(
                    dwg,
                    [line.strip()],
                    insert=(text_center_x, line3_y),
                    font_size=f"{12 * self.pt_to_mm}mm",
                    font_family="Georgia",
                    anchor="middle",
                    fill="black"
                ))

    def create_memorial_svg(self, orders, batch_num):
        import traceback
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        print(f"[ColouredLargePhotoStakesProcessor] Creating SVG: {filepath}")
        try:
            dwg = svgwrite.Drawing(
                filepath,
                size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
            )
            # Process 4 memorials in 2x2 grid
            for idx, order in enumerate(orders):
                if idx >= 4:
                    break
                row = idx // self.grid_cols
                col = idx % self.grid_cols
                x = self.x_offset_px + (col * self.memorial_width_px)
                y = self.y_offset_px + (row * self.memorial_height_px)
                print(f"  Adding photo memorial at grid ({row}, {col}) position: x={x}, y={y}")
                self.add_photo_memorial(dwg, x, y, order)
            # Add reference point
            self.add_reference_point(dwg)
            print(f"[ColouredLargePhotoStakesProcessor] Saving SVG to: {filepath}")
            dwg.save()
            print(f"[ColouredLargePhotoStakesProcessor] SVG successfully written: {filepath}")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[ColouredLargePhotoStakesProcessor] ERROR: Failed to write SVG {filepath}\n{tb}")



import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd

class PhotoStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        print('PhotoStakesProcessor.__init__ called')
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'PHOTO'
        
        # Photo dimensions and margins (in mm)
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

    def add_photo_memorial(self, dwg, x, y, order):
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
        if not pd.isna(order['image_path']):
            photo_path = order['image_path']
            print(f"Looking for photo: {photo_path}")
            norm_path = os.path.normpath(photo_path)
            print(f"[add_photo_memorial] photo_path: {photo_path}")
            print(f"[add_photo_memorial] Normalized: {norm_path}")
            print(f"[add_photo_memorial] Exists: {os.path.exists(norm_path)}")
            if os.path.exists(norm_path):
                print(f"Found photo: {norm_path}")
                photo_data = self.embed_image(norm_path)
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
        
        # Calculate text area dimensions
        text_x = frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_px - (text_x - x) - self.text_right_shift_px
        text_center_x = text_x + text_area_width / 2
        
        # Add text elements with consistent sizing from regular stakes
        if not pd.isna(order['line_1']):
            line1_y = y + (28 * self.px_per_mm)  # Same as regular stakes
            dwg.add(dwg.text(
                str(order['line_1']),
                insert=(text_center_x, line1_y),
                font_size=f"{17 * self.pt_to_mm}mm",  # Same as regular stakes
                font_family="Georgia",
                text_anchor="middle",
                fill="black"
            ))
        
        if not pd.isna(order['line_2']):
            line2_y = y + (45 * self.px_per_mm)  # Same as regular stakes
            dwg.add(dwg.text(
                str(order['line_2']),
                insert=(text_center_x, line2_y),
                font_size=f"{25 * self.pt_to_mm}mm",  # Same as regular stakes
                font_family="Georgia",
                text_anchor="middle",
                fill="black"
            ))
        
        if not pd.isna(order['line_3']):
            lines = self.wrap_text(str(order['line_3']))
            for line_idx, line in enumerate(lines):
                line3_y = y + ((57 + line_idx * 4) * self.px_per_mm)  # Same as regular stakes
                dwg.add(dwg.text(
                    line.strip(),
                    insert=(text_center_x, line3_y),
                    font_size=f"{12 * self.pt_to_mm}mm",  # Same as regular stakes
                    font_family="Georgia",
                    text_anchor="middle",
                    fill="black"
                ))

    def create_memorial_svg(self, orders, batch_num):
        if orders:
            print(f"Batch {batch_num} first order text fields: line_1={orders[0].get('line_1', '')}, line_2={orders[0].get('line_2', '')}, line_3={orders[0].get('line_3', '')}")
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        output_path = os.path.join(self.OUTPUT_DIR, filename)
        
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )
        
        # Process 3 memorials in top row
        for idx, order in enumerate(orders):
            if idx >= 3:
                break
                
            row = 0  # Always top row
            col = idx
            x = self.x_offset_px + (col * self.memorial_width_px)
            y = self.y_offset_px + (row * self.memorial_height_px)
            
            # Add memorial outline
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(self.memorial_width_px, self.memorial_height_px),
                rx=6*self.px_per_mm,
                ry=6*self.px_per_mm,
                fill='none',
                stroke='red',
                stroke_width=0.1*self.px_per_mm
            ))
            
            self.add_photo_memorial(dwg, x, y, order)
        
        # Add reference point
        ref_size_px = 0.1 * self.px_per_mm
        x_pos = self.page_width_px - ref_size_px
        y_pos = (289.8 - 0.011) * self.px_per_mm - ref_size_px
        
        dwg.add(dwg.rect(
            insert=(x_pos, y_pos),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))
        
        dwg.save()
        return dwg

    def process_orders(self, orders):
        print('PhotoStakesProcessor.process_orders called')
        # Accept both DataFrame and list
        if isinstance(orders, list):
            df = pd.DataFrame(orders)
        else:
            df = orders.copy()
        df.columns = [col.lower() for col in df.columns]
        print(f"Columns after normalization: {list(df.columns)}")
        print(df.head())
        # --- Select photo stakes using 'decorationtype' field ---
        if 'decorationtype' not in df.columns:
            print("Warning: 'decorationtype' column not found in input orders. Please ensure order_pipeline.py was run after updating SKULIST.csv.")
            df['decorationtype'] = ''
        allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble']
        photo_stakes = df[
            (df['type'] == 'regular stake') &
            (df['colour'].isin(allowed_colours)) &
            (df['image_path'].notna()) & (df['image_path'] != '') &
            (df['decorationtype'] == 'photo')
        ].copy()
        print(f"Rows after filtering for Regular Stake, allowed colours, and DecorationType == 'photo': {len(photo_stakes)}")
        print(photo_stakes[['order-id', 'sku', 'colour', 'decorationtype']].head() if not photo_stakes.empty else photo_stakes.head())
        if photo_stakes.empty:
            print("No eligible photo stakes found for photo_stakes.py processor.")
            return
        # Process in batches of 3
        batch_num = 1
        for start_idx in range(0, len(photo_stakes), 3):
            batch_orders = photo_stakes.iloc[start_idx:start_idx + 3]
            if not batch_orders.empty:
                print(f"\nProcessing Photo batch {batch_num}...")
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1
if __name__ == "__main__":
    print('photo_stakes.py main block started')
    import sys
    import pandas as pd
    import os
    from pathlib import Path
    import traceback

    try:
        output_dir = sys.argv[1] if len(sys.argv) > 1 else "SVG_OUTPUT"
        graphics_path = sys.argv[2] if len(sys.argv) > 2 else "G:/My Drive/001 NBNE/001 M/M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM/001 Design/002 MUTOH/002 AUTODESIGN"
        images_path = sys.argv[3] if len(sys.argv) > 3 else "G:/My Drive/003 APPS/002 AmazonSeller/004 IMAGES"

        orders_txt = str(Path(__file__).parent.parent / "001 AMAZON DATA DOWNLOAD" / "output.txt")
        if not os.path.exists(orders_txt):
            msg = f"Error: {orders_txt} does not exist. Please run order processing first."
            print(msg)
            with open("photo_stakes_error.log", "w", encoding="utf-8") as f:
                f.write(msg + "\n")
            sys.exit(1)

        print('Reading orders from file')
        orders = pd.read_csv(orders_txt, sep='\t', encoding='utf-8')
        print(f"Loaded columns: {list(orders.columns)}")
        print(orders.head())
        print('Creating PhotoStakesProcessor')
        processor = PhotoStakesProcessor(graphics_path, output_dir)
        print('Calling process_orders')
        processor.process_orders(orders)
        print('PhotoStakesProcessor.process_orders finished')
    except Exception as e:
        tb = traceback.format_exc()
        print("Exception occurred in photo_stakes.py:\n" + tb, file=sys.stderr)
        with open("photo_stakes_error.log", "w", encoding="utf-8") as f:
            f.write(tb)
        sys.exit(1)
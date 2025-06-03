import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import draw_rounded_rect, add_multiline_text

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
        self.grid_cols = 3
        self.grid_rows = 1
        self.x_offset_mm = 0
        self.y_offset_mm = 0
        # Text sizes (pt)
        self.line1_size_pt = 17
        self.line2_size_pt = 25

    def add_photo_memorial(self, dwg, col_idx, order):
        outer_x = [37, 566.51178, 1096.0236][col_idx]
        outer_y = 37
        outer_width = 529.13385
        outer_height = 340.15747
        outer_rx = 22.677166
        # Use shared SVG utility for outer rectangle
        dwg.add(draw_rounded_rect(
            dwg,
            insert=(outer_x, outer_y),
            size=(outer_width, outer_height),
            rx=outer_rx,
            ry=outer_rx,
            fill='none',
            stroke='#ff0000',
            stroke_width=0.377953
        ))
        photo_x = [75.842316, 605.35413, 1134.866][col_idx]
        photo_y = 77.060257
        photo_width = 190.02699
        photo_height = 260.03696
        photo_rx = 22.003126
        # Use shared SVG utility for black photo background
        dwg.add(draw_rounded_rect(
            dwg,
            insert=(photo_x, photo_y),
            size=(photo_width, photo_height),
            rx=photo_rx,
            ry=photo_rx,
            fill='#000000',
            stroke='none',
            stroke_width=0
        ))
        # Use shared SVG utility for blue outline
        dwg.add(draw_rounded_rect(
            dwg,
            insert=(photo_x, photo_y),
            size=(photo_width, photo_height),
            rx=photo_rx,
            ry=photo_rx,
            fill='none',
            stroke='#0000ff',
            stroke_width=0
        ))
        # Use shared SVG utility for photo border
        dwg.add(draw_rounded_rect(
            dwg,
            insert=(photo_x, photo_y),
            size=(photo_width, photo_height),
            rx=photo_rx,
            ry=photo_rx,
            fill='none',
            stroke='#000000',
            stroke_width=13.0018
        ))
        # Use shared SVG utility for magenta outline
        dwg.add(draw_rounded_rect(
            dwg,
            insert=(photo_x, photo_y),
            size=(photo_width, photo_height),
            rx=photo_rx,
            ry=photo_rx,
            fill='none',
            stroke='#ff00ff',
            stroke_width=0.377953
        ))

        if not pd.isna(order['image_path']) and order['image_path']:
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(script_dir, '..'))
            # Resolve image path
            # Normalize slashes in image_path for OS compatibility
            norm_image_path = os.path.normpath(order['image_path'])
            if os.path.isabs(norm_image_path):
                image_full_path = norm_image_path
            else:
                image_full_path = os.path.join(project_root, norm_image_path)
            print(f"[BWPhotoStakesProcessor] Resolved image_full_path: {image_full_path}")
            if os.path.exists(image_full_path):
                photo_data = self.embed_image(image_full_path)
                print(f"[BWPhotoStakesProcessor] embed_image returned: {bool(photo_data)}")
                if photo_data:
                    clip_id = f"photo_clip_{col_idx}"
                    clip_rect = dwg.rect(
                        insert=(photo_x, photo_y),
                        size=(photo_width, photo_height),
                        rx=photo_rx,
                        ry=photo_rx,
                        fill='none',
                        stroke='none'
                    )
                    dwg.defs.add(dwg.clipPath(id=clip_id).add(clip_rect))
                    dwg.add(dwg.image(
                        href=photo_data,
                        insert=(photo_x, photo_y),
                        size=(photo_width, photo_height),
                        clip_path=f'url(#{clip_id})'
                    ))
                else:
                    print(f"[BWPhotoStakesProcessor] Failed to embed image: {image_full_path}")
            else:
                print(f"[BWPhotoStakesProcessor] Image not found: {image_full_path}")

        # Add text with precise positioning and sizing
        text_lines = [order['line_1'], order['line_2'], order['line_3']]
        fill_color = '#000000'
        # Red border reference
        border_x = outer_x
        border_y = outer_y
        border_width = outer_width
        # --- Text layout logic adapted from photo_stakes.py ---
        # Calculate text area and center positions
        frame_x = outer_x + self.photo_left_margin_mm * self.px_per_mm
        frame_y = outer_y + (self.memorial_height_mm * self.px_per_mm - self.photo_height_px) / 2
        text_x = frame_x + self.photo_width_px + self.text_right_shift_px
        text_area_width = self.memorial_width_mm * self.px_per_mm - (text_x - outer_x) - self.text_right_shift_px
        text_center_x = text_x + text_area_width / 2

        # Use the same font sizes and vertical spacing as photo_stakes.py
        # (If you want to match photo_stakes.py exactly, you may want to use pt_to_mm as in that file)
        pt_to_mm = 0.352778
        # Line 1
        if not pd.isna(order['line_1']):
            line1_y = outer_y + (28 * self.px_per_mm)
            line1_font_size = 17 * pt_to_mm
            lines = split_line_to_fit(str(order['line_1']), 30)
            for idx, line in enumerate(lines):
                dy = 0 if idx == 0 else line1_font_size * 1.3
                dwg.add(add_multiline_text(
                    dwg,
                    [line],
                    insert=(text_center_x, line1_y + dy),
                    font_size=f"{line1_font_size}mm",
                    font_family="Georgia",
                    anchor="middle",
                    fill=fill_color
                ))
        # Line 2
        if not pd.isna(order['line_2']):
            line2_y = outer_y + (45 * self.px_per_mm)
            line2_font_size = 25 * pt_to_mm
            lines = split_line_to_fit(str(order['line_2']), 30)
            for idx, line in enumerate(lines):
                dy = 0 if idx == 0 else line2_font_size * 1.3
                dwg.add(add_multiline_text(
                    dwg,
                    [line],
                    insert=(text_center_x, line2_y + dy),
                    font_size=f"{line2_font_size}mm",
                    font_family="Georgia",
                    anchor="middle",
                    fill=fill_color
                ))
        # Line 3
        if not pd.isna(order['line_3']):
            base_y = outer_y + (57 * self.px_per_mm)
            line3_font_size = 12 * pt_to_mm
            lines = split_line_to_fit(order['line_3'], 30)
            for idx, line in enumerate(lines):
                dy = 0 if idx == 0 else line3_font_size * 1.3
                dwg.add(add_multiline_text(
                    dwg,
                    [line],
                    insert=(text_center_x, base_y + dy),
                    font_size=f"{line3_font_size}mm",
                    font_family="Georgia",
                    anchor="middle",
                    fill=fill_color
                ))

    def create_memorial_svg(self, orders, batch_num):
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        print(f"[BWPhotoStakesProcessor] Creating SVG: {filepath}")
        try:
            dwg = svgwrite.Drawing(
                filepath,
                size=("439.8mm", "289.9mm"),
                viewBox="0 0 1662.2362204933825 1095.6850393838827"
            )
            for col_idx, order in enumerate(orders):
                self.add_photo_memorial(dwg, col_idx, order)
            dwg.save()
            print(f"[BWPhotoStakesProcessor] SVG successfully written: {filepath}")
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"[BWPhotoStakesProcessor] ERROR: Failed to write SVG {filepath}\n{tb}")

    def process_orders(self, orders):
        print("\n[BW DEBUG] BWPhotoStakesProcessor.process_orders CALLED")
        if hasattr(orders, 'columns'):
            print("[BW DEBUG] Incoming DataFrame columns:", list(orders.columns))
        else:
            print("[BW DEBUG] 'orders' is not a DataFrame. Type:", type(orders))

        # Accept both DataFrame and list
        if isinstance(orders, list):
            df = pd.DataFrame(orders)
        else:
            df = orders.copy()
        df.columns = [col.lower() for col in df.columns]
        # Normalize relevant columns to lowercase and strip whitespace
        for col in ['type', 'colour', 'decorationtype']:
            if col in df.columns:
                df[col] = df[col].str.lower().str.strip()
        print("[BW DEBUG] DataFrame after normalization (head):")
        print(df.head())
        print("[BW DEBUG] Unique 'type':", df['type'].unique() if 'type' in df.columns else 'N/A')
        print("[BW DEBUG] Rows with non-empty image_path:", df[df['image_path'].notna() & (df['image_path'] != '')].shape[0])
        print("[BW DEBUG] Total rows before filtering:", len(df))

        # Stepwise filter debugging
        step1 = df[df['type'] == 'regular stake']
        print("[BW DEBUG] Rows after type=='regular stake':", len(step1))
        step2 = step1[step1['colour'] == 'black']
        print("[BW DEBUG] Rows after colour=='black':", len(step2))
        step3 = step2[step2['decorationtype'] == 'photo']
        print("[BW DEBUG] Rows after decorationtype=='photo':", len(step3))
        step4 = step3[step3['image_path'].notna() & (step3['image_path'] != '')]
        print("[BW DEBUG] Rows after image_path check:", len(step4))
        # Now use step4 as bw_stakes for further processing if needed
        # Use filtered DataFrame from above debug steps
        bw_photo_stakes = step4.copy()

        print(f"[BWPhotoStakesProcessor] Eligible orders found: {len(bw_photo_stakes)}")
        print(f"[BWPhotoStakesProcessor] Filtered columns: {list(bw_photo_stakes.columns)}")
        if bw_photo_stakes.empty:
            print(f"[BWPhotoStakesProcessor] WARNING: No eligible B&W photo stakes found. DataFrame columns: {list(df.columns)}")
            print(f"[BWPhotoStakesProcessor] DataFrame head:\n{df.head().to_string()}")
            return
        # Process in batches of 3 (top row)
        batch_num = 1
        for start_idx in range(0, len(bw_photo_stakes), 3):
            batch_orders = bw_photo_stakes.iloc[start_idx:start_idx + 3]
            if not batch_orders.empty:
        
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1

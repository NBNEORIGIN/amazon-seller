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
        # Determine if this is an attention order
        is_attention_order = False
        order_colour_lower = str(order.get('colour', '')).lower()
        order_type_lower = str(order.get('type', '')).lower()

        if order_colour_lower in ['marble', 'stone']:
            is_attention_order = True
        if order_type_lower == 'large plaque' or order_type_lower == 'regular plaque':
            is_attention_order = True

        is_om008016bw = (str(order.get('sku', '')).strip().upper() == 'OM008016BW')

        if is_om008016bw and self.d_clip_ellipse_om008016bw and self.d_border_om008016bw:
            # Specific logic for OM008016BW
            om_slot_group = dwg.g(transform=f"translate({x},{y})") # Slot position in pixels

            clip_path_id = f"omClip_{order.get('order-id', 'default').replace('-', '_').replace('.', '_')}_{int(x)}_{int(y)}"

            tx_g1_mm = -5.0270797
            ty_g1_mm = -86.4915987
            transform_g1_template_units_str = f"translate({tx_g1_mm},{ty_g1_mm})"

            if dwg.defs is None: dwg.defs = dwg.g()

            existing_clip_path = None
            # Check if clip_path_id already exists in defs to prevent duplicates
            if dwg.defs.elements:
                for el_val in dwg.defs.elements: # Simpler loop, no need for el_idx
                    if hasattr(el_val, 'attribs') and el_val.attribs.get('id') == clip_path_id:
                        existing_clip_path = el_val
                        break

            if not existing_clip_path:
                 # Apply scale transform directly to the clipPath element
                 clip_path_element = dwg.clipPath(id=clip_path_id, transform=f"scale({self.px_per_mm})")

                 # Create the path with its own translate transform
                 # (transform_g1_template_units_str was defined earlier in the original code)
                 path_for_clip = dwg.path(d=self.d_clip_ellipse_om008016bw, transform=transform_g1_template_units_str)

                 # Add the path directly to the clipPath element
                 clip_path_element.add(path_for_clip)
                 dwg.defs.add(clip_path_element)

            template_content_group = om_slot_group.add(dwg.g(transform=f"scale({self.px_per_mm})"))
            template_content_group.add(dwg.path(d=self.d_border_om008016bw, style="fill:#000000;stroke:none;", transform=transform_g1_template_units_str))

            photo_path_str = str(order.get('photo_path', ''))
            if photo_path_str and not pd.isna(photo_path_str):
                actual_photo_path = photo_path_str
                if not os.path.isabs(photo_path_str):
                    actual_photo_path = os.path.join(self.graphics_path, photo_path_str.replace('\\', os.sep))
                if os.path.exists(actual_photo_path):
                    photo_data = self.embed_image(actual_photo_path)
                    if photo_data:
                        img_x_mm, img_y_mm, img_width_mm, img_height_mm = 15.1252413, 16.4017223, 67.046234, 87.148118
                        photo_image = dwg.image(href=photo_data, insert=(f"{img_x_mm}mm", f"{img_y_mm}mm"), size=(f"{img_width_mm}mm", f"{img_height_mm}mm"))
                        photo_image.attribs['clip-path'] = f'url(#{clip_path_id})'
                        template_content_group.add(photo_image)
                    else: print(f"Failed to embed photo for OM008016BW: {actual_photo_path}")
                else: print(f"Warning: Photo not found for OM008016BW at {actual_photo_path}")
            else: print(f"Warning: No photo_path provided for OM008016BW, order ID: {order.get('order-id', 'N/A')}")

            rect_x_mm, rect_y_mm, rect_width_mm, rect_height_mm, rect_ry_mm, rect_stroke_width_mm = 0.05, 0.05, 199.90007, 119.90007, 5.9950037, 0.0999334
            om_stroke_color = 'yellow' if is_attention_order else '#ff0000'
            template_content_group.add(dwg.rect(insert=(f"{rect_x_mm}mm", f"{rect_y_mm}mm"), size=(f"{rect_width_mm}mm", f"{rect_height_mm}mm"), ry=f"{rect_ry_mm}mm", style=f"fill:none;stroke:{om_stroke_color};stroke-width:{rect_stroke_width_mm}mm"))
            dwg.add(om_slot_group)

        else:
            # Original logic for other SKUs, with conditional stroke and corrected dimension variables
            default_other_stroke_color = 'yellow' if is_attention_order else 'black'

            dwg.add(draw_rounded_rect(
                dwg,
                insert=(x, y),
                size=(self.memorial_width_px_default, self.memorial_height_px_default),
                rx=self.corner_radius_px_default,
                ry=self.corner_radius_px_default,
                fill='none',
                stroke=default_other_stroke_color,
                stroke_width=1
            ))

            frame_x = x + self.photo_left_margin_px_orig
            frame_y = y + (self.memorial_height_px_default - self.photo_height_px_orig) / 2

            clip_x = frame_x + (self.photo_width_px_orig - self.photo_clip_width_px_orig) / 2
            clip_y = frame_y + (self.photo_height_px_orig - self.photo_clip_height_px_orig) / 2

            text_x_for_blue_rect = frame_x + self.photo_width_px_orig + self.text_right_shift_px_orig
            text_area_width_for_blue_rect = self.memorial_width_px_default - (text_x_for_blue_rect - x) - self.text_right_shift_px_orig
            text_center_x_for_blue_rect = text_x_for_blue_rect + text_area_width_for_blue_rect / 2 - (self.photo_clip_width_px_orig / 2)
            text_center_y_for_blue_rect = y + (28 * self.px_per_mm)

            dwg.add(draw_rounded_rect(
                dwg,
                insert=(clip_x, clip_y),
                size=(self.photo_clip_width_px_orig, self.photo_clip_height_px_orig),
                rx=self.photo_corner_radius_px_orig,
                ry=self.photo_corner_radius_px_orig,
                fill='black',
                stroke='none',
                stroke_width=0
            ))

            clip_rect = dwg.rect(
                insert=(clip_x, clip_y),
                size=(self.photo_clip_width_px_orig, self.photo_clip_height_px_orig),
                rx=self.photo_corner_radius_px_orig,
                ry=self.photo_corner_radius_px_orig,
                fill='none',
                stroke='none'
            )

            if dwg.defs is None:
                dwg.defs = dwg.g()

            clip_path_id_non_om = f'clip_{x}_{y}'
            existing_clip_path_orig = None
            if dwg.defs.elements:
                for el_idx_loop, el_val in enumerate(dwg.defs.elements):
                    if el_val.attribs.get('id') == clip_path_id_non_om:
                        existing_clip_path_orig = el_val
                        break
            if not existing_clip_path_orig:
                clip_path = dwg.defs.add(dwg.clipPath(id=clip_path_id_non_om))
                clip_path.add(clip_rect)

            dwg.add(dwg.rect(
                insert=(text_center_x_for_blue_rect, text_center_y_for_blue_rect),
                size=(self.photo_clip_width_px_orig, self.photo_clip_height_px_orig),
                rx=self.photo_corner_radius_px_orig,
                ry=self.photo_corner_radius_px_orig,
                fill='none',
                stroke='blue',
                stroke_width=self.photo_outline_stroke_px_orig
            ))

            dwg.add(dwg.rect(
                insert=(frame_x, frame_y),
                size=(self.photo_width_px_orig, self.photo_height_px_orig),
                rx=self.photo_corner_radius_px_orig,
                ry=self.photo_corner_radius_px_orig,
                fill='none',
                stroke='black',
                stroke_width=self.photo_border_stroke_px_orig
            ))

            photo_path_str = str(order.get('photo_path', ''))
            if photo_path_str and not pd.isna(photo_path_str):
                actual_photo_path = photo_path_str
                if not os.path.isabs(photo_path_str):
                    actual_photo_path = os.path.join(self.graphics_path, photo_path_str.replace('\\', os.sep))

                if os.path.exists(actual_photo_path):
                    photo_data = self.embed_image(actual_photo_path)
                    if photo_data:
                        photo = dwg.image(
                            href=photo_data,
                            insert=(frame_x, frame_y),
                            size=(self.photo_width_px_orig, self.photo_height_px_orig),
                            clip_path=f'url(#{clip_path_id_non_om})'
                        )
                        dwg.add(photo)
                    else:
                        print(f"Failed to embed photo for SKU {order.get('sku')}")
                else:
                    print(f"Warning: Photo not found at {actual_photo_path} for SKU {order.get('sku')}")
            else:
                print(f"Warning: No photo_path for SKU {order.get('sku')}")
        
            text_x_final = frame_x + self.photo_width_px_orig + self.text_right_shift_px_orig
            text_area_width_final = self.memorial_width_px_default - (text_x_final - x) - self.text_right_shift_px_orig
            text_center_x_final = text_x_final + text_area_width_final / 2

            # pt_to_px = self.pt_to_mm * self.px_per_mm # Not needed directly if font_size in mm and dy in px

            if not pd.isna(order.get('line_1')):
                line1_y_px = y + (28 * self.px_per_mm) # Base y for line 1
                lines = split_line_to_fit(str(order.get('line_1','')), 30)
                line_height_px_l1 = self.line1_size_pt * self.pt_to_mm * self.px_per_mm * 1.3
                for i, line_text in enumerate(lines):
                    dy_px_line1 = i * line_height_px_l1
                    dwg.add(add_multiline_text(
                        dwg,
                        [line_text], # Pass list with single line
                        insert=(text_center_x_final, line1_y_px + dy_px_line1), # Use text_center_x_final
                        font_size=f"{self.line1_size_pt * self.pt_to_mm}mm",
                        font_family="Georgia",
                        anchor="middle",
                        fill="black"
                    ))

            if not pd.isna(order.get('line_2')):
                line2_y_px = y + (45 * self.px_per_mm) # Base y for line 2
                lines = split_line_to_fit(str(order.get('line_2','')), 30)
                line_height_px_l2 = self.line2_size_pt * self.pt_to_mm * self.px_per_mm * 1.3
                for idx, line in enumerate(lines):
                    dy_px_line2 = idx * line_height_px_l2
                    dwg.add(add_multiline_text(
                        dwg,
                        [line], # Pass list with single line
                        insert=(text_center_x_final, line2_y_px + dy_px_line2), # Use text_center_x_final
                        font_size=f"{self.line2_size_pt * self.pt_to_mm}mm",
                        font_family="Georgia",
                        anchor="middle",
                        fill="black"
                    ))

            if not pd.isna(order.get('line_3')):
                base_y_px = y + (57 * self.px_per_mm) # Base y for line 3
                lines = split_line_to_fit(str(order.get('line_3','')), 30)
                line3_size_pt = 12 # Assuming 12pt for line 3 as per original dy calculation
                line_height_px_l3 = line3_size_pt * self.pt_to_mm * self.px_per_mm * 1.3
                for idx, line in enumerate(lines):
                    dy_px_line3 = idx * line_height_px_l3
                    dwg.add(add_multiline_text(
                        dwg,
                        [line], # Pass list with single line
                        insert=(text_center_x_final, base_y_px + dy_px_line3), # Use text_center_x_final
                        font_size=f"{line3_size_pt * self.pt_to_mm}mm",
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
        # --- Start Diagnostic Logging for Order 203-1227886-3288363 ---
        target_order_id = '203-1227886-3288363'
        # Ensure 'order-id' column exists before trying to filter
        if 'order-id' in df.columns:
            target_order_df = df[df['order-id'] == target_order_id]

            if not target_order_df.empty:
                print(f"\n[DIAGNOSTIC] Data for order {target_order_id} BEFORE filtering in BWLargePhotoStakesProcessor:")
                target_order_data = target_order_df.iloc[0].to_dict() # Convert Series to dict
                for key, value in target_order_data.items():
                    print(f"  {key}: '{value}' (type: {type(value)})" )

                print(f"\n[DIAGNOSTIC] Filter conditions for order {target_order_id} in BWLargePhotoStakesProcessor:")

                # Condition 1: Colour
                cond1_colour_val = str(target_order_data.get('colour', '')).lower() # Ensure string for .lower()
                cond1_met = (cond1_colour_val == 'black')
                print(f"  1. df['colour'].str.lower() == 'black': Applied as ('{cond1_colour_val}' == 'black') -> {cond1_met}")

                # Condition 2: Type
                cond2_type_val = str(target_order_data.get('type', '')) # Ensure string for .lower()
                cond2_type_contains_large_stake = False
                if pd.notna(cond2_type_val): # Check if Series first, then apply .str methods
                     cond2_type_contains_large_stake = 'large stake' in cond2_type_val.lower()
                cond2_met = cond2_type_contains_large_stake
                print(f"  2. df['type'].str.contains('large stake', case=False, na=False): Applied as ('{cond2_type_val}'.lower() contains 'large stake') -> {cond2_met}")

                # Condition 3: DecorationType
                cond3_deco_val = str(target_order_data.get('decorationtype', '')).lower() # Ensure string for .lower()
                cond3_met = (cond3_deco_val == 'photo')
                print(f"  3. df['decorationtype'].str.lower() == 'photo': Applied as ('{cond3_deco_val}' == 'photo') -> {cond3_met}")

                # Condition 4: Photo Path
                cond4_path_val = target_order_data.get('photo_path', None)
                cond4_path_notna = pd.notna(cond4_path_val)
                cond4_path_notempty = False
                if cond4_path_notna and isinstance(cond4_path_val, str): # Check type before .strip()
                    cond4_path_notempty = cond4_path_val.strip() != ''
                elif cond4_path_notna: # Not a string but notna (e.g. if it was a number by mistake)
                     cond4_path_notempty = True

                cond4_met = cond4_path_notna and cond4_path_notempty
                print(f"  4. df['photo_path'].notna() AND df['photo_path'] != '': Value '{cond4_path_val}' -> notna={cond4_path_notna}, notempty_if_str_or_true_if_not_str={cond4_path_notempty} -> {cond4_met}")

                overall_should_be_eligible = cond1_met and cond2_met and cond3_met and cond4_met
                print(f"  Overall, should this order be eligible based on individual checks? {overall_should_be_eligible}\n")

            else:
                print(f"\n[DIAGNOSTIC] Order {target_order_id} not found in DataFrame in BWLargePhotoStakesProcessor prior to its specific filtering.\n")
        else:
            print(f"\n[DIAGNOSTIC] 'order-id' column not found in DataFrame in BWLargePhotoStakesProcessor. Cannot check for target_order_id.\n")
        # --- End Diagnostic Logging ---
        large_photo_stakes = df[
            (df['colour'].str.lower() == 'black') & 
            (df['type'].str.contains('large stake', case=False, na=False)) &
            (df['decorationtype'].str.lower() == 'photo') &
            (df['photo_path'].notna() & (df['photo_path'].astype(str).str.strip() != '')) # Ensured non-empty check and astype(str)
        ].copy()
        # Process in batches of 2
        batch_num = 1
        for start_idx in range(0, len(large_photo_stakes), 2):
            batch_orders = large_photo_stakes.iloc[start_idx:start_idx + 2]
            if not batch_orders.empty:
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1
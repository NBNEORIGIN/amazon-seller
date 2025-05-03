import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd
import textwrap
import re
from datetime import datetime
from pathlib import Path

class RegularStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'COLOUR'
        self.grid_cols = 3
        self.grid_rows = 3
        self.batch_size = self.grid_cols * self.grid_rows

        # Conversion factors
        self.px_per_mm = 1 / 0.26458333333
        self.pt_to_mm = 0.2645833333

        # Memorial and page dimensions
        self.memorial_width_mm = 140
        self.memorial_height_mm = 90
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.memorial_width_px = int(self.memorial_width_mm * self.px_per_mm)
        self.memorial_height_px = int(self.memorial_height_mm * self.px_per_mm)
        self.page_width_px = int(self.page_width_mm * self.px_per_mm)
        self.page_height_px = int(self.page_height_mm * self.px_per_mm)

        # Centering offsets
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows
        self.x_offset_mm = (self.page_width_mm - grid_width_mm) / 2
        self.y_offset_mm = (self.page_height_mm - grid_height_mm) / 2
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

        # Text sizes (in points)
        self.line1_size_pt = 17 * 1.2  # Increased by 20%
        self.line2_size_pt = 25 * 1.2
        self.line3_size_pt = 12 * 1.1

        # Stroke width and corner radius
        self.stroke_width = 0.1 * self.px_per_mm
        self.corner_radius_px = 6 * self.px_per_mm

    def check_grammar_and_typos(self, order):
        # a. Spaces before commas or periods
        for key in ['line_1', 'line_2', 'line_3']:
            value = order.get(key, "")
            value = "" if value is None or (isinstance(value, float) and pd.isna(value)) else str(value)
            if value and re.search(r"\s+[,\.]", value):
                print(f"Warning: Extra space before comma/period in {key}: '{value}'")

        # b. Future death dates (try to find DD/MM/YYYY or MM/DD/YYYY)
        date_pattern = r'(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)'
        for key in ['line_1', 'line_2', 'line_3']:
            value = order.get(key, "")
            value = "" if value is None or (isinstance(value, float) and pd.isna(value)) else str(value)
            if value:
                for match in re.findall(date_pattern, value):
                    # ...
                    try:
                        # Try UK format first (DD/MM/YYYY)
                        dt = datetime.strptime(match, "%d/%m/%Y")
                    except ValueError:
                        try:
                            # Try US format (MM/DD/YYYY)
                            dt = datetime.strptime(match, "%m/%d/%Y")
                        except ValueError:
                            continue
                    if dt.year > datetime.now().year:
                        print(f"Warning: Future year found in {key}: '{match}' in '{order[key]}'")

        # c. Capitalization of names (LINE_1 and LINE_2)
        for key in ['line_1', 'line_2']:
            value = order.get(key, "")
            value = "" if value is None or (isinstance(value, float) and pd.isna(value)) else str(value)
            if value and not value.istitle():
                print(f"Warning: Name not title case in {key}: '{value}'")

    def process_orders(self, orders):
        if isinstance(orders, list):
            df = pd.DataFrame(orders)
        else:
            df = orders.copy()

        df.columns = [col.lower() for col in df.columns]
        df['type'] = df['type'].str.strip().str.lower()
        df['colour'] = df['colour'].str.strip().str.lower()

        print(f"Columns after normalization: {list(df.columns)}")
        print(df.head())

        # Expand rows by number-of-items
        expanded_rows = []
        for _, row in df.iterrows():
            try:
                qty = int(row.get('number-of-items', 1))
                qty = max(qty, 1)
            except Exception:
                qty = 1
            for _ in range(qty):
                expanded_rows.append(row.copy())
        df_expanded = pd.DataFrame(expanded_rows)

        allowed_colours = ['copper', 'gold', 'silver', 'marble', 'stone']
        filtered = df_expanded[
            (
                (df_expanded['type'].str.contains('regular stake', na=False)) &
                (df_expanded['colour'].isin(allowed_colours))
            ) |
            (df_expanded['type'].str.contains('regular plaque', na=False)) |
            (df_expanded['sku'].astype(str).str.upper() == 'OM008021')
        ].copy()

        color_priority = {'copper': 0, 'gold': 1, 'silver': 2, 'stone': 3, 'marble': 4}
        filtered['color_priority'] = filtered['colour'].map(color_priority)
        filtered = filtered.sort_values('color_priority')

        # --- Exclude photo SKUs based on SKULIST.csv ---
        skulist_path = r'G:/My Drive/003 APPS/002 AmazonSeller/001 AMAZON DATA DOWNLOAD/SKULIST.csv'
        skulist_df = pd.read_csv(skulist_path)
        skulist_df.columns = [col.lower() for col in skulist_df.columns]
        photo_skus = set(skulist_df[(skulist_df['type'].str.lower().isin(['regular stake', 'regular plaque'])) & (skulist_df['graphic'].str.lower() == 'photo')]['sku'].str.strip())
        before = len(filtered)
        filtered = filtered[(filtered['type'].str.lower().isin(['regular stake', 'regular plaque'])) & (~filtered['sku'].isin(photo_skus))]
        print(f"Filtered out {before - len(filtered)} photo stakes from regular stake processing (by photo SKU list).")
        print(f"Sample regular stakes: {filtered[['order-id', 'sku', 'graphic']].head()}")

        print(f"\nFiltered columns: {list(filtered.columns)}")
        print(filtered.head())
        print(f"\nFound {len(filtered)} Regular Stakes (copper/gold/silver)")

        batch_num = 1
        total = len(filtered)
        for start_idx in range(0, total, self.batch_size):
            end_idx = min(start_idx + self.batch_size, total)
            batch_orders = filtered.iloc[start_idx:end_idx]
            print(f"\nProcessing Regular Stake batch {batch_num}: rows {start_idx} to {end_idx-1} (batch size: {len(batch_orders)})")
            if not batch_orders.empty:
                orders_dict = batch_orders.to_dict('records')
                print(f"Batch {batch_num} first order text fields: line_1={orders_dict[0].get('line_1')}, line_2={orders_dict[0].get('line_2')}, line_3={orders_dict[0].get('line_3')}")
                self.create_memorial_svg(orders_dict, batch_num)
                self.create_batch_csv(orders_dict, batch_num, self.CATEGORY)
                batch_num += 1

    def split_line_to_fit(self, line, max_chars):
        # Split a single line into lines that fit max_chars
        return textwrap.wrap(line, width=max_chars)

    def create_memorial_svg(self, orders, batch_num):
        if orders:
            print(f"Batch {batch_num} first order text fields: line_1={orders[0].get('line_1')}, line_2={orders[0].get('line_2')}, line_3={orders[0].get('line_3')}")
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        output_path = os.path.join(self.OUTPUT_DIR, filename)

        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )

        for idx in range(self.batch_size):
            row = idx // self.grid_cols
            col = idx % self.grid_cols

            x = self.x_offset_px + (col * self.memorial_width_px)
            y = self.y_offset_px + (row * self.memorial_height_px)

            dwg.add(dwg.rect(
                insert=(x, y),
                size=(self.memorial_width_px, self.memorial_height_px),
                rx=6*self.px_per_mm,
                ry=6*self.px_per_mm,
                fill='none',
                stroke='red',
                stroke_width=0.1*self.px_per_mm
            ))

            if idx < len(orders):
                order = orders[idx]
                self.check_grammar_and_typos(order)

                # Special handling for OM008021 graphic
                if str(order.get('sku', '')).upper() == 'OM008021':
                    graphic_path = r'G:/My Drive/001 NBNE/001 M/M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM/001 Design/002 MUTOH/002 AUTODESIGN/OM008021.png'
                    print(f"Using special graphic for OM008021: {graphic_path}")
                    if os.path.exists(graphic_path):
                        embedded_image = self.embed_image(graphic_path)
                        if embedded_image:
                            dwg.add(dwg.image(
                                href=embedded_image,
                                insert=(x, y),
                                size=(self.memorial_width_px, self.memorial_height_px)
                            ))
                        else:
                            print(f"Failed to embed OM008021 graphic")
                    else:
                        print(f"Warning: OM008021 graphic not found: {graphic_path}")
                elif order.get('graphic'):
                    graphic_path = os.path.join(self.graphics_path, str(order['graphic']))
                    print(f"Looking for graphic: {graphic_path}")
                    if os.path.exists(graphic_path):
                        print(f"Found graphic: {graphic_path}")
                        embedded_image = self.embed_image(graphic_path)
                        if embedded_image:
                            dwg.add(dwg.image(
                                href=embedded_image,
                                insert=(x, y),
                                size=(self.memorial_width_px, self.memorial_height_px)
                            ))
                        else:
                            print(f"Failed to embed graphic")
                    else:
                        print(f"Warning: Graphic not found: {graphic_path}")

                center_x = x + (self.memorial_width_px / 2)

                # Handle text lines with improved nan checking
                for line_num, (key, y_pos, font_size) in enumerate([
                    ('line_1', 28, self.line1_size_pt),
                    ('line_2', 45, self.line2_size_pt)
                ]):
                    value = order.get(key)
                    if value is not None and not (isinstance(value, float) and pd.isna(value)):
                        dwg.add(dwg.text(
                            str(value),
                            insert=(center_x, y + (y_pos * self.px_per_mm)),
                            font_size=f"{font_size * self.pt_to_mm}mm",
                            font_family="Georgia",
                            text_anchor="middle",
                            fill="black"
                        ))
                    else:
                        print(f"Warning: Missing text in {key} for order {order.get('order_id', 'Unknown')}")

                # Improved handling for LINE_3 (text box logic with tspan and robust line spacing)
                value = order.get('line_3')
                if value is not None and not (isinstance(value, float) and pd.isna(value)):
                    line3_text = str(value).strip()
                    if line3_text:  # Only process if there's actual text
                        lines = line3_text.split('\n')
                        font_mm = self.line3_size_pt * self.pt_to_mm
                        char_width_mm = 0.5 * font_mm
                        max_line_mm = self.memorial_width_mm * 0.6
                        max_chars = int(max_line_mm / char_width_mm)
                        split_lines = []
                        for l in lines:
                            if l.strip():  # Only process non-empty lines
                                split_lines.extend(self.split_line_to_fit(l, max_chars))
                        
                        if split_lines:  # Only continue if we have lines to display
                            if len(split_lines) == 1:
                                split_lines = textwrap.wrap(split_lines[0], width=30)
                            split_lines = split_lines[:5]
                            
                            # --- Conditional font size logic for Line 3 ---
                            total_chars = sum(len(line) for line in split_lines)
                            if 10 <= total_chars <= 30:
                                line3_font_size_pt = self.line1_size_pt
                            elif 31 <= total_chars <= 90:
                                line3_font_size_pt = self.line1_size_pt * 0.9
                            else:
                                line3_font_size_pt = self.line3_size_pt

                            # SVG <text> with <tspan>s for each line, robust line spacing
                            line3_text_element = dwg.text(
                                "",
                                insert=(center_x, y + (57 * self.px_per_mm)),
                                font_size=f"{line3_font_size_pt * self.pt_to_mm}mm",
                                font_family="Georgia",
                                text_anchor="middle",
                                fill="black"
                            )
                            for line_idx, line in enumerate(split_lines):
                                # For all lines after the first, use 1.2em for robust line spacing
                                if line_idx == 0:
                                    dy_val = "0"
                                else:
                                    dy_val = "1.2em"
                                tspan = dwg.tspan(
                                    line.strip(),
                                    x=[center_x],
                                    dy=[dy_val]
                                )
                                line3_text_element.add(tspan)
                            dwg.add(line3_text_element)
                else:
                    print(f"Warning: Missing text in LINE_3 for order {order.get('ORDER_ID', 'Unknown')}")

        # Add reference point (0.1mm blue square) in bottom right corner
        ref_size_px = 0.1 * self.px_per_mm
        x_pos = self.page_width_px - ref_size_px
        y_pos = (self.page_height_mm - 0.011) * self.px_per_mm - ref_size_px

        dwg.add(dwg.rect(
            insert=(x_pos, y_pos),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))

        dwg.save()
        return dwg

    import sys

if __name__ == "__main__":
    # Usage: python regular_stakes.py <output_dir> <graphics_path>
    import sys
    import pandas as pd
    import os
    from pathlib import Path

    output_dir = sys.argv[1] if len(sys.argv) > 1 else "SVG_OUTPUT"
    graphics_path = sys.argv[2] if len(sys.argv) > 2 else "G:/My Drive/001 NBNE/001 M/M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM/001 Design/002 MUTOH/002 AUTODESIGN"

    orders_txt = str(Path(__file__).parent.parent / "001 AMAZON DATA DOWNLOAD" / "output.txt")
    if not os.path.exists(orders_txt):
        print(f"Error: {orders_txt} does not exist. Please run order processing first.")
        sys.exit(1)

    orders = pd.read_csv(orders_txt, sep='\t', encoding='utf-8')
    print(f"Loaded columns: {list(orders.columns)}")
    print(orders.head())
    processor = RegularStakesProcessor(graphics_path, output_dir)
    processor.process_orders(orders)
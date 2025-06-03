import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd

class BWLargeStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'B&W_LARGE_STAKES'
        
        # SVG dimensions (from correct output)
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.viewbox_width = 1662
        self.viewbox_height = 1095
        
        # Memorial dimensions (exact from SVG)
        self.memorial_width_px = 755.42004
        self.memorial_height_px = 453.1008
        self.corner_radius_px = 22.012239
        self.stroke_width = 0.378046
        
        # Text sizes (from SVG)
        self.line1_size_pt = 45.3333  # "In Loving Memory Of"
        self.line2_size_pt = 66.6667  # Name
        self.line3_size_pt = 32       # Additional lines
        
        # Position of first memorial (from SVG)
        self.x_offset_px = 150.59283
        self.y_offset_px = 641.97479
        
        # Memorial spacing (from SVG)
        self.memorial_spacing_x_px = 755.79810  # Distance between memorials
        
        # Calculate grid layout
        self.grid_cols = 2
        self.grid_rows = 1

    def add_memorial(self, dwg, x, y, order):
        # Create the memorial rectangle (red cut line)
        rect = dwg.rect(
            insert=(x, y),
            size=(self.memorial_width_px, self.memorial_height_px),
            rx=self.corner_radius_px,
            ry=self.corner_radius_px,
            fill='none',
            stroke='#ff0000',
            stroke_width=self.stroke_width
        )
        dwg.add(rect)

        # Draw blue face outline (from template, using same size/position as memorial for now)
        blue_face = dwg.rect(
            insert=(x, y),
            size=(self.memorial_width_px, self.memorial_height_px),
            rx=self.corner_radius_px,
            ry=self.corner_radius_px,
            fill='none',
            stroke='#0000ff',
            stroke_width=self.stroke_width
        )
        dwg.add(blue_face)

        # Center X for text/graphics
        center_x = x + (self.memorial_width_px / 2)
        # Y positions for text (from user description, adjust as needed)
        line1_y = y + 29 / self.page_height_mm * self.viewbox_height  # 29mm from top of blue face
        line2_y = y + (self.memorial_height_px / 2)                  # Centered vertically
        line3_y = y + self.memorial_height_px - (29 / self.page_height_mm * self.viewbox_height)  # 29mm from bottom

        # --- Graphics embedding (if present) ---
        if 'graphic' in order and pd.notna(order['graphic']) and str(order['graphic']).strip() != '':
            graphic_path = os.path.join(self.graphics_path, str(order['graphic']))
            if os.path.exists(graphic_path):
                embedded_image = self.embed_image(graphic_path)
                if embedded_image:
                    dwg.add(dwg.image(
                        href=embedded_image,
                        insert=(x, y),
                        size=(self.memorial_width_px, self.memorial_height_px)
                    ))
                else:
                    print(f"[WARNING] Failed to embed graphic for order {order.get('order-id', '')}: {graphic_path}")
            else:
                print(f"[WARNING] Graphic file not found for order {order.get('order-id', '')}: {graphic_path}")
        else:
            print(f"[WARNING] No graphic specified for order {order.get('order-id', '')} (SKU: {order.get('sku', '')})")

        # --- Line 1 ---
        if not pd.isna(order['line_1']):
            dwg.add(dwg.text(
                str(order['line_1']),
                insert=(center_x, line1_y),
                font_family="Georgia",
                font_size=f"{self.line1_size_pt}px",
                fill="black",
                text_anchor="middle"
            ))
        # --- Line 2 ---
        if not pd.isna(order['line_2']):
            dwg.add(dwg.text(
                str(order['line_2']),
                insert=(center_x, line2_y),
                font_family="Georgia",
                font_size=f"{self.line2_size_pt}px",
                fill="black",
                text_anchor="middle"
            ))
        # --- Line 3 ---
        if not pd.isna(order['line_3']):
            lines = self.wrap_text(str(order['line_3']))
            current_y = line3_y
            line_spacing = 47.11817    # Spacing between lines, adjust as needed
            for line in lines:
                dwg.add(dwg.text(
                    line.strip(),
                    insert=(center_x, current_y),
                    font_family="Georgia",
                    font_size=f"{self.line3_size_pt}px",
                    fill="black",
                    text_anchor="middle"
                ))
                current_y += line_spacing

    def create_memorial_svg(self, orders, batch_num, output_path=None):
        if output_path is None:
            filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
            filepath = os.path.join(self.OUTPUT_DIR, filename)
        else:
            filepath = output_path
        # Create SVG with exact dimensions from sample
        dwg = svgwrite.Drawing(
            filepath,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.viewbox_width} {self.viewbox_height}"
        )
        
        # Process each order
        for idx, order in enumerate(orders):
            if idx >= 2:  # Only process 2 memorials
                break
                
            # Calculate position
            col = idx % self.grid_cols
            x = self.x_offset_px + (col * self.memorial_spacing_x_px)
            y = self.y_offset_px
            
            self.add_memorial(dwg, x, y, order)
        
        # Add reference point (blue pixel in bottom right)
        dwg.add(dwg.rect(
            insert=(1661.6220472, 1094.8876867919998),
            size=(0.37795280000000003, 0.37795280000000003),
            fill="blue"
        ))
        
        dwg.save()

    def process_orders(self, df):
        # Filter for B&W large stakes with graphics
        allowed_colours = ['black', 'slate']
        df['type'] = df['type'].astype(str).str.strip().str.lower()
        df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        df['decorationtype'] = df['decorationtype'].astype(str).str.strip().str.lower()
        # Enhanced diagnostics
        print("Unique values in 'type':", df['type'].unique())
        print("Unique values in 'colour':", df['colour'].unique())
        print("Unique values in 'decorationtype':", df['decorationtype'].unique())
        print("Sample graphic values:", df['graphic'].head(10).tolist())
        # Show why rows are excluded
        for idx, row in df.iterrows():
            reasons = []
            if row['type'] != 'large stake':
                reasons.append(f"type={row['type']}")
            if row['colour'] not in allowed_colours:
                reasons.append(f"colour={row['colour']}")
            if row['decorationtype'] != 'graphic':
                reasons.append(f"decorationtype={row['decorationtype']}")
            if reasons:
                print(f"Row {idx} excluded: {', '.join(reasons)}")
        large_stakes = df[
            (df['type'] == 'large stake') &
            (df['colour'].isin(allowed_colours)) &
            (df['decorationtype'] == 'graphic')
        ].copy()
        print(f"Rows after filtering for Large Stake, black/slate, and DecorationType == 'graphic': {len(large_stakes)}")
        print(large_stakes[['order-id', 'sku', 'colour', 'decorationtype']].head() if not large_stakes.empty else large_stakes.head())
        if large_stakes.empty:
            print("No eligible B&W large stakes found for bw_large_stakes.py processor.")
            return
        # Process in batches of 2
        batch_size = 2
        for batch_num, batch_start in enumerate(range(0, len(large_stakes), batch_size), 1):
            batch = large_stakes.iloc[batch_start:batch_start + batch_size]
            print(f"[DEBUG] Processing B&W Large Stake batch {batch_num}: {len(batch)} rows")
            print(batch[['order-id','type','colour','decorationtype']].head())
            self.create_memorial_svg(batch.to_dict('records'), batch_num)
            print(f"[BWLargeStakesProcessor] Writing batch CSV for batch {batch_num} to output directory {self.OUTPUT_DIR}")
            try:
                self.create_batch_csv(batch.to_dict('records'), batch_num, self.CATEGORY)
                print(f"[BWLargeStakesProcessor] Successfully wrote batch CSV for batch {batch_num}")
            except Exception as e:
                print(f"[BWLargeStakesProcessor] ERROR: Failed to write batch CSV for batch {batch_num}: {e}")

        # Export CSV for processed large stakes
        print(f"[DEBUG] large_stakes DataFrame has {len(large_stakes)} rows before CSV export.")
        if not large_stakes.empty:
            print("[DEBUG] large_stakes head before CSV export:")
            print(large_stakes.head())
            # Ensure output directory exists
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)
            csv_filename = os.path.join(self.OUTPUT_DIR, f"{self.CATEGORY}_{self.date_str}.csv")
            large_stakes.to_csv(csv_filename, index=False)
            print(f"Exported B&W Large Stakes CSV: {csv_filename} ({len(large_stakes)} rows)")
        else:
            print("No B&W Large Stakes to export to CSV.")
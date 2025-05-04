import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd

class ColouredLargeStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'COLOURED_LARGE_STAKES'
        # SVG/page dimensions (from codebase conventions)
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.viewbox_width = 1662
        self.viewbox_height = 1095
        # Memorial geometry (from SVG)
        self.memorial_width_px = 755.42004
        self.memorial_height_px = 453.1008
        self.corner_radius_px = 22.012239
        self.stroke_width = 0.378046
        # Text sizes (from SVG or design)
        self.line1_size_pt = 45.33  # e.g. "In Loving Memory Of"
        self.line2_size_pt = 66.67  # Name
        self.line3_size_pt = 32     # Additional lines
        # Grid layout (2x2)
        self.grid_cols = 2
        self.grid_rows = 2
        self.batch_size = self.grid_cols * self.grid_rows
        # Offsets and spacing (from SVG)
        self.x_offset_px = 150.59
        self.y_offset_px = 641.97
        self.memorial_spacing_x_px = 755.80
        self.memorial_spacing_y_px = 453.10

    def process_orders(self, df):
        # Filter for coloured large stakes
        filtered = df[
            (df['TYPE'].str.contains('Large Stake', case=False, na=False)) &
            (df['COLOUR'].str.lower().isin(['copper', 'gold', 'silver']))
        ].copy()

        batch_num = 1
        for start_idx in range(0, len(filtered), self.batch_size):
            batch_orders = filtered.iloc[start_idx:start_idx + self.batch_size]
            if not batch_orders.empty:
                print(f"\nProcessing Coloured Large Stake batch {batch_num}...")
                orders_dict = batch_orders.to_dict('records')
                self.create_memorial_svg(orders_dict, batch_num)
                self.create_batch_csv(orders_dict, batch_num, self.CATEGORY)
                batch_num += 1

    def create_memorial_svg(self, orders, batch_num):
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        print(f"Creating SVG file: {filepath}")
        dwg = svgwrite.Drawing(
            filepath,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.viewbox_width} {self.viewbox_height}"
        )
        positions = [
            # bottom right, bottom left, top right, top left
            (self.x_offset_px + self.memorial_spacing_x_px, self.y_offset_px),
            (self.x_offset_px, self.y_offset_px),
            (self.x_offset_px + self.memorial_spacing_x_px, self.y_offset_px - self.memorial_spacing_y_px),
            (self.x_offset_px, self.y_offset_px - self.memorial_spacing_y_px),
        ]
        for idx, order in enumerate(orders):
            if idx >= 4:
                break
            x, y = positions[idx]
            print(f"Adding memorial {idx+1} at position ({x}, {y})")
            self.add_memorial(dwg, x, y, order)
        # Add reference point (blue pixel in bottom right)
        dwg.add(dwg.rect(
            insert=(self.viewbox_width - 0.38, self.viewbox_height - 0.38),
            size=(0.38, 0.38),
            fill="blue"
        ))
        print(f"Saving SVG file to: {filepath}")
        dwg.save()
        print(f"SVG file saved successfully")

    def add_memorial(self, dwg, x, y, order):
        # Draw rounded rectangle for the memorial
        dwg.add(dwg.rect(
            insert=(x, y),
            size=(self.memorial_width_px, self.memorial_height_px),
            rx=self.corner_radius_px,
            ry=self.corner_radius_px,
            fill='white',  # Could be changed based on COLOUR
            stroke='black',
            stroke_width=self.stroke_width
        ))
        # Place text fields (assume LINE_1, LINE_2, LINE_3)
        # Adjust these positions as needed
        center_x = x + self.memorial_width_px / 2
        # Example vertical offsets for text lines
        y1 = y + 80
        y2 = y + 180
        y3 = y + 260
        dwg.add(dwg.text(
            order.get('LINE_1', ''),
            insert=(center_x, y1),
            font_size=f"{self.line1_size_pt}px",
            font_family="Georgia",
            text_anchor="middle",
            fill="black"
        ))
        dwg.add(dwg.text(
            order.get('LINE_2', ''),
            insert=(center_x, y2),
            font_size=f"{self.line2_size_pt}px",
            font_family="Georgia",
            text_anchor="middle",
            fill="black"
        ))
        dwg.add(dwg.text(
            order.get('LINE_3', ''),
            insert=(center_x, y3),
            font_size=f"{self.line3_size_pt}px",
            font_family="Georgia",
            text_anchor="middle",
            fill="black"
        ))
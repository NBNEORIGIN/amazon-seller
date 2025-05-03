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
        # Create the memorial rectangle
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
        
        # Calculate center x position for text
        center_x = x + (self.memorial_width_px / 2)
        
        # Add text elements with center alignment
        if not pd.isna(order['line_1']):
            dwg.add(dwg.text(
                str(order['line_1']),
                insert=(center_x, y + 128.72077),
                font_family="Georgia",
                font_size=f"{self.line1_size_pt}px",
                fill="black",
                text_anchor="middle"  # Center align text
            ))
        
        if not pd.isna(order['line_2']):
            dwg.add(dwg.text(
                str(order['line_2']),
                insert=(center_x, y + 210.50568),
                font_family="Georgia",
                font_size=f"{self.line2_size_pt}px",
                fill="black",
                text_anchor="middle"  # Center align text
            ))
        
        if not pd.isna(order['line_3']):
            lines = self.wrap_text(str(order['line_3']))
            current_y = y + 257.62384  # Start Y for line 3
            line_spacing = 47.11817    # Spacing between lines
            
            for line in lines:
                dwg.add(dwg.text(
                    line.strip(),
                    insert=(center_x, current_y),
                    font_family="Georgia",
                    font_size=f"{self.line3_size_pt}px",
                    fill="black",
                    text_anchor="middle"  # Center align text
                ))
                current_y += line_spacing

    def create_memorial_svg(self, orders, batch_num):
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        
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
        large_stakes = df[
            (df['COLOUR'].str.lower() == 'black') & 
            (df['TYPE'].str.contains('Large Stake', case=False, na=False)) &
            (df['graphic'].notna())
        ].copy()
        
        print(f"\nFound {len(large_stakes)} B&W Large Stakes")
        
        # Process in batches of 2
        batch_num = 1
        for start_idx in range(0, len(large_stakes), 2):
            batch_orders = large_stakes.iloc[start_idx:start_idx + 2]
            if not batch_orders.empty:
                print(f"\nProcessing B&W Large Stakes batch {batch_num}...")
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1
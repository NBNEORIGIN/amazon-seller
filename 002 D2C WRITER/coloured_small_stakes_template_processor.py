import os
import copy
import base64
import pandas as pd
import xml.etree.ElementTree as ET
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import add_multiline_text

class ColouredSmallStakesTemplateProcessor:
    def __init__(self, template_path, output_dir, graphics_path=None):
        self.template_path = template_path
        self.output_dir = output_dir
        self.graphics_path = graphics_path  # Directory containing graphics
        os.makedirs(self.output_dir, exist_ok=True)
        self.batch_size = 9  # 3x3 grid

    def process_orders(self, df):
        # Input `df` is assumed to be pre-filtered for this processor's category.
        df = df.copy()
        df.columns = [col.lower() for col in df.columns]
        # Normalize and diagnose unique values
        df['type'] = df['type'].astype(str).str.strip().str.lower()
        df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        df['decorationtype'] = df['decorationtype'].astype(str).str.strip().str.lower()
        print('Unique type values:', df['type'].unique())
        print('Unique colour values:', df['colour'].unique())
        print('Unique decorationtype values:', df['decorationtype'].unique())

        # Filtering logic removed. Input df is assumed to be pre-filtered.
        df_to_process = df

        if df_to_process.empty:
            print(f"No eligible orders for ColouredSmallStakesTemplateProcessor.")
            return

        print(f"Processing {len(df_to_process)} orders for ColouredSmallStakesTemplateProcessor.")
        n_orders = len(df_to_process)
        batch_num = 1
        for start_idx in range(0, n_orders, self.batch_size):
            batch_orders = df_to_process.iloc[start_idx:start_idx + self.batch_size]
            if not batch_orders.empty:
                svg_out_path = os.path.join(
                    self.output_dir,
                    f"coloured_small_stakes_batch_{batch_num:03d}.svg"
                )
                self.populate_svg(batch_orders, svg_out_path)
                # Output corresponding CSV file for this batch
                csv_out_path = os.path.splitext(svg_out_path)[0] + ".csv"
                batch_orders.to_csv(csv_out_path, index=False, encoding="utf-8-sig")
                print(f"Wrote batch CSV: {csv_out_path}")
                batch_num += 1

    import base64
    def embed_image(self, image_path):
        # Embed image as base64 data URI for SVG (PNG/JPG/SVG)
        try:
            ext = os.path.splitext(image_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg']:
                with open(image_path, 'rb') as f:
                    encoded = base64.b64encode(f.read()).decode('ascii')
                mime = 'image/png' if ext == '.png' else 'image/jpeg'
                data_uri = f"data:{mime};base64,{encoded}"
                return data_uri
            else:
                print(f"[embed_image] Skipping non-PNG/JPG file: {image_path}")
                return None
        except Exception as e:
            print(f"Failed to embed image: {image_path} ({e})")
            return None

    def populate_svg(self, batch_orders, output_svg_path):
        import svgwrite
        import math
        print(f"[populate_svg] graphics_path: {self.graphics_path}")
        print(f"[populate_svg] batch_orders['graphic'] column: {batch_orders['graphic'].tolist()}")

        # SVG page size
        page_w = 480
        page_h = 290
        dwg = svgwrite.Drawing(
            filename=output_svg_path,
            size=(f"{page_w}mm", f"{page_h}mm"),
            viewBox=f"0 0 {page_w} {page_h}"
        )

        # Memorial size and grid
        mem_w = 108
        mem_h = 75
        corner_r = 6
        grid_cols = 3
        grid_rows = 3
        total_mem = grid_cols * grid_rows
        # Calculate top-left of bottom-right grid
        grid_total_w = grid_cols * mem_w
        grid_total_h = grid_rows * mem_h
        grid_start_x = page_w - grid_total_w
        grid_start_y = page_h - grid_total_h

        # Draw each memorial (bottom row first, right to left)
        for idx, (_, order) in enumerate(batch_orders.iterrows()):
            if idx >= total_mem:
                break
            row = grid_rows - 1 - (idx // grid_cols)  # bottom to top
            col = grid_cols - 1 - (idx % grid_cols)   # right to left
            x = grid_start_x + col * mem_w
            y = grid_start_y + row * mem_h
            # Draw red rounded rectangle
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(mem_w, mem_h),
                rx=corner_r, ry=corner_r,
                fill='none',
                stroke='red',
                stroke_width=0.1
            ))
            # Draw/center graphic
            graphic_filename = str(order.get('graphic', '')).strip()
            if graphic_filename:
                graphic_path = os.path.join(self.graphics_path, graphic_filename)
                if os.path.exists(graphic_path):
                    embedded_image = self.embed_image(graphic_path)
                    if embedded_image:
                        # Center graphic, preserve aspect ratio (max mem_w x mem_h)
                        # For now, just fill the box (SVG will preserve aspect)
                        dwg.add(dwg.image(
                            href=embedded_image,
                            insert=(x, y),
                            size=(mem_w, mem_h),
                            preserveAspectRatio='xMidYMid meet'
                        ))
            # Draw text fields (centered) using shared utilities
            font_family = "Georgia"
            center_x = x + mem_w / 2
            center_y = y + (mem_h / 2)
            pt_to_mm = 0.352778
            # Line 1: 3.33pt, 15mm above center
            line1 = str(order.get('line_1', ''))
            check_grammar_and_typos(line1)
            line1_lines = split_line_to_fit(line1, 30)
            dwg.add(add_multiline_text(
                dwg,
                line1_lines,
                insert=(center_x, center_y - 15),
                font_size="3.33pt",
                font_family=font_family,
                anchor="middle",
                fill="black"
            ))
            # Line 2: 2.5mm, centered
            line2 = str(order.get('line_2', ''))
            check_grammar_and_typos(line2)
            line2_lines = split_line_to_fit(line2, 30)
            dwg.add(add_multiline_text(
                dwg,
                line2_lines,
                insert=(center_x, center_y),
                font_size="2.5mm",
                font_family=font_family,
                anchor="middle",
                fill="black"
            ))
            # Line 3: 3.33pt, 10mm below center, wrap at 30 chars, line spacing 1
            line3 = str(order.get('line_3', ''))
            check_grammar_and_typos(line3)
            line3_lines = split_line_to_fit(line3, 30)
            dwg.add(add_multiline_text(
                dwg,
                line3_lines,
                insert=(center_x, center_y + 10),
                font_size="3.33pt",
                font_family=font_family,
                anchor="middle",
                fill="black"
            ))

        # Draw UV printer reference blue square
        blue_size = 0.1
        dwg.add(dwg.rect(
            insert=(page_w - blue_size, page_h - blue_size),
            size=(blue_size, blue_size),
            fill='blue'
        ))
        dwg.save()
        print(f"Wrote batch SVG: {output_svg_path}")


if __name__ == "__main__":
    # Example usage
    template_path = r"g:\My Drive\003 APPS\XXX AmazonSeller - DEVLOPMENT\005 Assets\002_svg_templates\small_colour.svg"
    output_dir = r"g:\My Drive\003 APPS\XXX AmazonSeller - DEVLOPMENT\SVG_OUTPUT"
    graphics_path = r"g:\My Drive\003 APPS\XXX AmazonSeller - DEVLOPMENT\005 Assets\001_graphics"
    orders_path = r"g:\My Drive\003 APPS\XXX AmazonSeller - DEVLOPMENT\001 AMAZON DATA DOWNLOAD\output.txt"
    if not os.path.exists(orders_path):
        print(f"Orders file not found: {orders_path}")
        exit(1)
    df = pd.read_csv(orders_path, sep='\t', encoding='utf-8')
    processor = ColouredSmallStakesTemplateProcessor(template_path, output_dir, graphics_path)
    processor.process_orders(df)
    print("Coloured Small Stakes SVG generation complete!")

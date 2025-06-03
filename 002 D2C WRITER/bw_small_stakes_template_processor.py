import os
import base64
import pandas as pd
import svgwrite
from coloured_small_stakes_template_processor import ColouredSmallStakesTemplateProcessor
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import add_multiline_text

class BlackAndWhiteSmallStakesTemplateProcessor(ColouredSmallStakesTemplateProcessor):
    def __init__(self, template_path, output_dir, graphics_path=None):
        super().__init__(template_path, output_dir, graphics_path)
        self.batch_size = 3  # Only 3 memorials per batch (bottom row)

    def process_orders(self, df):
        df = df.copy()
        df.columns = [col.lower() for col in df.columns]
        df['type'] = df['type'].astype(str).str.strip().str.lower()
        df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        # Only small stake, black
        filtered = df[(df['type'] == 'small stake') & (df['colour'] == 'black')]
        print('Filtered rows for B&W Small Stakes:', len(filtered))
        batch_num = 1
        for start_idx in range(0, len(filtered), self.batch_size):
            batch_orders = filtered.iloc[start_idx:start_idx + self.batch_size]
            if not batch_orders.empty:
                svg_out_path = os.path.join(
                    self.output_dir,
                    f"bw_small_stakes_batch_{batch_num:03d}.svg"
                )
                self.populate_svg(batch_orders, svg_out_path)
                # Output corresponding CSV file for this batch
                csv_out_path = os.path.splitext(svg_out_path)[0] + ".csv"
                batch_orders.to_csv(csv_out_path, index=False, encoding="utf-8-sig")
                print(f"Wrote batch CSV: {csv_out_path}")
                batch_num += 1

    def populate_svg(self, batch_orders, output_svg_path):
        # SVG page size
        page_w = 480
        page_h = 290
        dwg = svgwrite.Drawing(
            filename=output_svg_path,
            size=(f"{page_w}mm", f"{page_h}mm"),
            viewBox=f"0 0 {page_w} {page_h}"
        )
        mem_w = 108
        mem_h = 75
        corner_r = 6
        grid_cols = 3
        grid_rows = 1
        total_mem = grid_cols * grid_rows
        grid_total_w = grid_cols * mem_w
        grid_total_h = grid_rows * mem_h
        grid_start_x = page_w - grid_total_w
        grid_start_y = page_h - grid_total_h
        for idx, (_, order) in enumerate(batch_orders.iterrows()):
            if idx >= total_mem:
                break
            row = 0  # Only bottom row
            col = grid_cols - 1 - (idx % grid_cols)   # right to left
            x = grid_start_x + col * mem_w
            y = grid_start_y + row * mem_h
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(mem_w, mem_h),
                rx=corner_r, ry=corner_r,
                fill='none',
                stroke='red',
                stroke_width=0.1
            ))
            # Special SKU logic
            sku = str(order.get('sku', '')).strip()
            if sku == 'M0634S - CAT - RAINBOW BRIDGE':
                graphic_filename = 'Small Rainbow Bridge.png'
            else:
                graphic_filename = str(order.get('graphic', '')).strip()
                if graphic_filename and not graphic_filename.lower().startswith('small '):
                    graphic_filename = 'Small ' + graphic_filename
            graphic_path = os.path.join(self.graphics_path, graphic_filename)
            if os.path.exists(graphic_path):
                embedded_image = self.embed_image(graphic_path)
                if embedded_image:
                    dwg.add(dwg.image(
                        href=embedded_image,
                        insert=(x, y),
                        size=(mem_w, mem_h),
                        preserveAspectRatio='xMidYMid meet'
                    ))
            # Text placement (modular, using Georgia, same font sizes/positions)
            font_family = "Georgia"
            center_x = x + mem_w / 2
            center_y = y + (mem_h / 2)
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
        # UV printer reference blue square
        blue_size = 0.1
        dwg.add(dwg.rect(
            insert=(page_w - blue_size, page_h - blue_size),
            size=(blue_size, blue_size),
            fill='blue'
        ))
        dwg.save()
        print(f"Wrote batch SVG: {output_svg_path}")

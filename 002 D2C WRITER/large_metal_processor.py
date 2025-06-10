import os
import base64
import pandas as pd
import svgwrite
from coloured_small_stakes_template_processor import ColouredSmallStakesTemplateProcessor
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processors.text_utils import split_line_to_fit, check_grammar_and_typos
from core.processors.svg_utils import add_multiline_text

class LargeMetalProcessor(ColouredSmallStakesTemplateProcessor):
    def __init__(self, template_path, output_dir, graphics_path=None):
        super().__init__(template_path, output_dir, graphics_path)
        # mem_w = 127, mem_h = 76.2
        # page_w = 480, page_h = 290
        # grid_cols = 480 // 127 = 3
        # grid_rows = 290 // 76.2 = 3 (integer division)
        # However, the original logic was to place them on the bottom row.
        # Let's stick to a single row for now, as per original.
        # grid_cols = 3, grid_rows = 1.
        # batch_size = grid_cols * grid_rows
        self.batch_size = 3 # 3 items fit in a row: 3 * 127 = 381mm, page width is 480mm

    def process_orders(self, df):
        df = df.copy()
        df.columns = [col.lower() for col in df.columns]
        df['type'] = df['type'].astype(str).str.strip().str.lower()
        # No 'colour' column for large metal, remove if it was there
        # df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        # Only large metal
        filtered = df[df['type'] == 'large metal']
        print('Filtered rows for Large Metal:', len(filtered))
        batch_num = 1
        for start_idx in range(0, len(filtered), self.batch_size):
            batch_orders = filtered.iloc[start_idx:start_idx + self.batch_size]
            if not batch_orders.empty:
                svg_out_path = os.path.join(
                    self.output_dir,
                    f"large_metal_batch_{batch_num:03d}.svg"
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
        mem_w = 127
        mem_h = 76.2
        corner_r = 6 # Remains 6 as per current file and no new instruction

        # Recalculate grid based on new mem_w, mem_h and page_w, page_h
        # Original logic: items placed on the bottom row, right to left.
        # page_w = 480, page_h = 290

        current_grid_cols = 3 # From self.batch_size in __init__
        current_grid_rows = 1 # Implied by original "bottom row" logic

        # Check if they fit, adjust if necessary
        if current_grid_cols * mem_w > page_w:
            current_grid_cols = page_w // mem_w
        if current_grid_rows * mem_h > page_h:
            current_grid_rows = page_h // mem_h

        # Update batch_size in __init__ if these calculations lead to a different number
        # For now, assume self.batch_size correctly reflects the number of items per SVG.
        # The problem states "The batch_size should also be updated to grid_cols * grid_rows."
        # This was done in __init__ based on the assumption of 3 cols, 1 row.

        grid_cols = current_grid_cols
        grid_rows = current_grid_rows

        # total_mem is effectively self.batch_size for one SVG page
        total_mem_on_page = grid_cols * grid_rows

        grid_total_w = grid_cols * mem_w
        grid_total_h = grid_rows * mem_h

        # Position the grid at the bottom-right of the page
        grid_start_x = page_w - grid_total_w
        grid_start_y = page_h - grid_total_h

        for idx, (_, order) in enumerate(batch_orders.iterrows()):
            if idx >= total_mem_on_page: # Ensure we don't try to place more items than fit
                break

            # Assuming items are filled right-to-left, bottom row first if multiple rows.
            # For a single row (grid_rows = 1):
            row_idx = 0 # Relative to the grid block, not page
            col_idx = grid_cols - 1 - (idx % grid_cols) # right to left filling

            # For multiple rows (if grid_rows > 1), filling bottom-up, right-to-left:
            # row_idx = grid_rows - 1 - (idx // grid_cols)
            # col_idx = grid_cols - 1 - (idx % grid_cols)

            # Sticking to original single row, right-to-left logic
            x = grid_start_x + col_idx * mem_w
            y = grid_start_y + row_idx * mem_h # y will be grid_start_y since row_idx is 0 for a single row

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

if __name__ == "__main__":
    import pandas as pd
    import os

    print("Running LargeMetalProcessor basic test...")

    # Create dummy directories and data for testing
    test_output_dir = "test_lmp_output"
    test_graphics_dir = "test_lmp_graphics"
    os.makedirs(test_output_dir, exist_ok=True)
    os.makedirs(test_graphics_dir, exist_ok=True)

    # Dummy graphics file (empty)
    # In a real scenario, this would be an actual image.
    # The processor's embed_image checks for file existence.
    dummy_graphic_name = "Small TestGraphic.png"
    with open(os.path.join(test_graphics_dir, dummy_graphic_name), "w") as f:
        f.write("") # Create an empty file

    processor = LargeMetalProcessor(
        template_path=None, # LargeMetalProcessor doesn't use template_path in __init__
        output_dir=test_output_dir,
        graphics_path=test_graphics_dir
    )

    # Create a sample DataFrame
    sample_data = {
        'order-id': ['123-001', '123-002', '123-003', '123-004'],
        'SKU': ['LM001', 'LM002', 'SM001', 'LM003'],
        'Type': ['Large Metal', 'Large Metal', 'Small Metal', 'Large Metal'], # Note: Case difference
        'Colour': ['Silver', 'Silver', 'Black', 'Silver'], # Colour is not used by LMP
        'Graphic': [dummy_graphic_name, 'NonExistent.png', 'SomeGraphic.png', dummy_graphic_name],
        'Line_1': ['In Loving Memory', 'Forever In Our Hearts', 'Pet Angel', 'Gone But Not Forgotten'],
        'Line_2': ['Name One', 'Name Two', 'Buddy', 'Name Three'],
        'Line_3': ['1950-2020', '1960-2021', '2010-2022', '1970-2023']
    }
    test_df = pd.DataFrame(sample_data)

    print(f"Initial test DataFrame:\n{test_df}")

    # Process the orders
    # The processor itself filters for 'type' == 'large metal'
    processor.process_orders(test_df)

    print(f"Test finished. Check '{test_output_dir}' for generated SVGs and CSVs.")
    print("Expected output: SVGs for LM001, LM002, LM003 (3 orders).")
    print(f"Graphic '{dummy_graphic_name}' should be attempted for LM001 and LM003.")
    print("Graphic 'NonExistent.png' for LM002 should be skipped gracefully.")

    # Basic cleanup (optional, for local testing)
    # import shutil
    # shutil.rmtree(test_output_dir)
    # shutil.rmtree(test_graphics_dir)
    # print("Cleaned up test directories.")

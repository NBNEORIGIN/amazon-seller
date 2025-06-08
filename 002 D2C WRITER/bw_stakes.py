import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd

class BWStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir)
        self.CATEGORY = 'regular_bw_stakes'  # Updated CATEGORY

        # Page dimensions specific to B&W Stakes
        self.page_width_mm = 480
        self.page_height_mm = 330

        # Recalculate page pixel dimensions based on new mm values and px_per_mm from MemorialBase
        self.page_width_px = int(self.page_width_mm * self.px_per_mm)
        self.page_height_px = int(self.page_height_mm * self.px_per_mm)

        # Memorial dimensions (assuming they are standard, as inherited from MemorialBase)
        # self.memorial_width_mm = 140 (from MemorialBase)
        # self.memorial_height_mm = 90 (from MemorialBase)
        self.memorial_width_px = int(self.memorial_width_mm * self.px_per_mm)
        self.memorial_height_px = int(self.memorial_height_mm * self.px_per_mm)

        # x_offset_px and y_offset_px are no longer used for centering;
        # positioning is absolute from bottom-right.

    def process_orders(self, df): # Reverted: lang_tool_instance_global parameter removed
        # Normalize all column names to lowercase and strip
        df.columns = [col.lower().strip() for col in df.columns]
        if 'type' in df.columns:
            df['type'] = df['type'].astype(str).str.strip().str.lower()
        if 'colour' in df.columns:
            df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        if 'decorationtype' not in df.columns:
    
            df['decorationtype'] = ''
        else:
            df['decorationtype'] = df['decorationtype'].astype(str).str.strip().str.lower()

        allowed_colours = ['black']
        eligible = df[
            (df['type'] == 'regular stake') &
            (df['colour'].isin(allowed_colours)) &
            (df['decorationtype'] == 'graphic')
        ].copy()
        print(f"[BW DEBUG] Eligible before expansion: {len(eligible)}")

        if eligible.empty:
            print("[BW DEBUG] No eligible B&W stakes before expansion.")
            return

        # Expand rows by number-of-items
        expanded_rows = []
        for _, row in eligible.iterrows():
            try:
                qty = int(row.get('number-of-items', 1))
                qty = max(qty, 1)
            except Exception:
                qty = 1
            for _ in range(qty):
                expanded_rows.append(row.copy())
        df_expanded = pd.DataFrame(expanded_rows)

        bw_stakes = df_expanded[
            (df_expanded['type'] == 'regular stake') &
            (df_expanded['colour'].isin(allowed_colours)) &
            (df_expanded['decorationtype'] == 'graphic') &
            (df_expanded['graphic'].notna())
        ].copy()
        print(f"\nFound {len(bw_stakes)} B&W Stakes")
        
        # Process in batches of 3
        batch_num = 1
        for start_idx in range(0, len(bw_stakes), 3):
            batch_orders = bw_stakes.iloc[start_idx:start_idx + 3]
            if not batch_orders.empty:
                print(f"\nProcessing B&W batch {batch_num}...")
                self.create_memorial_svg(batch_orders.to_dict('records'), batch_num)
                # Reverted: lang_tool_instance_global argument removed
                self.create_batch_csv(batch_orders.to_dict('records'), batch_num, self.CATEGORY)
                batch_num += 1

    def create_memorial_svg(self, orders, batch_num):
        filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg" # self.CATEGORY is now 'regular_bw_stakes'
        output_path = os.path.join(self.OUTPUT_DIR, filename)
        
        # Use updated page dimensions for SVG size
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"), # Uses new page_width_mm, page_height_mm
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}" # Uses new page_width_px, page_height_px
        )
        
        # Process up to 3 memorials with bottom-right placement
        for idx, order in enumerate(orders):
            if idx >= 3: # Max 3 orders
                break
            
            # New placement logic (bottom-right)
            if idx == 0:  # First item (bottom-right)
                x = self.page_width_px - self.memorial_width_px
                y = self.page_height_px - self.memorial_height_px
            elif idx == 1:  # Second item (bottom edge, left of first)
                x = self.page_width_px - (2 * self.memorial_width_px)
                y = self.page_height_px - self.memorial_height_px
            elif idx == 2:  # Third item (bottom edge, left of second)
                x = self.page_width_px - (3 * self.memorial_width_px)
                y = self.page_height_px - self.memorial_height_px
            else: # Should not happen due to "if idx >= 3: break"
                continue

            default_slot_stroke_color = 'red'
            slot_stroke_color = default_slot_stroke_color
            is_attention_order = False

            order_colour_lower = str(order.get('colour', '')).lower()
            order_type_lower = str(order.get('type', '')).lower()

            if order_colour_lower in ['marble', 'stone']:
                is_attention_order = True

            if order_type_lower == 'regular plaque':
                is_attention_order = True

            if is_attention_order:
                slot_stroke_color = 'yellow'

            # Add memorial outline
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(self.memorial_width_px, self.memorial_height_px),
                rx=6*self.px_per_mm, # Kept from existing code
                ry=6*self.px_per_mm, # Kept from existing code
                fill='none',
                stroke=slot_stroke_color, # MODIFIED HERE
                stroke_width=0.1*self.px_per_mm # Kept from existing code
            ))
            
            # Add graphic if exists
            if not pd.isna(order['graphic']):
                graphic_path = os.path.join(self.graphics_path, str(order['graphic']))
                print(f"Looking for graphic: {graphic_path}")
                if os.path.exists(graphic_path):
                    print(f"Found graphic: {graphic_path}")
                    embedded_image = self.embed_image(graphic_path)
                    if embedded_image:
                        print(f"Successfully embedded graphic")
                        dwg.add(dwg.image(
                            href=embedded_image,
                            insert=(x, y),
                            size=(self.memorial_width_px, self.memorial_height_px)
                        ))
                    else:
                        print(f"Failed to embed graphic")
                else:
                    print(f"Warning: Graphic not found: {graphic_path}")
            
            # Calculate text center
            center_x = x + (self.memorial_width_px / 2)

            # --- Robust text handling for B&W, matching regular_stakes.py ---
            # Line 1
            value1 = order.get('line_1')
            if value1 is not None and not (isinstance(value1, float) and pd.isna(value1)):
                dwg.add(dwg.text(
                    str(value1),
                    insert=(center_x, y + (28 * self.px_per_mm)),
                    font_size=f"{17 * self.pt_to_mm}mm",
                    font_family="Georgia",
                    text_anchor="middle",
                    fill="black"
                ))
            else:
                print(f"Warning: Missing text in line_1 for order {order.get('order-id', 'Unknown')}")

            # Line 2
            value2 = order.get('line_2')
            if value2 is not None and not (isinstance(value2, float) and pd.isna(value2)):
                dwg.add(dwg.text(
                    str(value2),
                    insert=(center_x, y + (45 * self.px_per_mm)),
                    font_size=f"{25 * self.pt_to_mm}mm",
                    font_family="Georgia",
                    text_anchor="middle",
                    fill="black"
                ))
            else:
                print(f"Warning: Missing text in line_2 for order {order.get('order-id', 'Unknown')}")

            # Line 3 (multi-line, dynamic font and tspan logic)
            value3 = order.get('line_3')
            if value3 is not None and not (isinstance(value3, float) and pd.isna(value3)):
                line3_text = str(value3).strip()
                if line3_text:
                    lines = line3_text.split('\n')
                    font_mm = 12 * self.pt_to_mm
                    char_width_mm = 0.5 * font_mm
                    max_line_mm = self.memorial_width_mm * 0.6
                    max_chars = int(max_line_mm / char_width_mm)
                    split_lines = []
                    for l in lines:
                        if l.strip():
                            split_lines.extend(self.wrap_text(l, max_chars))
                    if split_lines:
                        if len(split_lines) == 1:
                            import textwrap
                            split_lines = textwrap.wrap(split_lines[0], width=30)
                        split_lines = split_lines[:5]
                        total_chars = sum(len(line) for line in split_lines)
                        if 10 <= total_chars <= 30:
                            line3_font_size_pt = 17 * 1.2
                        elif 31 <= total_chars <= 90:
                            line3_font_size_pt = 17 * 1.2 * 0.9
                        else:
                            line3_font_size_pt = 12 * 1.1
                        line3_text_element = dwg.text(
                            "",
                            insert=(center_x, y + (57 * self.px_per_mm)),
                            font_size=f"{line3_font_size_pt * self.pt_to_mm}mm",
                            font_family="Georgia",
                            text_anchor="middle",
                            fill="black"
                        )
                        for line_idx, line in enumerate(split_lines):
                            dy_val = "0" if line_idx == 0 else "1.2em"
                            tspan = dwg.tspan(
                                line.strip(),
                                x=[center_x],
                                dy=[dy_val]
                            )
                            line3_text_element.add(tspan)
                        dwg.add(line3_text_element)
            else:
                print(f"Warning: Missing text in line_3 for order {order.get('order-id', 'Unknown')}")

        # Add reference point (using the method from MemorialBase for consistency if desired, or keep specific one)
        # For now, keeping the existing specific reference point logic from bw_stakes.py
        # It might need adjustment if its position is critical relative to new page size.
        # The y_pos calculation (289.8 - 0.011) * self.px_per_mm was likely tied to the old page_height_mm (289.9).
        # Let's adjust it to be relative to the new page_height_px for bottom-right corner.
        ref_size_px = 0.1 * self.px_per_mm
        # x_pos = self.page_width_px - ref_size_px # This is correct for bottom-right
        # y_pos = self.page_height_px - ref_size_px # This is correct for bottom-right
        
        # Using the inherited add_reference_point method is cleaner if it does what's needed.
        # MemorialBase.add_reference_point places it at page_width_px - ref_size_px and page_height_px - ref_size_px
        # This is likely the desired behavior for the new layout.
        self.add_reference_point(dwg) # Use the method from MemorialBase
        
        dwg.save()
        return dwg

if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Parse arguments for output directory and graphics path
    if len(sys.argv) != 3:
        print("Usage: python bw_stakes.py <output_dir> <graphics_path>")
        sys.exit(1)

    output_dir = sys.argv[1]
    graphics_path = sys.argv[2]

    # Load the CSV (one memorial per row, already expanded)
    csv_path = str(Path(__file__).parent.parent / "001 AMAZON DATA DOWNLOAD" / "output.csv")
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)

    df = pd.read_csv(csv_path, encoding="utf-8")
    processor = BWStakesProcessor(graphics_path, output_dir)
    processor.process_orders(df)
    print("B&W Stake SVG generation complete!")

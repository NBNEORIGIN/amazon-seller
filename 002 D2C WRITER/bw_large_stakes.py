import os
import svgwrite
from memorial_base import MemorialBase
import pandas as pd

class BWLargeStakesProcessor(MemorialBase):
    def __init__(self, graphics_path, output_dir):
        super().__init__(graphics_path, output_dir) # MemorialBase provides px_per_mm, pt_to_mm, date_str
        self.CATEGORY = 'regular_bw_large_stakes'
        
        # Page dimensions
        self.page_width_mm = 480
        self.page_height_mm = 330
        self.page_width_px = int(self.page_width_mm * self.px_per_mm)
        self.page_height_px = int(self.page_height_mm * self.px_per_mm)
        
        # Memorial dimensions for large stakes
        self.memorial_width_mm = 220
        self.memorial_height_mm = 150
        self.memorial_width_px = int(self.memorial_width_mm * self.px_per_mm)
        self.memorial_height_px = int(self.memorial_height_mm * self.px_per_mm)
        
        # Style attributes, scaled by px_per_mm
        self.corner_radius_px = int(8 * self.px_per_mm) # Example: 8mm radius
        self.stroke_width_px = 0.2 * self.px_per_mm # Example: 0.2mm stroke width

        # Text sizes in pixels (example point sizes, adjust as needed)
        # Using pt_to_mm for conversion then to px
        _line1_pt = 20  # Example: "In Loving Memory Of"
        _line2_pt = 30  # Example: Name
        _line3_pt = 18  # Example: Additional lines

        self.line1_font_px = int(_line1_pt * self.pt_to_mm * self.px_per_mm)
        self.line2_font_px = int(_line2_pt * self.pt_to_mm * self.px_per_mm)
        self.line3_font_px = int(_line3_pt * self.pt_to_mm * self.px_per_mm)
        
        # Grid layout (for 2 items per page)
        self.grid_cols = 2 # Remains 2
        self.grid_rows = 1 # Remains 1
        # Old x_offset_px, y_offset_px, memorial_spacing_x_px are removed as placement is absolute bottom-right

    def add_memorial(self, dwg, x, y, order):
        # Create the memorial rectangle (red cut line)
        # x, y are the top-left corner of the memorial block
        rect = dwg.rect(
            insert=(x, y),
            size=(self.memorial_width_px, self.memorial_height_px),
            rx=self.corner_radius_px,
            ry=self.corner_radius_px,
            fill='none',
            stroke='#ff0000', # Red stroke for cut line
            stroke_width=self.stroke_width_px # Use new stroke_width_px
        )
        dwg.add(rect)

        # Optional: Draw blue face outline (kept for now, if it's a design requirement)
        # If this is purely for visual debugging in SVG, it can be removed.
        # For now, assuming it might be a design element.
        # blue_face = dwg.rect(
        #     insert=(x, y),
        #     size=(self.memorial_width_px, self.memorial_height_px),
        #     rx=self.corner_radius_px,
        #     ry=self.corner_radius_px,
        #     fill='none',
        #     stroke='#0000ff', # Blue stroke
        #     stroke_width=self.stroke_width_px / 2 # Thinner if just a guide
        # )
        # dwg.add(blue_face)

        center_x = x + (self.memorial_width_px / 2)

        # --- Graphics embedding (if present) ---
        # Using memorial_width_px and memorial_height_px for graphic size
        if 'graphic' in order and pd.notna(order['graphic']) and str(order['graphic']).strip() != '':
            graphic_path = os.path.join(self.graphics_path, str(order['graphic']))
            if os.path.exists(graphic_path):
                embedded_image = self.embed_image(graphic_path) # From MemorialBase
                if embedded_image:
                    dwg.add(dwg.image(
                        href=embedded_image,
                        insert=(x, y), # Graphic typically covers the whole memorial area
                        size=(self.memorial_width_px, self.memorial_height_px)
                    ))
                else:
                    print(f"[WARNING] Failed to embed graphic for order {order.get('order-id', '')}: {graphic_path}")
            else:
                print(f"[WARNING] Graphic file not found for order {order.get('order-id', '')}: {graphic_path}")
        # else: # Removed redundant else print, graphic absence is not necessarily a warning for all stakes
            # print(f"[INFO] No graphic specified for order {order.get('order-id', '')} (SKU: {order.get('sku', '')})")


        # --- Text Positioning and Sizing ---
        # Y positions relative to the memorial block's top 'y'
        # These percentages can be tuned for aesthetics.
        line1_y_abs = y + (0.15 * self.memorial_height_px)
        line2_y_abs = y + (0.40 * self.memorial_height_px) # Adjusted for potentially larger Line 2
        line3_start_y_abs = y + (0.65 * self.memorial_height_px) # Start Y for multi-line text block for Line 3

        # --- Line 1 ---
        if pd.notna(order.get('line_1')):
            dwg.add(dwg.text(
                str(order['line_1']),
                insert=(center_x, line1_y_abs),
                font_family="Georgia",
                font_size=f"{self.line1_font_px}px", # Use new pixel font size
                fill="black",
                text_anchor="middle"
            ))
        # --- Line 2 ---
        if pd.notna(order.get('line_2')):
            dwg.add(dwg.text(
                str(order['line_2']),
                insert=(center_x, line2_y_abs),
                font_family="Georgia",
                font_size=f"{self.line2_font_px}px", # Use new pixel font size
                fill="black",
                text_anchor="middle"
            ))
        # --- Line 3 ---
        if pd.notna(order.get('line_3')):
            # Using wrap_text from MemorialBase. Max chars might need adjustment for larger font/memorial.
            # Estimate max_chars based on new memorial_width_px and line3_font_px
            # This is a rough estimate, character widths vary.
            # char_width_estimate_px = self.line3_font_px * 0.5 # Common heuristic
            # max_chars_line3 = int((self.memorial_width_px * 0.9) / char_width_estimate_px) # 90% of width

            # Simpler: use a fixed sensible wrap width or pass one from __init__ if complex adjustment is needed.
            # For now, let MemorialBase's default or a reasonable fixed value handle it.
            lines = self.wrap_text(str(order['line_3']), max_chars=35) # Max_chars can be tuned

            # Calculate line height based on font size (e.g., 1.2 * font_size)
            line_height_px = int(self.line3_font_px * 1.2)

            # Create a text group for Line 3 for easier multi-line handling if needed, or add directly
            line3_text_element = dwg.text(
                "", # Main text element, tspans will be added
                insert=(center_x, line3_start_y_abs),
                font_family="Georgia",
                font_size=f"{self.line3_font_px}px", # Use new pixel font size
                fill="black",
                text_anchor="middle"
            )

            for line_idx, line_content in enumerate(lines):
                dy_val = "0" if line_idx == 0 else f"{line_height_px}px" # Relative offset for subsequent lines
                tspan = dwg.tspan(line_content.strip(), x=[center_x], dy=[dy_val])
                line3_text_element.add(tspan)
            dwg.add(line3_text_element)


    def create_memorial_svg(self, orders, batch_num, output_path=None):
        if output_path is None:
            # Filename uses new self.CATEGORY
            filename = f"{self.CATEGORY}_{self.date_str}_{batch_num:03d}.svg"
            filepath = os.path.join(self.OUTPUT_DIR, filename)
        else:
            filepath = output_path

        # Create SVG with new page dimensions
        dwg = svgwrite.Drawing(
            filepath,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"), # Use new page_width_mm, page_height_mm
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}" # Use new page_width_px, page_height_px
        )
        
        # Process up to 2 memorials with new bottom-right placement
        for idx, order in enumerate(orders):
            if idx >= 2:  # Max 2 orders for large stakes
                break
            
            # New placement logic (bottom-right)
            if idx == 0:  # First item (bottom-right)
                x = self.page_width_px - self.memorial_width_px
                y = self.page_height_px - self.memorial_height_px
            elif idx == 1:  # Second item (bottom edge, left of first)
                x = self.page_width_px - (2 * self.memorial_width_px)
                y = self.page_height_px - self.memorial_height_px
            else: # Should not happen
                continue

            self.add_memorial(dwg, x, y, order) # Pass calculated x, y
        
        self.add_reference_point(dwg) # Use inherited method from MemorialBase
        
        dwg.save()

    def process_orders(self, df):
        print(f"[DEBUG] Entering process_orders for {self.CATEGORY}")
        print(f"[DEBUG] Initial DataFrame shape: {df.shape}")
        print("[DEBUG] Initial DataFrame head:\n", df.head())

        # Normalize all column names to lowercase and strip
        df.columns = [col.lower().strip() for col in df.columns]

        # Ensure essential columns exist and perform type conversions
        if 'type' in df.columns:
            df['type'] = df['type'].astype(str).str.strip().str.lower()
        else:
            df['type'] = '' # Add empty column if missing to prevent key errors
            print("[DEBUG] 'type' column was missing. Added as empty.")

        if 'colour' in df.columns:
            df['colour'] = df['colour'].astype(str).str.strip().str.lower()
        else:
            df['colour'] = ''
            print("[DEBUG] 'colour' column was missing. Added as empty.")

        if 'decorationtype' not in df.columns:
            df['decorationtype'] = '' # Default to empty string if missing
            print("[DEBUG] 'decorationtype' column was missing. Added as empty.")
        else:
            df['decorationtype'] = df['decorationtype'].astype(str).str.strip().str.lower()

        print(f"[DEBUG] DataFrame shape after normalization/type conversion: {df.shape}")
        print("[DEBUG] DataFrame head after normalization/type conversion:\n", df.head())

        allowed_colours = ['black', 'slate']
        print(f"[DEBUG] Filtering conditions: type == 'large stake', colour in {allowed_colours}, decorationtype == 'graphic'")

        # Apply filters
        large_stakes = df[
            (df['type'] == 'large stake') &
            (df['colour'].isin(allowed_colours)) &
            (df['decorationtype'] == 'graphic')
        ].copy() # Use .copy() to avoid SettingWithCopyWarning

        print(f"[DEBUG] DataFrame shape after filtering: {large_stakes.shape}")
        if not large_stakes.empty:
            print("[DEBUG] Filtered large_stakes head:\n", large_stakes.head())
            print("[DEBUG] Sample rows from filtered large_stakes (up to 5):")
            for i, (_, row) in enumerate(large_stakes.head().iterrows()):
                print(f"  Row {i}: Order ID: {row.get('order-id', 'N/A')}, SKU: {row.get('sku', 'N/A')}, Type: {row.get('type')}, Colour: {row.get('colour')}, Deco: {row.get('decorationtype')}, Graphic: {row.get('graphic', 'N/A')}")
        else:
            print("[DEBUG] No rows matched the filtering criteria for large stakes.")
            # Optional: Log why some rows that might seem eligible were excluded
            potential_matches = df[df['type'] == 'large stake']
            if not potential_matches.empty:
                print(f"[DEBUG] Found {len(potential_matches)} rows with type 'large stake' before other filters.")
                for idx, row in potential_matches.head().iterrows(): # Check a few
                    reasons = []
                    if not row['colour'] in allowed_colours: reasons.append(f"colour='{row['colour']}' (not in {allowed_colours})")
                    if not row['decorationtype'] == 'graphic': reasons.append(f"decorationtype='{row['decorationtype']}' (not 'graphic')")
                    if reasons: print(f"  Potential Large Stake (Order ID: {row.get('order-id', 'N/A')}) excluded due to: {'; '.join(reasons)}")
            else:
                print("[DEBUG] No rows even matched type 'large stake'.")


        if large_stakes.empty:
            print(f"No eligible {self.CATEGORY} found.")
            return

        print(f"\nFound {len(large_stakes)} orders for {self.CATEGORY}")

        # Process in batches of 2 (as per self.grid_cols)
        batch_size = self.grid_cols
        for batch_num, batch_start in enumerate(range(0, len(large_stakes), batch_size), 1):
            batch_df = large_stakes.iloc[batch_start:batch_start + batch_size]
            if not batch_df.empty:
                print(f"\nProcessing {self.CATEGORY} batch {batch_num} ({len(batch_df)} orders)...")
                # print(batch_df[['order-id','type','colour','decorationtype']].head()) # Already logged above more detailed
                self.create_memorial_svg(batch_df.to_dict('records'), batch_num)
                self.create_batch_csv(batch_df.to_dict('records'), batch_num, self.CATEGORY) # Uses updated self.CATEGORY

        # Export CSV for all processed large stakes for this category
        if not large_stakes.empty:
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)
            # Use new self.CATEGORY for the consolidated CSV filename
            csv_filename = os.path.join(self.OUTPUT_DIR, f"{self.CATEGORY}_{self.date_str}_ALL.csv")
            large_stakes.to_csv(csv_filename, index=False, encoding="utf-8")
            print(f"Exported consolidated {self.CATEGORY} CSV: {csv_filename} ({len(large_stakes)} rows)")
        else:
            print(f"No {self.CATEGORY} to export to consolidated CSV.")
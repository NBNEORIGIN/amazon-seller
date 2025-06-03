import os
import svgwrite
import pandas as pd
from datetime import datetime

from core.processors.base import ProcessorBase
from core.processors import register_processor
from core.processors.text_utils import TextUtils
from core.processors.svg_utils import SVGUtils

class BWLargeStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = TextUtils()
        self.svg_utils = SVGUtils()

        self.CATEGORY = 'B&W_LARGE_STAKES'
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # SVG dimensions (from original file, seems specific to this stake type)
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.viewbox_width = 1662  # This seems to be the effective pixel dimensions for the SVG content
        self.viewbox_height = 1095

        # Memorial item dimensions (exact from SVG comments in original)
        self.memorial_width_px = 755.42004
        self.memorial_height_px = 453.1008
        self.corner_radius_px = 22.012239
        self.stroke_width_px = 0.378046 # For outlines

        # Text sizes (points, but used as px in original SVG text, needs clarification or use pt_to_px)
        # For now, assuming these are pixel sizes as used in original f-strings for font_size
        self.line1_font_size_px = 45.3333
        self.line2_font_size_px = 66.6667
        self.line3_font_size_px = 32

        # Position of first memorial item (top-left of the item)
        self.item_x_offset_px = 150.59283 # From left of page to first item
        self.item_y_offset_px = 641.97479 # From top of page to first item (seems large, might be bottom-up Y or specific viewbox)
                                          # Given viewbox_height is 1095, an item at Y=641 would be in lower half.
                                          # Original comment: "Position of first memorial (from SVG)"
                                          # Original create_memorial_svg has y = self.y_offset_px, and this is the only row.
                                          # This implies the items are placed starting at this Y coordinate.

        # Memorial spacing (distance between start of one item and start of next)
        self.item_spacing_x_px = 755.79810

        # Layout: 2 items per page, in a single row for this processor
        self.grid_cols = 2
        self.grid_rows = 1
        self.batch_size = self.grid_cols * self.grid_rows # Max 2 items per SVG page

    def is_applicable(self, order_data: pd.Series) -> bool:
        order_type = str(order_data.get('type', '')).strip().lower()
        decoration_type = str(order_data.get('decorationtype', '')).strip().lower()
        colour = str(order_data.get('colour', '')).strip().lower()

        # Original filtering also allowed 'slate'
        return (order_type == 'large stake' and
                decoration_type == 'graphic' and
                colour in ['black', 'slate'])

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        self.output_dir = output_dir
        self.graphics_path = graphics_path # For graphics associated with orders
        os.makedirs(self.output_dir, exist_ok=True)

        if order_data.empty:
            print("No B&W Large Stakes orders to process.")
            return

        # Assuming order_data is already filtered by is_applicable
        # Additional filtering from original (e.g. graphic.notna()) can be added if necessary
        df_to_process = order_data.copy()

        if 'graphic' not in df_to_process.columns or df_to_process['graphic'].isna().all():
            print(f"Warning: No orders with graphics found for BWLargeStakesProcessor. Skipping.")
            #return # Or process without graphics if that's a valid state

        print(f"Processing {len(df_to_process)} B&W Large Stakes orders.")

        batch_num = 1
        total_items = len(df_to_process)

        for start_idx in range(0, total_items, self.batch_size): # self.batch_size is 2
            end_idx = min(start_idx + self.batch_size, total_items)
            current_batch_df = df_to_process.iloc[start_idx:end_idx]

            if not current_batch_df.empty:
                orders_for_svg_page = current_batch_df.to_dict('records')

                if len(orders_for_svg_page) == 1: # Single item processing
                    order = orders_for_svg_page[0]
                    order_id = str(order.get('order-id', 'NO_ID')).strip()
                    sku = str(order.get('sku', 'NO_SKU')).strip()
                    filename = f"BW_LARGE_STAKE_{order_id}_{sku}.svg"
                else: # Batch page (max 2 items)
                    filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"

                self._create_memorial_page_svg(orders_for_svg_page, filename)
                # self._create_batch_csv(...) # If CSVs per page are needed
                batch_num += 1

        # The original also had a final CSV export of ALL processed large_stakes.
        # This might be better handled by the main application after all processors run.
        # For now, keeping processor focused on its SVGs.

    def _add_item_to_svg_page(self, dwg, x_item_start: float, y_item_start: float, order_details: dict):
        """Adds a single B&W Large Stake item to the SVG drawing."""

        # Red cut line rectangle
        dwg.add(dwg.rect(insert=(x_item_start, y_item_start), size=(self.memorial_width_px, self.memorial_height_px),
                         rx=self.corner_radius_px, ry=self.corner_radius_px, fill='none',
                         stroke='#ff0000', stroke_width=self.stroke_width_px))

        # Blue face outline (assuming same as item boundary for now)
        dwg.add(dwg.rect(insert=(x_item_start, y_item_start), size=(self.memorial_width_px, self.memorial_height_px),
                         rx=self.corner_radius_px, ry=self.corner_radius_px, fill='none',
                         stroke='#0000ff', stroke_width=self.stroke_width_px))

        center_x_abs = x_item_start + (self.memorial_width_px / 2)

        # Y positions for text (relative to y_item_start, needs careful check with viewbox)
        # Original: line1_y = y + 29 / self.page_height_mm * self.viewbox_height
        # This implies Y positions were calculated based on overall page/viewbox ratios, not item-relative mm.
        # For now, using fixed pixel offsets from item top, which is more robust if y_item_start is correct.
        # These offsets might need to be derived from original visual inspection if logic was complex.
        # Let's assume: Line 1 near top, Line 2 middle, Line 3 near bottom of the item.
        # Approximate mm offsets from item top for text lines:
        line1_y_offset_mm = 25
        line2_y_offset_mm = self.memorial_height_mm / 2  # Centered
        line3_y_offset_mm = self.memorial_height_mm - 25 # Approx 25mm from bottom

        # Graphics embedding
        graphic_filename = str(order_details.get('graphic', '')).strip()
        if graphic_filename:
            graphic_full_path = os.path.join(self.graphics_path, graphic_filename)
            if os.path.exists(graphic_full_path):
                embedded_image_data = self.svg_utils.embed_image(graphic_full_path) # SVGUtils
                if embedded_image_data:
                    dwg.add(dwg.image(href=embedded_image_data, insert=(x_item_start, y_item_start),
                                      size=(self.memorial_width_px, self.memorial_height_px)))
                else:
                    print(f"Warning: Failed to embed graphic {graphic_filename} for order {order_details.get('order-id')}")
            else:
                print(f"Warning: Graphic file not found: {graphic_full_path} for order {order_details.get('order-id')}")

        # Text lines
        # Line 1
        text_l1 = str(order_details.get('line_1', '')).strip()
        if text_l1:
            self.svg_utils.add_text(dwg, text_l1, insert_x=center_x_abs,
                                    insert_y=y_item_start + (line1_y_offset_mm * self.px_per_mm), # Convert mm offset to px
                                    font_size_px=self.line1_font_size_px, # Directly use px if defined as such
                                    font_family="Georgia", text_anchor="middle", fill="black")
        # Line 2
        text_l2 = str(order_details.get('line_2', '')).strip()
        if text_l2:
            self.svg_utils.add_text(dwg, text_l2, insert_x=center_x_abs,
                                    insert_y=y_item_start + (line2_y_offset_mm * self.px_per_mm),
                                    font_size_px=self.line2_font_size_px,
                                    font_family="Georgia", text_anchor="middle", fill="black")
        # Line 3 (potentially multi-line)
        text_l3 = str(order_details.get('line_3', '')).strip()
        if text_l3:
            # Original used self.wrap_text(). Assuming TextUtils provides similar.
            # Max chars for large stake text line might be different.
            # For now, using a generic split and simple multi-line add.
            # A more sophisticated approach from TextUtils would be better.
            # lines = self.text_utils.wrap_text(text_l3, width=30) # Example width
            lines = self.text_utils.split_line_to_fit_multiline(text_l3, max_chars_per_line=30, max_lines=3) # Example

            current_y_for_l3 = y_item_start + (line3_y_offset_mm * self.px_per_mm)
            # Original line_spacing was 47.11817 px. This is approx 12.5mm at 3.78px/mm.
            line_spacing_px = 12.5 * self.px_per_mm

            self.svg_utils.add_multiline_text(dwg, lines, insert_x=center_x_abs, insert_y=current_y_for_l3,
                                              font_size_px=self.line3_font_size_px, font_family="Georgia",
                                              text_anchor="middle", fill="black", line_spacing_px=line_spacing_px)

    def _create_memorial_page_svg(self, orders_on_page: list, filename: str):
        output_path = os.path.join(self.output_dir, filename)
        dwg = svgwrite.Drawing(filename=output_path, size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                               viewBox=f"0 0 {self.viewbox_width} {self.viewbox_height}")

        for idx, order_item_details in enumerate(orders_on_page):
            if idx >= self.batch_size: break # Max 2 items for this processor

            item_x = self.item_x_offset_px + (idx * self.item_spacing_x_px)
            item_y = self.item_y_offset_px # All items in the same row for this processor

            self._add_item_to_svg_page(dwg, item_x, item_y, order_item_details)

        # Add reference point (blue pixel in bottom right, from original SVG sample)
        # Coordinates are specific to the viewbox
        dwg.add(dwg.rect(insert=(1661.6220472, 1094.8876867919998),
                         size=(0.37795280000000003, 0.37795280000000003), fill="blue"))
        try:
            dwg.save(pretty=True)
            print(f"B&W Large Stake SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving B&W Large Stake SVG {output_path}: {e}")

# Register the processor
register_processor("bw_large_stakes", BWLargeStakesProcessor)

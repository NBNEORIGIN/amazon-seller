import os
import svgwrite
import pandas as pd
from datetime import datetime

from core.processors.base import ProcessorBase
from core.processors import register_processor
from core.processors.text_utils import TextUtils
from core.processors.svg_utils import SVGUtils
from .text_utils import create_batch_csv # Changed to import from local text_utils

class ColouredLargeStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = TextUtils()
        self.svg_utils = SVGUtils()

        self.CATEGORY = 'COLOURED_LARGE_STAKES'
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # SVG/page dimensions
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.viewbox_width = 1662  # Effective pixel width for content
        self.viewbox_height = 1095 # Effective pixel height for content

        # Memorial item geometry
        self.memorial_width_px = 755.42004
        self.memorial_height_px = 453.1008
        self.corner_radius_px = 22.012239
        self.stroke_width_px = 0.378046

        # Text sizes (original uses 'pt' but applies them as 'px' in f-string)
        # Storing as pixel values for direct use, assuming original intent was pixel size.
        self.line1_font_size_px = 45.33
        self.line2_font_size_px = 66.67
        self.line3_font_size_px = 32

        # Grid layout (2x2) for up to 4 items
        self.grid_cols = 2
        self.grid_rows = 2
        self.batch_size = self.grid_cols * self.grid_rows

        # Positioning: items are placed based on a specific order, not simple grid iteration.
        # Original 'positions' list: bottom-right, bottom-left, top-right, top-left.
        # These are top-left coordinates for each of the 4 slots in that order.
        self.item_positions_px = [
            (150.59 + 755.80, 641.97), # Slot 0 (Original bottom-right)
            (150.59, 641.97),          # Slot 1 (Original bottom-left)
            (150.59 + 755.80, 641.97 - 453.10), # Slot 2 (Original top-right)
            (150.59, 641.97 - 453.10),          # Slot 3 (Original top-left)
        ]
        self.px_per_mm = self.viewbox_width / self.page_width_mm # Calculate for theme adjustments

    def is_applicable(self, order_data: pd.Series) -> bool:
        order_type = str(order_data.get('type', '')).strip().lower()
        colour = str(order_data.get('colour', '')).strip().lower()
        decoration_type = str(order_data.get('decorationtype', '')).strip().lower()

        allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble']

        return (order_type == 'large stake' and
                colour in allowed_colours and
                decoration_type == 'graphic')

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        self.output_dir = output_dir
        self.graphics_path = graphics_path
        os.makedirs(self.output_dir, exist_ok=True)

        if order_data.empty:
            print("No Coloured Large Stakes orders to process.")
            return

        df_to_process = order_data.copy()
        # Original used uppercase TYPE, COLOUR. Ensuring consistency if input varies.
        df_to_process.columns = [col.upper() for col in df_to_process.columns]


        print(f"Processing {len(df_to_process)} Coloured Large Stakes.")

        batch_num = 1
        total_items = len(df_to_process)

        for start_idx in range(0, total_items, self.batch_size): # self.batch_size is 4
            end_idx = min(start_idx + self.batch_size, total_items)
            current_batch_df = df_to_process.iloc[start_idx:end_idx]

            if not current_batch_df.empty:
                orders_for_svg_page = current_batch_df.to_dict('records')

                filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}_No_Jig.svg" # Original had "_No Jig"

                self._create_memorial_page_svg(orders_for_svg_page, filename)
                create_batch_csv(orders_for_svg_page, batch_num, self.CATEGORY, self.output_dir, self.date_str)
                batch_num += 1

    def _add_item_to_svg_page(self, dwg, x_item_start: float, y_item_start: float, order_details: dict):
        """Adds a single Coloured Large Stake item to the SVG drawing."""

        # Item background and outline
        # Original fill was 'white', could be dynamic based on order_details['COLOUR'] if needed
        self.svg_utils.draw_rounded_rect(dwg, insert=(x_item_start, y_item_start),
                                         size=(self.memorial_width_px, self.memorial_height_px),
                                         rx=self.corner_radius_px, ry=self.corner_radius_px,
                                         fill='white', stroke='red', stroke_width=self.stroke_width_px)

        # Graphic
        graphic_filename = str(order_details.get('GRAPHIC', '')).strip() # Original used uppercase keys
        if graphic_filename:
            graphic_full_path = os.path.join(self.graphics_path, graphic_filename)
            if os.path.exists(graphic_full_path):
                embedded_image_data = self.svg_utils.embed_image(graphic_full_path)
                if embedded_image_data:
                    dwg.add(dwg.image(href=embedded_image_data, insert=(x_item_start, y_item_start),
                                      size=(self.memorial_width_px, self.memorial_height_px)))
            else:
                print(f"Warning: Graphic file not found: {graphic_full_path}")

        # Text
        center_x_abs = x_item_start + self.memorial_width_px / 2

        theme = str(order_details.get('THEME', '')).strip().lower()
        y1_offset_px = 80 # Default base offset from item top for line 1 text
        y2_offset_px = 180 # Default base offset from item top for line 2 text
        current_line2_font_size_px = self.line2_font_size_px

        if theme == 'islamic':
            y1_offset_px += 40 * self.px_per_mm
            y2_offset_px += 30 * self.px_per_mm
            current_line2_font_size_px *= 0.5

        y1_abs = y_item_start + y1_offset_px
        y2_abs = y_item_start + y2_offset_px
        y3_abs = y_item_start + 260 # Original fixed offset for line 3

        text_l1 = self.text_utils.check_grammar_and_typos(str(order_details.get('LINE_1', '')))
        lines_l1 = self.text_utils.split_line_to_fit(text_l1, 30) # Assuming 30 char width
        self.svg_utils.add_multiline_text_svgwrite(dwg, lines_l1, insert=(center_x_abs, y1_abs),
                                          font_size_px=self.line1_font_size_px, font_family="Georgia",
                                          text_anchor="middle", fill="black")

        text_l2 = self.text_utils.check_grammar_and_typos(str(order_details.get('LINE_2', '')))
        lines_l2 = self.text_utils.split_line_to_fit(text_l2, 30)
        self.svg_utils.add_multiline_text_svgwrite(dwg, lines_l2, insert=(center_x_abs, y2_abs),
                                          font_size_px=current_line2_font_size_px, font_family="Georgia",
                                          text_anchor="middle", fill="black")

        text_l3 = self.text_utils.check_grammar_and_typos(str(order_details.get('LINE_3', '')))
        lines_l3 = self.text_utils.split_line_to_fit(text_l3, 30)
        self.svg_utils.add_multiline_text_svgwrite(dwg, lines_l3, insert=(center_x_abs, y3_abs),
                                          font_size_px=self.line3_font_size_px, font_family="Georgia",
                                          text_anchor="middle", fill="black", line_spacing_px=(47.11817)) # Original spacing


    def _create_memorial_page_svg(self, orders_on_page: list, filename: str):
        output_path = os.path.join(self.output_dir, filename)
        dwg = svgwrite.Drawing(filename=output_path, size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
                               viewBox=f"0 0 {self.viewbox_width} {self.viewbox_height}")

        for idx, order_item_details in enumerate(orders_on_page):
            if idx >= len(self.item_positions_px): break # Max 4 items based on defined positions

            item_x_px, item_y_px = self.item_positions_px[idx]
            self._add_item_to_svg_page(dwg, item_x_px, item_y_px, order_item_details)

        # Reference point (specific coordinates from original)
        blue_square_x = self.viewbox_width - 0.38
        blue_square_y = self.viewbox_height - 0.38 + (0.05 * self.px_per_mm) # Adjusted Y
        dwg.add(dwg.rect(insert=(blue_square_x, blue_square_y), size=(0.38, 0.38), fill="blue"))

        try:
            dwg.save(pretty=True)
            print(f"Coloured Large Stake SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving Coloured Large Stake SVG {output_path}: {e}")

# Register the processor
register_processor("coloured_large_stakes", ColouredLargeStakesProcessor)

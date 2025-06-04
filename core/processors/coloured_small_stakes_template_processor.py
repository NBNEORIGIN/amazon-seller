import os
import pandas as pd
import svgwrite # Used directly by the original populate_svg
from datetime import datetime
# xml.etree.ElementTree is not used by the current populate_svg, so omitting for now.
# import xml.etree.ElementTree as ET

from core.processors.base import ProcessorBase
from core.processors import register_processor
from core.processors.text_utils import TextUtils
from core.processors.svg_utils import SVGUtils
from .text_utils import create_batch_csv # Changed to import from local text_utils

class ColouredSmallStakesTemplateProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str, template_path: str = None): # template_path is optional
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        # The template_path was in original __init__ but not used by populate_svg.
        # If true template XML manipulation is intended later, this would be used to load it.
        self.template_path = template_path
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = TextUtils()
        self.svg_utils = SVGUtils()

        self.CATEGORY = "COLOURED_SMALL_STAKES"
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.batch_size = 9  # 3x3 grid for these items

        # Page and item dimensions from original populate_svg
        self.page_w_mm = 480
        self.page_h_mm = 290
        self.item_w_mm = 108
        self.item_h_mm = 75
        self.item_corner_r_mm = 6

        # Grid layout (3x3), populated bottom-right to top-left
        self.grid_cols = 3
        self.grid_rows = 3

        # Calculate top-left of the overall grid (which itself is bottom-right aligned on page)
        grid_total_w_mm = self.grid_cols * self.item_w_mm
        grid_total_h_mm = self.grid_rows * self.item_h_mm
        self.grid_start_x_mm = self.page_w_mm - grid_total_w_mm
        self.grid_start_y_mm = self.page_h_mm - grid_total_h_mm

        # Font related constants (original used pt and mm directly in svgwrite calls)
        self.font_family = "Georgia"
        self.pt_to_mm = 0.352778 # For converting pt font sizes if needed by SVGUtils

    def is_applicable(self, order_data: pd.Series) -> bool:
        order_type = str(order_data.get('type', '')).strip().lower()
        colour = str(order_data.get('colour', '')).strip().lower()
        decoration_type = str(order_data.get('decorationtype', '')).strip().lower()

        type_synonyms = {'small stake', 'small metal', 'small', 'mini', 'mini stake'}
        # Prompt includes 'black', original filtered for non-black 'coloured'. Following prompt.
        allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble', 'black']

        return (order_type in type_synonyms and
                colour in allowed_colours and
                decoration_type == 'graphic')

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        self.output_dir = output_dir
        self.graphics_path = graphics_path
        os.makedirs(self.output_dir, exist_ok=True)

        if order_data.empty:
            print("No Coloured Small Stakes orders to process.")
            return

        df_to_process = order_data.copy()
        print(f"Processing {len(df_to_process)} Coloured Small Stakes.")

        batch_num = 1
        total_items = len(df_to_process)

        for start_idx in range(0, total_items, self.batch_size):
            end_idx = min(start_idx + self.batch_size, total_items)
            current_batch_df = df_to_process.iloc[start_idx:end_idx]

            if not current_batch_df.empty:
                # Filename generation
                # For this processor, it always generates a batch page even for a single item.
                filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"

                self._generate_svg_page_for_batch(current_batch_df, filename)

                create_batch_csv(current_batch_df.to_dict('records'), batch_num, self.CATEGORY, self.output_dir, self.date_str)
                # The old direct to_csv call is now replaced by the utility.
                # csv_out_path = os.path.join(self.output_dir, os.path.splitext(filename)[0] + ".csv")
                # current_batch_df.to_csv(csv_out_path, index=False, encoding="utf-8-sig")
                # print(f"Wrote batch CSV: {csv_out_path}")
                batch_num += 1

    def _generate_svg_page_for_batch(self, batch_orders_df: pd.DataFrame, filename: str):
        """
        Generates an SVG page for a batch of orders using svgwrite,
        replicating the layout from the original populate_svg method.
        """
        output_svg_path = os.path.join(self.output_dir, filename)

        dwg = svgwrite.Drawing(
            filename=output_svg_path,
            size=(f"{self.page_w_mm}mm", f"{self.page_h_mm}mm"),
            viewBox=f"0 0 {self.page_w_mm} {self.page_h_mm}" # Viewbox in mm
        )

        # Draw each memorial item (bottom row first, right to left)
        for idx, (_, order_series) in enumerate(batch_orders_df.iterrows()):
            if idx >= self.batch_size: # Should not exceed 9 items
                break

            # Grid population order: bottom-to-top, right-to-left
            row_visual = self.grid_rows - 1 - (idx // self.grid_cols)
            col_visual = self.grid_cols - 1 - (idx % self.grid_cols)

            item_x_mm = self.grid_start_x_mm + (col_visual * self.item_w_mm)
            item_y_mm = self.grid_start_y_mm + (row_visual * self.item_h_mm)

            # Draw red rounded rectangle (item boundary)
            dwg.add(dwg.rect(insert=(f"{item_x_mm}mm", f"{item_y_mm}mm"),
                             size=(f"{self.item_w_mm}mm", f"{self.item_h_mm}mm"),
                             rx=f"{self.item_corner_r_mm}mm", ry=f"{self.item_corner_r_mm}mm",
                             fill='none', stroke='red', stroke_width='0.1mm'))

            # Graphic
            graphic_filename = str(order_series.get('graphic', '')).strip()
            if graphic_filename and self.graphics_path:
                graphic_full_path = os.path.join(self.graphics_path, graphic_filename)
                if os.path.exists(graphic_full_path):
                    # embed_image_to_group might be too specific if no group exists in template.
                    # A simpler embed_image that returns data URI is fine for svgwrite.
                    embedded_image_data_uri = self.svg_utils.embed_image(graphic_full_path)
                    if embedded_image_data_uri:
                        dwg.add(dwg.image(href=embedded_image_data_uri,
                                          insert=(f"{item_x_mm}mm", f"{item_y_mm}mm"), # Position within item boundary
                                          size=(f"{self.item_w_mm}mm", f"{self.item_h_mm}mm"), # Size to fill item
                                          preserveAspectRatio='xMidYMid meet'))

            # Text
            item_center_x_mm = item_x_mm + self.item_w_mm / 2
            item_center_y_mm = item_y_mm + self.item_h_mm / 2

            # Line 1: 3.33pt, 15mm above item center
            text_l1 = self.text_utils.check_grammar_and_typos(str(order_series.get('line_1', '')))
            lines_l1 = self.text_utils.split_line_to_fit(text_l1, 30)
            self.svg_utils.add_multiline_text_svgwrite(dwg, lines_l1,
                                              insert=(f"{item_center_x_mm}mm", f"{item_center_y_mm - 15}mm"),
                                              font_size_pt=3.33, font_family=self.font_family,
                                              text_anchor="middle", fill="black")

            # Line 2: 2.5mm font size, centered in item
            text_l2 = self.text_utils.check_grammar_and_typos(str(order_series.get('line_2', '')))
            lines_l2 = self.text_utils.split_line_to_fit(text_l2, 30)
            self.svg_utils.add_multiline_text_svgwrite(dwg, lines_l2,
                                              insert=(f"{item_center_x_mm}mm", f"{item_center_y_mm}mm"),
                                              font_size_mm=2.5, font_family=self.font_family, # Directly in mm
                                              text_anchor="middle", fill="black")

            # Line 3: 3.33pt, 10mm below item center
            text_l3 = self.text_utils.check_grammar_and_typos(str(order_series.get('line_3', '')))
            lines_l3 = self.text_utils.split_line_to_fit(text_l3, 30)
            self.svg_utils.add_multiline_text_svgwrite(dwg, lines_l3,
                                              insert=(f"{item_center_x_mm}mm", f"{item_center_y_mm + 10}mm"),
                                              font_size_pt=3.33, font_family=self.font_family,
                                              text_anchor="middle", fill="black")

        # UV printer reference blue square (bottom-right of page)
        blue_square_size_mm = 0.1
        dwg.add(dwg.rect(insert=(f"{self.page_w_mm - blue_square_size_mm}mm", f"{self.page_h_mm - blue_square_size_mm}mm"),
                         size=(f"{blue_square_size_mm}mm", f"{blue_square_size_mm}mm"), fill='blue'))

        try:
            dwg.save(pretty=True)
            print(f"Generated SVG page: {output_svg_path}")
        except Exception as e:
            print(f"Error saving SVG {output_svg_path}: {e}")

# Register the processor
register_processor("coloured_small_stakes", ColouredSmallStakesTemplateProcessor)

import os
import svgwrite
import pandas as pd
from datetime import datetime # Keep for potential use in filename generation
from pathlib import Path

from core.processors.base import ProcessorBase
from core.processors import register_processor
from . import text_utils # Changed to module import
from . import svg_utils   # Changed to module import
# Removed specific create_batch_csv import, will use text_utils.create_batch_csv

class RegularStakesProcessor(ProcessorBase):
    def __init__(self, graphics_path: str, output_dir: str):
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.text_utils = text_utils # Assign module
        self.svg_utils = svg_utils     # Assign module

        # Constants from original class (might need refactoring or be part of SVGUtils)
        self.CATEGORY = 'COLOUR' # Used in original filename, might need to be dynamic
        self.grid_cols = 3
        self.grid_rows = 3
        self.batch_size = self.grid_cols * self.grid_rows # Page generation logic

        # Conversion factors
        self.px_per_mm = 1 / 0.26458333333
        self.pt_to_mm = 0.2645833333

        # Memorial and page dimensions (specific to this processor's output format)
        self.memorial_width_mm = 140
        self.memorial_height_mm = 90
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        self.memorial_width_px = self.memorial_width_mm * self.px_per_mm
        self.memorial_height_px = self.memorial_height_mm * self.px_per_mm
        self.page_width_px = self.page_width_mm * self.px_per_mm
        self.page_height_px = self.page_height_mm * self.px_per_mm

        # Centering offsets for page grid
        grid_width_mm = self.memorial_width_mm * self.grid_cols
        grid_height_mm = self.memorial_height_mm * self.grid_rows
        self.x_offset_mm = (self.page_width_mm - grid_width_mm) / 2
        self.y_offset_mm = (self.page_height_mm - grid_height_mm) / 2
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)

        # Text sizes (in points)
        self.line1_size_pt = 17 * 1.2
        self.line2_size_pt = 25 * 1.2
        self.line3_size_pt = 12 * 1.1

        # Stroke width and corner radius
        self.stroke_width = 0.1 * self.px_per_mm
        self.corner_radius_px = 6 * self.px_per_mm

        # Date string for batch naming (from MemorialBase)
        self.date_str = datetime.now().strftime("%Y%m%d_%H%M%S")


    def is_applicable(self, order_data: pd.Series) -> bool:
        order_data_lower = order_data.rename(index=str.lower) # Ensure case-insensitivity for column names

        type_ = str(order_data_lower.get('type', '')).strip().lower()
        colour = str(order_data_lower.get('colour', '')).strip().lower()
        decorationtype = str(order_data_lower.get('decorationtype', '')).strip().lower()
        sku = str(order_data_lower.get('sku', '')).strip().lower() # Get SKU for special cases

        allowed_types = ['regular stake', 'regular plaque']
        allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble']

        # Special SKU OM008021 is mentioned in the original script's create_memorial_svg.
        # This SKU seems to bypass some standard rules and use a specific graphic.
        # If it's OM008021, we can consider it applicable for this processor
        # as the original script had specific handling for it within this processor's drawing logic.
        if sku == 'om008021':
            return True

        # Standard applicability check
        type_is_valid = type_ in allowed_types
        colour_is_valid = colour in allowed_colours
        decoration_is_valid = decorationtype != 'photo' # Any decoration type other than 'photo'

        return type_is_valid and colour_is_valid and decoration_is_valid

    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str):
        self.output_dir = output_dir
        self.graphics_path = graphics_path # Ensure instance variables are current
        os.makedirs(self.output_dir, exist_ok=True)

        # order_data is already pre-filtered by is_applicable by the main GUI loop
        # However, the original script had further processing and filtering (qty expansion, specific SKU lists)

        if order_data.empty:
            print(f"[{self.CATEGORY}] No orders passed initial is_applicable check.")
            return

        # Make a copy to avoid SettingWithCopyWarning
        df = order_data.copy()

        # Normalize column names (already done in is_applicable for its checks, but good practice here too for safety)
        df.columns = [col.lower().strip() for col in df.columns]

        # 1. Expand rows by 'number-of-items'
        expanded_rows = []
        for _, row in df.iterrows():
            try:
                # Ensure 'number-of-items' exists and is a valid integer
                qty = int(row.get('number-of-items', 1))
                qty = max(qty, 1) # Ensure quantity is at least 1
            except (ValueError, TypeError):
                qty = 1
            for _ in range(qty):
                expanded_rows.append(row.copy())

        if not expanded_rows:
            print(f"[{self.CATEGORY}] No orders after expansion (or empty initial list).")
            return
        df_expanded = pd.DataFrame(expanded_rows)

        # Re-apply is_applicable filters here to the expanded list, or ensure initial data is clean.
        # The is_applicable in the GUI filters the original list.
        # Here, we are processing the already filtered (and now expanded) list.
        # The original script re-filtered after expansion. Let's stick to that for now.
        # This means is_applicable's conditions are checked again on potentially duplicated rows.

        # The original script's filtering logic was:
        # allowed_types = ['regular stake', 'regular plaque']
        # allowed_colours = ['copper', 'gold', 'silver', 'stone', 'marble']
        # special_skus = ['om008021'] # This is now part of is_applicable

        # df_expanded['type'] = df_expanded['type'].astype(str).str.strip().str.lower()
        # df_expanded['colour'] = df_expanded['colour'].astype(str).str.strip().str.lower()
        # df_expanded['decorationtype'] = df_expanded['decorationtype'].astype(str).str.strip().str.lower()
        # df_expanded['sku'] = df_expanded['sku'].astype(str).str.strip().str.lower()

        # The is_applicable method will be used by the main loop, so df_expanded should already conform
        # to the general rules. The main additional filtering here is the photo SKU exclusion.

        # 2. Exclude photo SKUs based on SKULIST.csv
        # This logic is critical and was in the original script.
        try:
            # Determine project root to find assets/SKULIST.csv
            # Assumes this processor file is in core/processors/
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            skulist_path = os.path.join(project_root, 'assets', 'SKULIST.csv')

            if not os.path.exists(skulist_path):
                print(f"Warning: SKULIST.csv not found at {skulist_path}. Cannot perform photo SKU exclusion.")
                skulist_df = pd.DataFrame(columns=['sku', 'type', 'decorationtype']) # Empty DataFrame
            else:
                skulist_df = pd.read_csv(skulist_path)

            skulist_df.columns = [col.lower().strip() for col in skulist_df.columns]

            # Ensure necessary columns exist in skulist_df
            if 'sku' not in skulist_df.columns: skulist_df['sku'] = pd.NA
            if 'type' not in skulist_df.columns: skulist_df['type'] = ''
            if 'decorationtype' not in skulist_df.columns: skulist_df['decorationtype'] = ''

            skulist_df['sku'] = skulist_df['sku'].astype(str).str.strip().str.lower()
            skulist_df['type'] = skulist_df['type'].astype(str).str.strip().str.lower()
            skulist_df['decorationtype'] = skulist_df['decorationtype'].astype(str).str.strip().str.lower()

            # Identify SKUs that are 'regular stake' or 'regular plaque' but are 'photo' decoration type
            photo_skus_to_exclude = set(
                skulist_df[
                    (skulist_df['type'].isin(['regular stake', 'regular plaque'])) &
                    (skulist_df['decorationtype'] == 'photo')
                ]['sku']
            )

            if photo_skus_to_exclude:
                print(f"[{self.CATEGORY}] Photo SKUs identified for exclusion: {photo_skus_to_exclude}")
                # Ensure 'sku' column exists in df_expanded before attempting to filter
                if 'sku' in df_expanded.columns:
                    df_expanded['sku_lower'] = df_expanded['sku'].astype(str).str.strip().str.lower()
                    # Exclude these photo SKUs, unless it's the special 'om008021' (which is handled by is_applicable)
                    initial_count = len(df_expanded)
                    df_expanded = df_expanded[
                        (~df_expanded['sku_lower'].isin(photo_skus_to_exclude)) | (df_expanded['sku_lower'] == 'om008021')
                    ]
                    print(f"[{self.CATEGORY}] {initial_count - len(df_expanded)} orders excluded due to photo SKU list (retaining om008021 if present).")
                else:
                    print(f"[{self.CATEGORY}] Warning: 'sku' column not found in order data. Cannot perform photo SKU exclusion.")

        except Exception as e:
            print(f"[{self.CATEGORY}] Error during SKULIST.csv processing for photo SKU exclusion: {e}")
            # Continue without this specific exclusion if SKULIST processing fails

        final_filtered_df = df_expanded

        if final_filtered_df.empty:
            print(f"[{self.CATEGORY}] No orders remaining after all processing and filtering steps.")
            return

        # 3. Sort by color_priority
        color_priority = {'copper': 0, 'gold': 1, 'silver': 2, 'stone': 3, 'marble': 4}
        # Ensure 'colour' column exists before mapping
        if 'colour' in final_filtered_df.columns:
            final_filtered_df['color_priority'] = final_filtered_df['colour'].map(color_priority)
            # Sort, placing NaNs (if any from map) last or first, then drop helper column
            final_filtered_df = final_filtered_df.sort_values('color_priority', na_position='last').drop(columns=['color_priority'])
        else:
            print(f"[{self.CATEGORY}] Warning: 'colour' column not found for sorting.")


        # Batching logic (from original refactoring, should be okay)
        items_per_page = self.grid_cols * self.grid_rows
        batch_num = 1
        total_items = len(final_filtered_df)

        print(f"[{self.CATEGORY}] Processing {total_items} items in batches of {items_per_page}.")

        for i in range(0, total_items, items_per_page):
            batch_df = final_filtered_df.iloc[i:i + items_per_page]
            if not batch_df.empty:
                # The _create_memorial_page_svg expects a list of dicts
                orders_dict_list = batch_df.to_dict('records')

                # Filename generation logic from previous version of process method
                if len(orders_dict_list) == 1:
                    order = orders_dict_list[0]
                    order_id = str(order.get('order-id', 'NO_ID')).strip()
                    sku = str(order.get('sku', 'NO_SKU')).strip()
                    graphic_val = str(order.get('graphic', 'NO_GRAPHIC')).strip().replace('.png', '')
                    filename = f"REGULAR_{order_id}_{sku}_{graphic_val}.svg"
                    self._create_memorial_page_svg(orders_dict_list, batch_num, filename)
                else:
                    page_filename = f"{self.CATEGORY}_batch_{self.date_str}_{batch_num:03d}.svg"
                    self._create_memorial_page_svg(orders_dict_list, batch_num, page_filename)

                # Use the centralized CSV creation utility via the text_utils module
                self.text_utils.create_batch_csv(orders_dict_list, batch_num, self.CATEGORY, self.output_dir, self.date_str)
                batch_num += 1

        print(f"[{self.CATEGORY}] processing complete. {total_items} items processed into {batch_num - 1} SVG/CSV file(s).")

    def _create_memorial_page_svg(self, orders_in_batch: list, batch_number: int, filename: str):
        """
        Creates a single SVG page with multiple memorials from the batch.
        orders_in_batch: A list of order dictionaries for the current page.
        batch_number: The current batch number (for logging).
        filename: The desired filename for the SVG.
        """
        output_path = os.path.join(self.output_dir, filename)

        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.page_width_mm}mm", f"{self.page_height_mm}mm"),
            viewBox=f"0 0 {self.page_width_px} {self.page_height_px}"
        )

        for idx_in_page in range(len(orders_in_batch)): # Iterate only for actual orders in batch
            order_item = orders_in_batch[idx_in_page]

            row_on_page = idx_in_page // self.grid_cols
            col_on_page = idx_in_page % self.grid_cols

            x_pos = self.x_offset_px + (col_on_page * self.memorial_width_px)
            y_pos = self.y_offset_px + (row_on_page * self.memorial_height_px)

            # Draw placeholder rect for the item slot (optional, for debugging)
            dwg.add(dwg.rect(
                insert=(x_pos, y_pos),
                size=(self.memorial_width_px, self.memorial_height_px),
                rx=self.corner_radius_px,
                ry=self.corner_radius_px,
                fill='none',
                stroke='grey', # Changed from red to grey
                stroke_width=self.stroke_width / 2 # Thinner
            ))

            # --- Apply graphic ---
            # TODO: self.embed_image was from MemorialBase. This needs to be SVGUtils.embed_image or similar.
            # For now, assuming self.svg_utils.embed_image(path) exists.
            graphic_filename = str(order_item.get('graphic', '')).strip()
            if graphic_filename:
                # Special handling for OM008021 (if still needed, though is_applicable should filter it out if it's B&W)
                # This processor is for COLOUR regular stakes. OM008021 might be B&W.
                # The original logic had a hardcoded G: drive path which is not portable.
                # Assuming graphics are found via self.graphics_path
                if graphic_filename.upper() == 'OM008021.PNG' or graphic_filename.upper() == 'OM008021':
                     # This SKU might need special handling or its own processor if rules are complex.
                     # For now, treat as a regular graphic if found in graphics_path.
                     pass # Let it be handled by the generic graphic logic below.

                graphic_full_path = os.path.join(self.graphics_path, graphic_filename)
                if os.path.exists(graphic_full_path):
                    # Define insert and size for the image
                    img_insert_pos = (x_pos, y_pos)
                    img_size = (self.memorial_width_px, self.memorial_height_px)

                    # Call embed_image correctly
                    img_obj = self.svg_utils.embed_image(
                        dwg,
                        image_path=graphic_full_path,
                        insert=img_insert_pos,
                        size=img_size
                        # defs=dwg.defs # Optional for pixelated style
                    )
                    if img_obj is None:
                        # The embed_image function itself prints warnings for not found / errors
                        print(f"Further Warning: Embedding graphic {graphic_filename} failed for order {order_item.get('order-id')}")
                # embed_image handles "not found" case, so no specific else needed here for that.

            # --- Add Text ---
            center_x_abs = x_pos + (self.memorial_width_px / 2)

            for line_key, y_offset_mm, font_size_pt, max_chars_override in [
                ('line_1', 28, self.line1_size_pt, None),
                ('line_2', 45, self.line2_size_pt, None),
                ('line_3', 57, self.line3_size_pt, 30) # line_3 has special multiline logic
            ]:
                text_content = str(order_item.get(line_key, '')).strip()
                if not text_content: # Skip empty lines
                    continue

                # Grammar/Typo check (from TextUtils)
                # text_content = self.text_utils.check_grammar_and_typos(text_content) # Assuming this method exists

                font_family = "Georgia" # TODO: Make configurable or part of TextUtils
                fill_color = "black"    # TODO: Make configurable

                if line_key == 'line_3':
                    # Special multiline handling for line_3
                    font_size_mm = font_size_pt * self.pt_to_mm
                    char_width_approx_mm = 0.5 * font_size_mm # Rough estimation
                    max_line_width_mm = self.memorial_width_mm * 0.6 # 60% of memorial width

                    # Use max_chars_override if provided (e.g. 30 for single line before splitting)
                    # otherwise calculate based on available width
                    effective_max_chars = max_chars_override if max_chars_override else int(max_line_width_mm / char_width_approx_mm)

                    lines_to_draw = self.text_utils.split_line_to_fit_multiline(text_content, effective_max_chars, 5) # Max 5 lines for line_3

                    # Conditional font size for Line 3 based on original logic
                    total_chars_line3 = sum(len(line) for line in lines_to_draw)
                    if 10 <= total_chars_line3 <= 30 and len(lines_to_draw) <=2 : # Adjusted logic
                        current_font_size_pt = self.line1_size_pt
                    elif 31 <= total_chars_line3 <= 90 and len(lines_to_draw) <=3: # Adjusted logic
                        current_font_size_pt = self.line1_size_pt * 0.9
                    else:
                        current_font_size_pt = font_size_pt # Default line3_size_pt

                    if lines_to_draw:
                        self.svg_utils.add_multiline_text(
                            dwg, lines_to_draw,
                            insert_x=center_x_abs, insert_y=(y_pos + y_offset_mm * self.px_per_mm),
                            font_size_mm=(current_font_size_pt * self.pt_to_mm), # Use font_size_mm
                            font_family=font_family, text_anchor="middle", fill=fill_color
                        )
                else: # line_1, line_2 (single line centered)
                     self.svg_utils.add_multiline_text(
                         dwg,
                         lines=[text_content], # Pass the single line as a list
                         insert_x=center_x_abs,
                         insert_y=(y_pos + y_offset_mm * self.px_per_mm),
                         font_size_mm=(font_size_pt * self.pt_to_mm), # Use font_size_mm
                         font_family=font_family,
                         text_anchor="middle",
                         fill=fill_color
                     )

        # Add reference point (bottom right corner of the page)
        ref_size_px = 0.1 * self.px_per_mm
        dwg.add(dwg.rect(
            insert=(self.page_width_px - ref_size_px, self.page_height_px - ref_size_px),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))

        try:
            dwg.save(pretty=True) # pretty=True for readable SVG
            print(f"SVG page generated: {output_path}")
        except Exception as e:
            print(f"Error saving SVG {output_path}: {e}")

# Register the processor
register_processor("regular_stakes", RegularStakesProcessor)

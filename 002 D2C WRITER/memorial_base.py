import pandas as pd
import svgwrite

import os
from svgwrite import mm
import textwrap
import sys
from pathlib import Path
import base64
import mimetypes
from datetime import datetime
# Removed: import language_tool_python

class MemorialBase:
    def __init__(self, graphics_path, output_dir):
        
        # Conversion factors
        self.px_per_mm = 1 / 0.26458333333
        self.pt_to_mm = 0.2645833333
        
        # Memorial dimensions
        self.memorial_width_mm = 140
        self.memorial_height_mm = 90
        
        # Page dimensions
        self.page_width_mm = 439.8
        self.page_height_mm = 289.9
        
        # Convert all dimensions to pixels for viewBox
        self.memorial_width_px = int(self.memorial_width_mm * self.px_per_mm)
        self.memorial_height_px = int(self.memorial_height_mm * self.px_per_mm)
        self.page_width_px = int(self.page_width_mm * self.px_per_mm)
        self.page_height_px = int(self.page_height_mm * self.px_per_mm)
        
        # Calculate centering offsets (for 3x3 grid by default)
        grid_width_mm = self.memorial_width_mm * 3
        grid_height_mm = self.memorial_height_mm * 3
        self.x_offset_mm = (self.page_width_mm - grid_width_mm) / 2
        self.y_offset_mm = (self.page_height_mm - grid_height_mm) / 2
        self.x_offset_px = int(self.x_offset_mm * self.px_per_mm)
        self.y_offset_px = int(self.y_offset_mm * self.px_per_mm)
        
        self.graphics_path = graphics_path
        self.OUTPUT_DIR = output_dir
        
        # Get current date for file naming
        self.date_str = datetime.now().strftime('%y%m%d')

    @staticmethod
    def generate_warnings(row): # Reverted: lang_tool parameter removed
        import re, datetime
        warnings = []
        # Standardized keys for text fields (original or similar logic)
        text_fields_to_check = ['LINE_1', 'LINE_2', 'LINE_3']

        # Existing regex checks (should be similar to the original pre-LT version)
        for key in text_fields_to_check:
            value = str(row.get(key, "")).strip()
            if value:
                if re.search(r"\s+[,\.]", value):
                    warnings.append(f"Punctuation: Extra space before comma/period in {key}")
                if re.search(r"[a-zA-Z],[a-zA-Z]", value) and not re.search(r"\b(?:Mrs|Mr|Ms)\.,[a-zA-Z]", value):
                    warnings.append(f"Punctuation: Missing space after comma in {key}")
                if "  " in value:
                    warnings.append(f"Spacing: Double space found in {key}")
                if re.search(r"\b(\w+) \1\b", value, re.IGNORECASE):
                    warnings.append(f"Grammar: Repeated word in {key}")

                if key in ['LINE_1', 'LINE_2'] and not value.istitle() and not value.isupper() and not value.islower():
                    if not re.match(r"^\d{1,2}\w{2} \w+ \d{4} ?-? ?\d{1,2}\w{2} \w+ \d{4}$", value):
                        if not re.match(r"^\d{4} ?-? ?\d{4}$", value):
                            warnings.append(f"Capitalization: Consider title case for {key}")

                date_pattern_flexible = r'\b(\d{1,2}[-/]\d{1,2}[-/](\d{2}|\d{4}))\b'
                # Corrected tuple unpacking: removed the underscore for the non-existent third group
                for date_match_str, year_str in re.findall(date_pattern_flexible, value):
                    try:
                        normalized_date_str = date_match_str.replace('-', '/')
                        if len(year_str) == 2:
                            parsed_dt = datetime.datetime.strptime(normalized_date_str, "%d/%m/%y")
                            if parsed_dt.year > datetime.datetime.now().year + 50:
                                parsed_dt = parsed_dt.replace(year=parsed_dt.year - 100)
                        else:
                            parsed_dt = datetime.datetime.strptime(normalized_date_str, "%d/%m/%Y")
                    except ValueError:
                        try:
                            if len(year_str) == 2:
                                parsed_dt = datetime.datetime.strptime(normalized_date_str, "%m/%d/%y")
                                if parsed_dt.year > datetime.datetime.now().year + 50:
                                    parsed_dt = parsed_dt.replace(year=parsed_dt.year - 100)
                            else:
                                parsed_dt = datetime.datetime.strptime(normalized_date_str, "%m/%d/%Y")
                        except ValueError:
                            continue

                    if parsed_dt.year > datetime.datetime.now().year :
                        warnings.append(f"Date: Possible future year {parsed_dt.year} in {key}: '{date_match_str}'")

        # Removed LanguageTool checks section entirely

        return "; ".join(warnings)

    # Corrected indentation for create_batch_csv, embed_image, wrap_text, add_reference_point
    # These methods should be at the same indentation level as __init__ and generate_warnings

    def create_batch_csv(self, orders, batch_num, category): # Reverted: lang_tool_instance_global parameter removed
        """Create CSV file for the batch with specified category prefix, matching regular_stakes.py logic and including all fields present in input orders."""
        filename = f"{category}_{self.date_str}_{batch_num:03d}.csv"
        filepath = os.path.join(self.OUTPUT_DIR, filename)

        all_keys = set()
        for order in orders:
            all_keys.update([k.upper() for k in order.keys()])

        svg_filename = f"{category}_{self.date_str}_{batch_num:03d}.svg"
        preferred_columns = [
            'SVG FILE', 'DESIGN FILE', 'ORDER-ID', 'ORDER-ITEM-ID', 'SKU', 'NUMBER-OF-ITEMS',
            'TYPE', 'COLOUR', 'GRAPHIC', 'LINE_1', 'LINE_2', 'LINE_3', 'THEME', 'WARNINGS'
        ]
        extra_columns = [col for col in all_keys if col not in preferred_columns]
        columns = preferred_columns + extra_columns

        data = []
        # Removed LanguageTool initialization and try/except block
        # Removed process_order_warnings helper function
        for order in orders:
            row = {}
            row['SVG FILE'] = svg_filename
            row['DESIGN FILE'] = f"{category}_{self.date_str}_{batch_num:03d}"
            for col in columns: # Corrected variable name from col_name_in_loop to col
                if col in ['SVG FILE', 'DESIGN FILE']:
                    continue
                val = order.get(col, order.get(col.lower(), order.get(col.upper(), '')))
                row[col] = val
            row['WARNINGS'] = MemorialBase.generate_warnings(order) # Reverted call
            data.append(row)

        df = pd.DataFrame(data)
        if not df.empty:
            present_columns = [col for col in columns if col in df.columns]
            df = df[present_columns]
        df.to_csv(filepath, index=False, encoding="utf-8")


    def embed_image(self, image_path):
        print(f"[embed_image] Original image_path: {image_path}")
        norm_path = os.path.normpath(image_path)
        print(f"[embed_image] Normalized image_path: {norm_path}")
        exists = os.path.exists(norm_path)
        print(f"[embed_image] File exists: {exists}")
        try:
            mime_type = mimetypes.guess_type(norm_path)[0]
            if mime_type is None:
                mime_type = 'image/png'
            with open(norm_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            print(f"[embed_image] Successfully read and encoded image: {norm_path}")
            return f'data:{mime_type};base64,{img_data}'
        except Exception as e:
            print(f"[embed_image] Error embedding image {norm_path}: {str(e)}")
            return None

    def wrap_text(self, text, max_chars=40):
        if pd.isna(text):
            return []
        lines = str(text).split('\n')
        wrapped_lines = []
        for line in lines:
            if len(line.strip()) > 0:
                if len(line) > max_chars:
                    current_line = []
                    words = line.split()
                    for word in words:
                        if current_line and len(' '.join(current_line + [word])) > max_chars:
                            wrapped_lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            current_line.append(word)
                    if current_line:
                        wrapped_lines.append(' '.join(current_line))
                else:
                    wrapped_lines.append(line)
            else:
                wrapped_lines.append('')
        return wrapped_lines

    def add_reference_point(self, dwg):
        ref_size_px = 0.1 * self.px_per_mm
        x_pos = self.page_width_px - ref_size_px
        y_pos = self.page_height_px - ref_size_px
        dwg.add(dwg.rect(
            insert=(x_pos, y_pos),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))

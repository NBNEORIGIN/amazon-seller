import pandas as pd
import svgwrite
print('memorial_base.py loaded')
import os
from svgwrite import mm
import textwrap
import sys
from pathlib import Path
import base64
import mimetypes
from datetime import datetime

class MemorialBase:
    def __init__(self, graphics_path, output_dir):
        print('MemorialBase.__init__ called')
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
    def generate_warnings(row):
        import re, datetime
        warnings = []
        # Check for extra spaces before comma/period and missing spaces after
        for key in ['LINE_1', 'LINE_2', 'LINE_3']:
            value = row.get(key, "")
            if value:
                if re.search(r"\s+[,\.]", value):
                    warnings.append(f"Extra space before comma/period in {key}")
                if re.search(r"[a-zA-Z],[a-zA-Z]", value):
                    warnings.append(f"Missing space after comma in {key}")
                if "  " in value:
                    warnings.append(f"Double space in {key}")
                if re.search(r"\b(\w+) \1\b", value, re.IGNORECASE):
                    warnings.append(f"Repeated word in {key}")
                # Check for capitalization (optional, flag if not title case)
                if value and not value.istitle():
                    warnings.append(f"Not title case in {key}")
                # Check for future dates
                date_pattern = r'(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)'
                for match in re.findall(date_pattern, value):
                    try:
                        dt = datetime.datetime.strptime(match, "%d/%m/%Y")
                    except ValueError:
                        try:
                            dt = datetime.datetime.strptime(match, "%m/%d/%Y")
                        except ValueError:
                            continue
                    if dt.year > datetime.datetime.now().year:
                        warnings.append(f"Future year found in {key}: {match}")
        return "; ".join(warnings)


    def create_batch_csv(self, orders, batch_num, category):
        """Create CSV file for the batch with specified category prefix, matching regular_stakes.py logic and including all fields present in input orders."""
        filename = f"{category}_{self.date_str}_{batch_num:03d}.csv"
        filepath = os.path.join(self.OUTPUT_DIR, filename)

        # Find all unique keys across all orders (for max flexibility)
        all_keys = set()
        for order in orders:
            all_keys.update([k.upper() for k in order.keys()])

        # Define preferred/standard order of columns, matching regular_stakes.py
        svg_filename = f"{category}_{self.date_str}_{batch_num:03d}.svg"
        preferred_columns = [
            'SVG FILE', 'DESIGN FILE', 'ORDER-ID', 'ORDER-ITEM-ID', 'SKU', 'NUMBER-OF-ITEMS',
            'TYPE', 'COLOUR', 'GRAPHIC', 'LINE_1', 'LINE_2', 'LINE_3', 'THEME', 'WARNINGS'
        ]
        extra_columns = [col for col in all_keys if col not in preferred_columns]
        columns = preferred_columns + extra_columns

        data = []
        for order in orders:
            row = {}
            row['SVG FILE'] = svg_filename
            row['DESIGN FILE'] = f"{category}_{self.date_str}_{batch_num:03d}"
            for col in columns:
                if col in ['SVG FILE', 'DESIGN FILE']:
                    continue
                # Try both upper and lower case keys
                val = order.get(col, order.get(col.lower(), order.get(col.upper(), '')))
                row[col] = val
            # Add warnings using the static method
            row['WARNINGS'] = MemorialBase.generate_warnings(order)
            data.append(row)

        df = pd.DataFrame(data)
        # Ensure column order for output
        df = df[columns]
        df.to_csv(filepath, index=False, encoding="utf-8")

    def embed_image(self, image_path):
        try:
            mime_type = mimetypes.guess_type(image_path)[0]
            if mime_type is None:
                mime_type = 'image/png'
            with open(image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            return f'data:{mime_type};base64,{img_data}'
        except Exception as e:
            print(f"Error embedding image {image_path}: {str(e)}")
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
        y_pos = (self.page_height_mm - 0.011) * self.px_per_mm - ref_size_px
        dwg.add(dwg.rect(
            insert=(x_pos, y_pos),
            size=(ref_size_px, ref_size_px),
            fill='blue'
        ))

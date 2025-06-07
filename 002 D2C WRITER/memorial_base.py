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
import language_tool_python # Added import

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
    def generate_warnings(row, lang_tool=None): # Added lang_tool parameter
        import re, datetime
        warnings = []
        text_fields_to_check = ['LINE_1', 'LINE_2', 'LINE_3'] # Standardized keys

        # Existing regex checks
        for key in text_fields_to_check:
            value = str(row.get(key, "")).strip() # Ensure it's a string and stripped
            if value: # Only process if there's actual text
                if re.search(r"\s+[,\.]", value):
                    warnings.append(f"Punctuation: Extra space before comma/period in {key}")
                if re.search(r"[a-zA-Z],[a-zA-Z]", value) and not re.search(r"\b(?:Mrs|Mr|Ms)\.,[a-zA-Z]", value): # Avoid flagging "Mr.,Smith"
                    warnings.append(f"Punctuation: Missing space after comma in {key}")
                if "  " in value: # Double spaces
                    warnings.append(f"Spacing: Double space found in {key}")
                if re.search(r"\b(\w+) \1\b", value, re.IGNORECASE): # Repeated words
                    warnings.append(f"Grammar: Repeated word in {key}")

                # Check for capitalization (optional, flag if not title case for certain lines)
                # This is a simple check; LanguageTool might provide more nuanced feedback.
                # Only apply to LINE_1 and LINE_2 as LINE_3 can be more free-form.
                if key in ['LINE_1', 'LINE_2'] and not value.istitle() and not value.isupper() and not value.islower():
                    # Check if it's a date range or similar pattern that shouldn't be title case
                    if not re.match(r"^\d{1,2}\w{2} \w+ \d{4} ?-? ?\d{1,2}\w{2} \w+ \d{4}$", value): # e.g. 1st Jan 2020 - 2nd Feb 2021
                         # Also check for simple year ranges like "1940 - 2020"
                        if not re.match(r"^\d{4} ?-? ?\d{4}$", value):
                            warnings.append(f"Capitalization: Consider title case for {key}")

                # Check for future dates (more robustly)
                # Matches DD/MM/YYYY, DD-MM-YYYY, MM/DD/YYYY, MM-DD-YYYY, also with YY
                date_pattern_flexible = r'\b(\d{1,2}[-/]\d{1,2}[-/](\d{2}|\d{4}))\b'
                for date_match_str, _, year_str in re.findall(date_pattern_flexible, value):
                    try:
                        # Normalize separators for strptime
                        normalized_date_str = date_match_str.replace('-', '/')
                        # Attempt to parse common date formats
                        if len(year_str) == 2:
                            parsed_dt = datetime.datetime.strptime(normalized_date_str, "%d/%m/%y")
                            if parsed_dt.year > datetime.datetime.now().year + 50: # Heuristic for YY: if 2070+ assume 1970
                                parsed_dt = parsed_dt.replace(year=parsed_dt.year - 100)
                        else: # len(year_str) == 4
                            parsed_dt = datetime.datetime.strptime(normalized_date_str, "%d/%m/%Y")
                    except ValueError:
                        try: # Try MM/DD/YY(YY)
                            if len(year_str) == 2:
                                parsed_dt = datetime.datetime.strptime(normalized_date_str, "%m/%d/%y")
                                if parsed_dt.year > datetime.datetime.now().year + 50:
                                    parsed_dt = parsed_dt.replace(year=parsed_dt.year - 100)
                            else:
                                parsed_dt = datetime.datetime.strptime(normalized_date_str, "%m/%d/%Y")
                        except ValueError:
                            continue # Could not parse with common formats

                    if parsed_dt.year > datetime.datetime.now().year :
                        warnings.append(f"Date: Possible future year {parsed_dt.year} in {key}: '{date_match_str}'")

        # LanguageTool checks
        if lang_tool:
            for key in text_fields_to_check:
                value = str(row.get(key, "")).strip()
                if value: # Only check if there's text
                    try:
                        matches = lang_tool.check(value)
                        for match in matches:
                            # Avoid some less critical or potentially noisy rules if needed by checking match.ruleId
                            # Example: match.ruleId not in ['UPPERCASE_SENTENCE_START', 'SENTENCE_WHITESPACE']

                            # Extract the actual error snippet from the original text being checked ('value')
                            error_snippet = value[match.offset : match.offset + match.errorLength]

                            # Construct the new warning message string
                            suggestion_text = match.replacements[0] if match.replacements else ''
                            warning_msg = f"LT ({match.ruleId} | {match.category}): {match.message} Suggested: '{suggestion_text}'. Found: '[{error_snippet}]'"
                            warnings.append(warning_msg)
                    except Exception as e:
                        warnings.append(f"LT_ERROR: Could not process field {key} with LanguageTool: {e}")

        return "; ".join(warnings)

    # Corrected indentation for create_batch_csv, embed_image, wrap_text, add_reference_point
    # These methods should be at the same indentation level as __init__ and generate_warnings

    def create_batch_csv(self, orders, batch_num, category, lang_tool_instance_global=None): # Added lang_tool_instance_global
        """Create CSV file for the batch with specified category prefix, matching regular_stakes.py logic and including all fields present in input orders."""
        filename = f"{category}_{self.date_str}_{batch_num:03d}.csv"
        filepath = os.path.join(self.OUTPUT_DIR, filename)

        all_keys = set()
        for order in orders:
            all_keys.update([k.upper() for k in order.keys()])

        svg_filename = f"{category}_{self.date_str}_{batch_num:03d}.svg" # This is the SVG filename used for reference in CSV
        preferred_columns = [
            'SVG FILE', 'DESIGN FILE', 'ORDER-ID', 'ORDER-ITEM-ID', 'SKU', 'NUMBER-OF-ITEMS',
            'TYPE', 'COLOUR', 'GRAPHIC', 'LINE_1', 'LINE_2', 'LINE_3', 'THEME', 'WARNINGS'
        ]
        extra_columns = [col for col in all_keys if col not in preferred_columns]
        columns = preferred_columns + extra_columns

        data = []

        def process_order_warnings(order_data, lt_tool_to_use):
            # Helper function to avoid code duplication for warning generation
            row = {}
            row['SVG FILE'] = svg_filename
            row['DESIGN FILE'] = f"{category}_{self.date_str}_{batch_num:03d}"
            for col in columns:
                if col in ['SVG FILE', 'DESIGN FILE']:
                    continue
                val = order_data.get(col, order_data.get(col.lower(), order_data.get(col.upper(), '')))
                row[col] = val
            row['WARNINGS'] = MemorialBase.generate_warnings(order_data, lt_tool_to_use)
            return row

        if lang_tool_instance_global:
            # Use the provided global instance
            print(f"Using provided LanguageTool instance for batch {batch_num} of {category}.")
            for order in orders:
                data.append(process_order_warnings(order, lang_tool_instance_global))
        else:
            # Initialize LanguageTool locally for this batch
            try:
                with language_tool_python.LanguageTool('en-US') as local_lt_instance:
                    print(f"LanguageTool initialized locally for batch {batch_num} of {category}.")
                    for order in orders:
                        data.append(process_order_warnings(order, local_lt_instance))
            except Exception as e:
                print(f"WARNING: LanguageTool could not be initialized or used locally in MemorialBase.create_batch_csv for {category} batch {batch_num}: {e}. Grammar checks will be skipped for this batch.")
                for order in orders: # Fallback if local LT init fails
                    data.append(process_order_warnings(order, None))
            # If LT initialized but failed during processing of an order (less likely for LT init issues)
            # current 'data' list will have orders processed before failure (with LT warnings).
            # To process remaining orders in the 'orders' list without LT:
            # This requires knowing how many were successfully processed.
            # For simplicity, if LT fails, this batch might have mixed warning quality or just skip LT for all.
            # The current logic processes all orders with None if LT fails at init.
            # If it fails after some processing, those processed before failure are in `data`.
            # The loop for `orders` is inside the try block, so if `lang_tool_instance` fails, remaining orders are processed in except.
            # The code structure for fallback is okay for init failure.

        df = pd.DataFrame(data)
        if not df.empty: # Ensure columns are reordered only if DataFrame is not empty
            present_columns = [col for col in columns if col in df.columns] # Ensure we only try to access present columns
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

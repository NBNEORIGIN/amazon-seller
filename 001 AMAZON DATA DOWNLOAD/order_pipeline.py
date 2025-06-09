import os
import csv
import requests
import zipfile
import io
import xml.etree.ElementTree as ET
import tempfile
import pandas as pd
import re
import datetime
import shutil

# --- Robust XML parsing logic ---
def parse_xml_for_fields(xml_path):
    with open(xml_path, 'rb') as f:
        xml_bytes = f.read()
        xml_text = xml_bytes.decode('utf-8')
        tree = ET.ElementTree(ET.fromstring(xml_text))
    root = tree.getroot()
    graphic = ""
    line_1 = ""
    line_2 = ""
    line_3 = ""
    for area in root.findall(".//areas"):
        label = area.find("label")
        if label is not None and label.text == "Graphic":
            option_value = area.find("optionValue")
            if option_value is not None and option_value.text:
                graphic = option_value.text.strip()
                break
            display_value = area.find("displayValue")
            if display_value is not None and display_value.text:
                graphic = display_value.text.strip()
                break
    if not graphic:
        for elem in root.iter():
            if elem.tag == "label" and elem.text == "Graphic":
                parent = elem.getparent() if hasattr(elem, "getparent") else None
                if parent is not None:
                    for sibling in parent:
                        if sibling.tag == "displayValue" and sibling.text:
                            graphic = sibling.text.strip()
                            break
                        if sibling.tag == "optionValue" and sibling.text:
                            graphic = sibling.text.strip()
                            break
            if graphic:
                break
    for line_label, target in [("Line 1", "line_1"), ("Line 2", "line_2"), ("Line 3", "line_3")]:
        found = False
        for area in root.findall(".//areas"):
            label = area.find("label")
            if label is not None and label.text == line_label:
                text_elem = area.find("text")
                if text_elem is not None and text_elem.text:
                    if target == "line_1":
                        line_1 = text_elem.text.strip()
                    elif target == "line_2":
                        line_2 = text_elem.text.strip()
                    elif target == "line_3":
                        line_3 = text_elem.text.strip()
                    found = True
                    break
        if found:
            continue
        for elem in root.iter():
            if elem.tag == "label" and elem.text == line_label:
                parent = elem.getparent() if hasattr(elem, "getparent") else None
                value = None
                if parent is not None:
                    for sibling in parent:
                        if sibling.tag == "inputValue" and sibling.text:
                            value = sibling.text.strip()
                            break
                        if sibling.tag == "text" and sibling.text:
                            value = sibling.text.strip()
                            break
                if value:
                    if target == "line_1":
                        line_1 = value
                    elif target == "line_2":
                        line_2 = value
                    elif target == "line_3":
                        line_3 = value
                    break
    return graphic, line_1, line_2, line_3

def download_and_extract_zip(url, dest_folder):
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(dest_folder)
        return True
    except Exception as e:
        print(f"Failed to download or extract ZIP: {url} -> {e}")
        return False

def extract_zip_urls_and_meta_from_report(report_path):
    orders = []
    with open(report_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            zip_url = row.get('customized-url', '')
            if zip_url and zip_url.startswith('http'):
                orders.append({
                    "order-id": row.get("order-id", ""),
                    "order-item-id": row.get("order-item-id", ""),
                    "sku": row.get("sku", ""),
                    "number-of-items": row.get("number-of-items", ""),
                    "zip_url": zip_url
                })
    return orders

def load_skulist(skulist_file):
    skulookup = {}
    print(f"Attempting to load SKULIST from: {skulist_file}")
    if not skulist_file or not os.path.exists(skulist_file):
        raise FileNotFoundError(f'SKULIST.csv not found at: {skulist_file}')
    with open(skulist_file, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"SKULIST.csv loaded, {len(rows)} rows found.")
        for i, row in enumerate(rows[:3]):
            print(f"Row {i} (raw): {row}")
        # After normalization, print the first 3 normalized rows
        for i, row in enumerate(rows[:3]):
            normalized = {k.lower(): v.strip() for k, v in row.items()}
            print(f"Row {i} (normalized): keys={list(normalized.keys())}, decorationtype={normalized.get('decorationtype')}")
        # Dynamically detect the SKU column key
        if rows and rows[0]:
            sku_col = None
            for k in rows[0].keys():
                if k.strip().lower().replace('\ufeff', '') == 'sku':
                    sku_col = k
                    break
            if not sku_col:
                raise ValueError("Could not find SKU column in SKULIST.csv")
        else:
            raise ValueError("SKULIST.csv appears empty or malformed")
        for row in rows:
            sku = row.get(sku_col, '').strip().lower()
            if sku:
                # Normalize all keys to lower-case for robust access (including 'decorationtype')
                normalized = {k.lower(): v.strip() for k, v in row.items()}
                skulookup[sku] = normalized
    print(f'SKULIST lookup keys: {list(skulookup.keys())}')
    return skulookup

def generate_warnings(row):
    warnings = []
    for key in ['line_1', 'line_2', 'line_3']:
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
            if value and not value.istitle():
                warnings.append(f"Not title case in {key}")
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

def process_amazon_orders(report_paths, images_dir, output_dir, skulist_path=None, status_callback=None):
    # Force images_dir to canonical location
    # Dynamically resolve images_dir relative to the script's location for portability
    images_dir = 'images'
    print(f"[DEBUG] Resolved images_dir (relative): {os.path.abspath(images_dir)}")
    # --- WINDSURF PATCH: Clean images directory before extracting any new images (rollback: remove this block) ---
    if os.path.exists(images_dir):
        image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
        if image_files:
            print(f"[DEBUG] Deleting {len(image_files)} files from images directory...")
            for f in image_files:
                try:
                    os.remove(os.path.join(images_dir, f))
                except Exception as e:
                    print(f"[ERROR] Could not delete {f}: {e}")
    # --- END WINDSURF PATCH ---
    # Accepts a list of report files or a single file
    if isinstance(report_paths, str):
        report_paths = [report_paths]

    import csv
    import tempfile
    import shutil
    import pandas as pd

    # Load SKU list
    skulookup = load_skulist(skulist_path) if skulist_path else {}
    print(f'SKULIST lookup keys: {list(skulookup.keys())}')

    # Aggregate all orders from all reports
    all_orders = []
    for report_path in report_paths:
        orders = extract_zip_urls_and_meta_from_report(report_path)
        all_orders.extend(orders)
    temp_dir = tempfile.mkdtemp()
    downloads_dir = os.path.join(temp_dir, "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    output_rows = []
    os.makedirs(images_dir, exist_ok=True)
    for i, order in enumerate(all_orders):
        order_folder = os.path.join(downloads_dir, f"{order['order-id']}_{order['order-item-id']}")
        os.makedirs(order_folder, exist_ok=True)
        image_path = ""
        if download_and_extract_zip(order["zip_url"], order_folder):
            if status_callback:
                status_callback(f"Downloaded zip file {i+1} of {len(all_orders)}")
            else:
                print(f"Downloaded zip file {i+1} of {len(all_orders)}")
            xml_files = [f for f in os.listdir(order_folder) if f.endswith('.xml')]
            if xml_files:
                xml_path = os.path.join(order_folder, xml_files[0])
                graphic, line_1, line_2, line_3 = parse_xml_for_fields(xml_path)
            else:
                graphic = line_1 = line_2 = line_3 = ""
            jpg_files = [f for f in os.listdir(order_folder) if f.lower().endswith('.jpg')]
            if jpg_files:
                jpg_files_full = [os.path.join(order_folder, f) for f in jpg_files]
                largest_jpg = max(jpg_files_full, key=os.path.getsize)
                new_image_name = f"{order['order-item-id']}.jpg"
                dest_path = os.path.join(images_dir, new_image_name)
                print(f"[DEBUG] Preparing to copy image to: {dest_path}")
                try:
                    shutil.copy2(largest_jpg, dest_path)
                    print(f"[DEBUG] Successfully copied image to: {dest_path}")
                    image_path = os.path.join('images', new_image_name).replace('\\', '/')
                    print(f"[DEBUG] Final image_path for CSV: {image_path}")
                except Exception as copy_err:
                    print(f"[ERROR] Failed to copy image {largest_jpg} to {dest_path}: {copy_err}")
                    image_path = ""
            else:
                print(f"[WARNING] No .jpg file found for order {order['order-item-id']}")
                image_path = ""
        else:
            graphic = line_1 = line_2 = line_3 = ""
        original_sku = str(order["sku"]).strip()
        sku_key = original_sku.lower().strip()
        sku_info = skulookup.get(sku_key)
        if not sku_info:
            # Try lower-case, all spaces removed
            sku_key_nospace = sku_key.replace(' ', '')
            for k, v in skulookup.items():
                if sku_key_nospace == k.replace(' ', ''):
                    sku_info = v
                    break
        if not sku_info:
            # Try lower-case, dashes/underscores removed (spaces preserved)
            sku_key_nodash = sku_key.replace('-', '').replace('_', '')
            for k, v in skulookup.items():
                if sku_key_nodash == k.replace('-', '').replace('_', ''):
                    sku_info = v
                    break
        if not sku_info:
            sku_info = {}
            print(f"Unmapped SKU: {order['sku']}")
            missing_sku_warning = f"SKU '{order['sku']}' not found in SKULIST.csv. Please add it for future mapping."
        else:
            missing_sku_warning = ""
        print(f"Processing SKU {order['sku']}: sku_info={sku_info}")
        # Special case: if SKU is 'OD042030Silver', force graphic to 'OD042030Silver.png'
        graphic_value = (graphic + ".png") if graphic else ""
        if original_sku.strip().lower() == 'od042030silver':
            graphic_value = 'OD042030Silver.png'
        row = {
            "order-id": order["order-id"],
            "order-item-id": order["order-item-id"],
            "sku": order["sku"],
            "number-of-items": order["number-of-items"],
            "type": sku_info.get("type", ""),
            "colour": sku_info.get("colour", ""),
            "graphic": graphic_value,
            "line_1": line_1,
            "line_2": line_2,
            "line_3": line_3,
            "image_path": image_path,
            "theme": sku_info.get("theme", ""),
            "decorationtype": sku_info.get("decorationtype", sku_info.get("DecorationType", "")),
        }
        print(f"Order row decorationtype: {row['decorationtype']}")
        # Add missing SKU warning if applicable
        warning_text = generate_warnings(row)
        if missing_sku_warning:
            if warning_text:
                warning_text = missing_sku_warning + "; " + warning_text
            else:
                warning_text = missing_sku_warning
        # Retrieve processor_category from sku_info
        processor_category = sku_info.get('processorcategory', 'unclassified')
        if not processor_category: # Handles empty string as well
            processor_category = 'unclassified'
        row["processor_category"] = processor_category

        row["Warnings"] = warning_text
        print(f"[DEBUG] Writing row to CSV: {row}")
        output_rows.append(row)
    df_out = pd.DataFrame(output_rows)
    # --- WINDSURF PATCH: Set 'graphic' to 'Photo' for photo products (rollback: remove this block) ---
    if 'graphic' in df_out.columns and 'decorationtype' in df_out.columns:
        print('DEBUG BEFORE PATCH:')
        print(df_out[['graphic', 'decorationtype']].head(20))
        mask = df_out['decorationtype'].astype(str).str.strip().str.lower() == 'photo'
        print('DEBUG MASK SUM:', mask.sum())
        print('DEBUG ROWS TO PATCH:')
        print(df_out[mask][['graphic', 'decorationtype']])
        df_out.loc[mask, 'graphic'] = 'Photo'
        print('DEBUG AFTER PATCH:')
        print(df_out[mask][['graphic', 'decorationtype']])
    # --- END WINDSURF PATCH ---
    # Write CSV (comma-delimited)
    output_csv = os.path.join(output_dir, "output.csv")
    # Updated fieldnames to include processor_category
    fieldnames = [
        "order-id", "order-item-id", "sku", "number-of-items",
        "type", "colour", "graphic", "line_1", "line_2", "line_3",
        "image_path", "theme", "decorationtype", "processor_category", "Warnings"
    ]
    # Ensure processor_category column exists in df_out, if not, add it with default 'unclassified'
    if 'processor_category' not in df_out.columns:
        print(f"[WARNING] 'processor_category' column was not created during row processing. Adding it now with default 'unclassified'.")
        df_out['processor_category'] = 'unclassified'

    df_out.to_csv(output_csv, index=False, columns=fieldnames, encoding="utf-8-sig")
    # Write TXT (tab-delimited)
    output_txt = os.path.join(output_dir, "output.txt")
    df_out.to_csv(output_txt, index=False, columns=fieldnames, sep='\t', encoding="utf-8")
    # Print unmapped SKUs for debugging
    unmapped = [row['sku'] for row in output_rows if not row['type'] and not row['colour']]
    if unmapped:
        print(f"Unmapped SKUs: {unmapped}")

    # Group by processor_category and save categorized CSVs
    categorized_dfs = {}
    if 'processor_category' in df_out.columns:
        grouped = df_out.groupby('processor_category')
        for category_name, group_df in grouped:
            categorized_dfs[category_name] = group_df
            category_filename = os.path.join(output_dir, f"output_category_{str(category_name).replace(' ', '_').lower()}.csv")
            try:
                group_df.to_csv(category_filename, index=False, columns=fieldnames, encoding="utf-8-sig")
                print(f"Saved categorized CSV: {category_filename}")
            except Exception as e:
                print(f"[ERROR] Could not save categorized CSV {category_filename}: {e}")
    else:
        print("[WARNING] 'processor_category' column not found in DataFrame. All orders will be in 'unclassified' group.")
        categorized_dfs['unclassified'] = df_out.copy()
        # Attempt to save the unclassified group if the column was missing
        category_filename = os.path.join(output_dir, "output_category_unclassified.csv")
        try:
            df_out.to_csv(category_filename, index=False, columns=fieldnames, encoding="utf-8-sig")
            print(f"Saved unclassified orders (due to missing category column) to: {category_filename}")
        except Exception as e:
            print(f"[ERROR] Could not save unclassified CSV {category_filename}: {e}")

    return categorized_dfs

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
    import os
    skulookup = {}
    print(f"Attempting to load SKULIST from: {skulist_file}")
    if not skulist_file or not os.path.exists(skulist_file):
        raise FileNotFoundError(f'SKULIST.csv not found at: {skulist_file}')
    with open(skulist_file, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"SKULIST.csv loaded, {len(rows)} rows found.")
        for i, row in enumerate(rows[:3]):
            print(f"Row {i}: {row}")
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
                # Normalize all keys to lower-case for robust access
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

def process_amazon_orders(report_paths, images_dir, output_dir, skulist_path=None):
    # Accepts a list of report files or a single file
    if isinstance(report_paths, str):
        report_paths = [report_paths]

    import os
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
    for order in all_orders:
        order_folder = os.path.join(downloads_dir, f"{order['order-id']}_{order['order-item-id']}")
        os.makedirs(order_folder, exist_ok=True)
        image_path = ""
        if download_and_extract_zip(order["zip_url"], order_folder):
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
                try:
                    shutil.copy2(largest_jpg, dest_path)
                    image_path = dest_path
                except Exception as e:
                    print(f"Failed to copy image for order {order['order-item-id']}: {e}")
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
        row = {
            "order-id": order["order-id"],
            "order-item-id": order["order-item-id"],
            "sku": order["sku"],
            "number-of-items": order["number-of-items"],
            "type": sku_info.get("type", ""),
            "colour": sku_info.get("colour", ""),
            "graphic": (graphic + ".png") if graphic else "",
            "line_1": line_1,
            "line_2": line_2,
            "line_3": line_3,
            "image_path": image_path,
            "theme": sku_info.get("theme", ""),
        }
        # Add missing SKU warning if applicable
        warning_text = generate_warnings(row)
        if missing_sku_warning:
            if warning_text:
                warning_text = missing_sku_warning + "; " + warning_text
            else:
                warning_text = missing_sku_warning
        row["Warnings"] = warning_text
        output_rows.append(row)
    df_out = pd.DataFrame(output_rows)
    # Write CSV (comma-delimited)
    output_csv = os.path.join(output_dir, "output.csv")
    fieldnames = [
        "order-id", "order-item-id", "sku", "number-of-items",
        "type", "colour", "graphic", "line_1", "line_2", "line_3", "image_path", "theme", "Warnings"
    ]
    df_out.to_csv(output_csv, index=False, columns=fieldnames, encoding="utf-8-sig")
    # Write TXT (tab-delimited)
    output_txt = os.path.join(output_dir, "output.txt")
    df_out.to_csv(output_txt, index=False, columns=fieldnames, sep='\t', encoding="utf-8")
    # Print unmapped SKUs for debugging
    unmapped = [row['sku'] for row in output_rows if not row['type'] and not row['colour']]
    if unmapped:
        print(f"Unmapped SKUs: {unmapped}")
    return df_out

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

OUTPUT_DIR = r"G:\My Drive\003 APPS\002 AmazonSeller\001 AMAZON DATA DOWNLOAD"

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

    # Extract Graphic from either <optionValue> or <displayValue> with label "Graphic"
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
        # Try fallback: <label>Graphic</label> with <displayValue> or <optionValue> in parent
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

    # Extract Line 1, 2, 3 from <areas> or <label>Line N</label> with <text> or <inputValue>
    for line_label, target in [("Line 1", "line_1"), ("Line 2", "line_2"), ("Line 3", "line_3")]:
        found = False
        # Look in <areas>
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
        # Fallback: search for <label>Line N</label> with <inputValue> or <text> in parent
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
        print(f"Failed to download or extract {url}: {e}")
        return False

def extract_zip_urls_and_meta_from_report(report_path):
    """Parse the TSV/text order report and extract all ZIP URLs and required metadata."""
    orders = []
    with open(report_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            url = row.get("customized-url")
            if url and url.startswith("http"):
                qty = row.get("quantity-purchased", "1")
                orders.append({
                    "order-id": row.get("order-id", ""),
                    "order-item-id": row.get("order-item-id", ""),
                    "sku": row.get("sku", ""),
                    # Set number-of-items to the per-row quantity-purchased
                    "number-of-items": qty,
                    "quantity-purchased": qty,
                    "zip_url": url
                })
    return orders

def load_skulist(skulist_file):
    """Load SKULIST.csv into a dictionary keyed by SKU."""
    df = pd.read_csv(skulist_file)
    lookup = {}
    for _, row in df.iterrows():
        sku = str(row["SKU"]).strip()
        lookup[sku] = {
            "Type": str(row.get("TYPE", "")).strip(),
            "Colour": str(row.get("COLOUR", "")).strip(),
            "Theme": str(row.get("Theme", "")).strip() if "Theme" in row else ""
        }
    return lookup

def generate_warnings(row):
    warnings = []
    # Check for extra spaces before comma/period and missing spaces after
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

def main():
    # Find all order report files (18 digit numbers, .txt extension)
    report_files = [
        os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR)
        if re.fullmatch(r"\d{18}\.txt", f)
    ]
    if not report_files:
        print("No order report files found in the folder.")
        return
    # Find SKULIST.csv
    skulist_path = os.path.join(OUTPUT_DIR, "SKULIST.csv")
    if not os.path.exists(skulist_path):
        print("SKULIST.csv not found in the folder.")
        return
    skulookup = load_skulist(skulist_path)
    all_orders = []
    for report in report_files:
        orders = extract_zip_urls_and_meta_from_report(report)
        all_orders.extend(orders)
    print(f"Found {len(all_orders)} orders with ZIP URLs in the reports.")
    temp_dir = tempfile.mkdtemp()
    downloads_dir = os.path.join(temp_dir, "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    output_rows = []
    images_dir = r"G:\My Drive\003 APPS\002 AmazonSeller\004 IMAGES"
    os.makedirs(images_dir, exist_ok=True)
    for order in all_orders:
        order_folder = os.path.join(downloads_dir, f"{order['order-id']}_{order['order-item-id']}")
        os.makedirs(order_folder, exist_ok=True)
        image_path = ""
        if download_and_extract_zip(order["zip_url"], order_folder):
            # Find the first XML in the extracted folder
            xml_files = [f for f in os.listdir(order_folder) if f.endswith('.xml')]
            if xml_files:
                xml_path = os.path.join(order_folder, xml_files[0])
                graphic, line_1, line_2, line_3 = parse_xml_for_fields(xml_path)
            else:
                graphic = line_1 = line_2 = line_3 = ""
            # Find jpg images
            jpg_files = [f for f in os.listdir(order_folder) if f.lower().endswith('.jpg')]
            if jpg_files:
                # Pick the largest file
                jpg_files_full = [os.path.join(order_folder, f) for f in jpg_files]
                largest_jpg = max(jpg_files_full, key=os.path.getsize)
                # Rename and copy to images_dir
                new_image_name = f"{order['order-item-id']}.jpg"
                dest_path = os.path.join(images_dir, new_image_name)
                try:
                    import shutil
                    shutil.copy2(largest_jpg, dest_path)
                    image_path = dest_path
                except Exception as e:
                    print(f"Failed to copy image for order {order['order-item-id']}: {e}")
        else:
            graphic = line_1 = line_2 = line_3 = ""
        sku_info = skulookup.get(order["sku"].strip(), {})
        row = {
            "order-id": order["order-id"],
            "order-item-id": order["order-item-id"],
            "sku": order["sku"],
            "number-of-items": order["number-of-items"],
            "type": sku_info.get("Type", ""),
            "colour": sku_info.get("Colour", ""),
            "graphic": (graphic + ".png") if graphic else "",
            "line_1": line_1,
            "line_2": line_2,
            "line_3": line_3,
            "image_path": image_path
        }
        row["Warnings"] = generate_warnings(row)
        output_rows.append(row)
    output_csv = os.path.join(OUTPUT_DIR, "output.csv")
    output_txt = os.path.join(OUTPUT_DIR, "output.txt")
    fieldnames = [
        "order-id", "order-item-id", "sku", "number-of-items",
        "type", "colour", "graphic", "line_1", "line_2", "line_3", "image_path", "Theme", "Warnings"
    ]
    # Write CSV (comma-delimited)
    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            if "Theme" not in row:
                row["Theme"] = ""
            if "Warnings" not in row:
                row["Warnings"] = ""
            writer.writerow(row)
    # Write TXT (tab-delimited)
    with open(output_txt, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for row in output_rows:
            if "Theme" not in row:
                row["Theme"] = ""
            if "Warnings" not in row:
                row["Warnings"] = ""
            writer.writerow(row)
    print(f"Processing complete! Output written to {output_csv} and {output_txt}")

if __name__ == "__main__":
    main()

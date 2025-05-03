import os
import csv
import requests
import zipfile
import io
import xml.etree.ElementTree as ET
import shutil
import tempfile
import re
from datetime import datetime

def clean_text(text):
    if not text:
        return text
    text = re.sub(r'\s+([,.])', r'\1', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def check_advanced_errors(texts):
    warnings = []
    current_year = datetime.now().year
    required_fields = ['Line 1', 'Line 2', 'Line 3']
    for field in required_fields:
        if field not in texts or not texts[field] or texts[field].strip() == "":
            warnings.append(f"Missing {field}")
    for key, val in texts.items():
        if not val:
            continue
        matches = re.findall(r'\b(20\d{2})\b', val)
        for year in matches:
            if int(year) > current_year:
                warnings.append(f"Future year in {key}: {year}")
    for key, val in texts.items():
        if val:
            if re.search(r'(.)\1{4,}', val):
                warnings.append(f"Suspicious repeated characters in {key}")
            if len(val) > 100:
                warnings.append(f"Unusually long text in {key}")
            if re.search(r'<[^>]+>', val):
                warnings.append(f"HTML/XML tags found in {key}")
    return "; ".join(warnings) if warnings else ""

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

def parse_xml_for_fields(xml_path, dest_folder, order_item_id):
    with open(xml_path, 'rb') as f:
        xml_bytes = f.read()
        xml_text = xml_bytes.decode('utf-8')
        tree = ET.ElementTree(ET.fromstring(xml_text))
    root = tree.getroot()
    texts = {}
    label_mapping = {
        'Introduction': 'Line 1',
        'Line 1': 'Line 1',
        'Text Line 1': 'Line 1',
        'First Line': 'Line 1',
        'Name': 'Line 2',
        'Line 2': 'Line 2',
        'Text Line 2': 'Line 2',
        'Second Line': 'Line 2',
        'Dates': 'Line 3',
        'Date': 'Line 3',
        'Line 3': 'Line 3',
        'Line3': 'Line 3',
        'Text Line 3': 'Line 3',
        'Third Line': 'Line 3'
    }
    for area in root.findall('.//areas'):
        label = area.findtext('label')
        text_value = area.findtext('text')
        if label and text_value:
            standard_label = label_mapping.get(label, label)
            texts[standard_label] = text_value
    if not texts:
        for child in root.findall('.//children/children/children/children'):
            label = child.findtext('label')
            input_value = child.findtext('inputValue')
            if label and input_value:
                standard_label = label_mapping.get(label, label)
                texts[standard_label] = input_value
    graphic = ""
    photo_path = ""
    for area in root.findall('.//areas'):
        graphic_val = area.findtext('graphic')
        if graphic_val:
            graphic = graphic_val
    for area in root.findall('.//areas'):
        photo_val = area.findtext('photo')
        if photo_val:
            orig_path = os.path.join(dest_folder, photo_val)
            if os.path.exists(orig_path):
                order_folder = os.path.dirname(dest_folder)
                photos_dir = os.path.join(order_folder, 'photos')
                os.makedirs(photos_dir, exist_ok=True)
                new_name = f"{order_item_id}.jpg"
                new_path = os.path.join(photos_dir, new_name)
                shutil.copy2(orig_path, new_path)
                photo_path = os.path.join('photos', new_name)
    return texts, graphic, photo_path

def parse_xml_in_folder(folder, order_item_id):
    for file in os.listdir(folder):
        if file.endswith('.xml'):
            return parse_xml_for_fields(os.path.join(folder, file), folder, order_item_id)
    return {}, '', ''

def get_batch_sort_key(order, skulookup):
    t = (order['TYPE'] or '').strip().lower()
    c = (order['COLOUR'] or '').strip().lower()
    g = (skulookup.get(order['sku'], {}).get('Graphic') or '').strip().lower()
    is_photo = 'photo' in g
    is_graphic = 'graphic' in g
    if t == 'regular stk' and c in ['copper', 'gold', 'silver'] and is_graphic:
        return (1, ['copper', 'gold', 'silver'].index(c), 0)
    if t == 'regular stk' and c == 'black' and is_graphic:
        return (2, 0, 0)
    if t == 'regular stk' and c in ['copper', 'gold', 'silver'] and is_photo:
        return (3, ['copper', 'gold', 'silver'].index(c), 1)
    if t == 'regular stk' and c == 'black' and is_photo:
        return (4, 0, 1)
    if t == 'large stk' and c in ['copper', 'gold', 'silver'] and is_graphic:
        return (5, ['copper', 'gold', 'silver'].index(c), 0)
    if t == 'large stk' and c == 'black' and is_graphic:
        return (6, 0, 0)
    if t == 'large stk' and c == 'black' and is_photo:
        return (7, 0, 1)
    if t == 'small stk':
        return (8, 0, 0)
    return (99, 0, 0)

def get_orders(base_dir=None):
    """Returns a list of order dicts. base_dir defaults to current script dir."""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Find SKULIST.csv
    skulist_path = os.path.join(base_dir, "SKULIST.csv")
    if not os.path.isfile(skulist_path):
        raise FileNotFoundError("SKULIST.csv not found in the directory.")

    # Find all 18-digit .txt files
    txt_files = [f for f in os.listdir(base_dir) if f.endswith('.txt') and len(os.path.splitext(f)[0]) == 18 and os.path.splitext(f)[0].isdigit()]
    txt_files = [os.path.join(base_dir, f) for f in txt_files]
    if not txt_files:
        raise FileNotFoundError("No 18-digit .txt files found in the directory.")

    # Read SKULIST.csv
    skulookup = {}
    with open(skulist_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row.get('SKU', '').strip()
            skulookup[sku] = {
                'COLOUR': row.get('COLOUR', '').strip(),
                'TYPE': row.get('TYPE', '').strip(),
                'Graphic': row.get('Graphic', '').strip(),
                'Theme': row.get('Theme', '').strip()
            }

    temp_dir = tempfile.mkdtemp()
    downloads_dir = os.path.join(temp_dir, "downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    all_orders = []
    for txt_file in txt_files:
        with open(txt_file, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
            if not rows or len(rows) < 2:
                continue
            for row in rows[1:]:
                if len(row) < 35:
                    continue
                order_id = row[0]
                order_item_id = row[1]
                sku = row[11]
                quantity = int(row[14]) if row[14].isdigit() else 1
                url = row[34]  # <-- AI column, zero-based index 34
                if not url:
                    continue
                folder_name = f"{order_id}_{order_item_id}"
                dest_folder = os.path.join(downloads_dir, folder_name)
                os.makedirs(dest_folder, exist_ok=True)
                if download_and_extract_zip(url, dest_folder):
                    texts, graphic, photo_path = parse_xml_in_folder(dest_folder, order_item_id)
                    texts_clean = {k: clean_text(v) for k, v in texts.items()}
                    warning_flag = check_advanced_errors(texts_clean)
                    sku_info = skulookup.get(sku, {'COLOUR': '', 'TYPE': '', 'Graphic': '', 'Theme': ''})
                    for i in range(quantity):
                        copy_order_item_id = f"{order_item_id}_copy_{i+1}" if i > 0 else order_item_id
                        order_data = {
                            'order-item-id': copy_order_item_id,
                            'order-id': order_id,
                            'COLOUR': sku_info['COLOUR'],
                            'graphic': graphic,
                            'line_1': texts_clean.get('Line 1', ''),
                            'line_2': texts_clean.get('Line 2', ''),
                            'line_3': texts_clean.get('Line 3', ''),
                            'TYPE': sku_info['TYPE'],
                            'sku': sku,
                            'Theme': sku_info['Theme'],
                            'photo_path': photo_path,
                            'warning_flag': warning_flag
                        }
                        all_orders.append(order_data)

    # Sort orders by batching logic
    all_orders.sort(key=lambda order: get_batch_sort_key(order, skulookup))
    return all_orders

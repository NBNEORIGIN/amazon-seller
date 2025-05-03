import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip  # pip install pyperclip
import csv
import subprocess
from pathlib import Path

OUTPUT_CSV_PATH = str(Path(__file__).parent / "001 AMAZON DATA DOWNLOAD" / "output.csv")
OUTPUT_TXT_PATH = str(Path(__file__).parent / "001 AMAZON DATA DOWNLOAD" / "output.txt")

def expand_txt_to_csv(txt_path, csv_path):
    import pandas as pd
    df = pd.read_csv(txt_path, sep='\t', dtype=str, encoding='utf-8')
    # Fill NaN with empty string
    df = df.fillna("")
    # Expand rows by number-of-items (default 1)
    def get_qty(row):
        try:
            qty = int(row.get('number-of-items', 1))
            return max(qty, 1)
        except Exception:
            return 1
    df_expanded = df.loc[df.index.repeat(df.apply(get_qty, axis=1))].reset_index(drop=True)
    # Set number-of-items to 1 for all rows (since each is now a single memorial)
    if 'number-of-items' in df_expanded.columns:
        df_expanded['number-of-items'] = 1
    df_expanded.to_csv(csv_path, index=False, encoding='utf-8')


def load_orders_and_columns(csv_path):
    try:
        with open(csv_path, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            orders = list(reader)
            columns = reader.fieldnames if reader.fieldnames else []
        return orders, columns
    except Exception:
        return [], []

def copy_to_clipboard(data, columns):
    lines = ["\t".join(columns)]
    for row in data:
        lines.append("\t".join(str(row.get(col, "")) for col in columns))
    pyperclip.copy("\n".join(lines))

def show_orders_gui():
    root = tk.Tk()
    root.title("Amazon Orders QA Table")

    # Try to get columns from CSV, else use default columns including Theme
    _, columns = load_orders_and_columns(OUTPUT_CSV_PATH)
    if not columns:
        columns = ["order-id", "order-item-id", "sku", "number-of-items", "type", "colour", "graphic", "line_1", "line_2", "line_3", "image_path", "Theme"]

    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.W, width=120)
    tree.pack(fill=tk.BOTH, expand=True)

    orders = []

    def refresh_table():
        nonlocal orders
        orders, new_columns = load_orders_and_columns(OUTPUT_CSV_PATH)
        tree.delete(*tree.get_children())
        if new_columns:
            tree["columns"] = new_columns
            for col in new_columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W, width=120)
        for row in orders:
            values = [row.get(col, "") for col in tree["columns"]]
            tree.insert('', tk.END, values=values)

    def copy_all():
        copy_to_clipboard(orders, tree["columns"])
        messagebox.showinfo("Copied", "Orders copied to clipboard for Google Sheets!")

    def run_order_processing():
        script_path = str(Path(__file__).parent / "001 AMAZON DATA DOWNLOAD" / "app.py")
        subprocess.run([sys.executable, script_path])
        refresh_table()
        messagebox.showinfo("Order Processing", "Order processing complete and table reloaded.")

    def generate_regular_stakes_svgs():
        try:
            svg_output = str(Path(__file__).parent / "SVG_OUTPUT")
            graphics_path = "G:/My Drive/001 NBNE/001 M/M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM/001 Design/002 MUTOH/002 AUTODESIGN"
            images_path = "G:/My Drive/003 APPS/002 AmazonSeller/004 IMAGES"
            # Step 1: Expand TXT to CSV with one memorial per row
            expand_txt_to_csv(OUTPUT_TXT_PATH, OUTPUT_CSV_PATH)
            # Step 2: Generate SVGs from output.csv
            script_path_regular = str(Path(__file__).parent / "002 D2C WRITER" / "regular_stakes.py")
            subprocess.run([sys.executable, script_path_regular, svg_output, graphics_path])
            script_path_bw = str(Path(__file__).parent / "002 D2C WRITER" / "bw_stakes.py")
            subprocess.run([sys.executable, script_path_bw, svg_output, graphics_path])
            script_path_photo = str(Path(__file__).parent / "002 D2C WRITER" / "photo_stakes.py")
            subprocess.run([sys.executable, script_path_photo, svg_output, graphics_path, images_path])
            messagebox.showinfo("SVGs", f"Regular Stake, B&W, and Photo Stake SVGs generated in {svg_output}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate SVGs: {e}")

    btn_frame = tk.Frame(root)
    btn_frame.pack(fill=tk.X, pady=5)
    tk.Button(btn_frame, text="Order Processing", command=run_order_processing).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Load Orders", command=refresh_table).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Copy All to Clipboard", command=copy_all).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Create SVGs", command=generate_regular_stakes_svgs).pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    show_orders_gui()
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

def prompt_file_path(prompt, default_ext=None):
    path = input(f"{prompt}: ").strip('"')
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        exit(1)
    if default_ext and not path.lower().endswith(default_ext):
        print(f"Warning: file does not end with {default_ext}, attempting to load anyway.")
    return path

def parse_month_year(date_str):
    # Handles ISO or other formats, returns 'Jan-24' style
    try:
        dt = pd.to_datetime(date_str)
        return dt.strftime('%b-%y')
    except Exception:
        return None

def main():
    print("Amazon Sales Heatmap Generator\n---")
    sales_path = prompt_file_path("Enter path to Amazon sales file (tab-delimited .txt)", default_ext='.txt')
    sku_map_path = prompt_file_path("Enter path to SKU mapping file (ASSEMBLY.csv)", default_ext='.csv')
    out_csv_path = input("Enter desired output CSV path (e.g., output_heatmap.csv): ").strip('"')

    # Load sales data
    sales_df = pd.read_csv(sales_path, sep='\t', dtype=str)
    # Clean: Only keep shipped items, drop cancelled, etc.
    sales_df = sales_df[sales_df['order-status'].str.lower() == 'shipped']
    sales_df['quantity'] = pd.to_numeric(sales_df['quantity'], errors='coerce').fillna(0).astype(int)
    sales_df['purchase-month'] = sales_df['purchase-date'].apply(parse_month_year)
    # Drop rows with missing SKU or month
    sales_df = sales_df.dropna(subset=['sku', 'purchase-month'])

    # Aggregate sales by SKU and month
    agg_sales = sales_df.groupby(['sku', 'purchase-month'])['quantity'].sum().reset_index()

    # Load SKU mapping
    sku_map = pd.read_csv(sku_map_path, dtype=str)
    sku_map = sku_map.rename(columns=lambda x: x.strip())
    # Use only relevant columns
    sku_map = sku_map[['CHILD SKU','MASTER SKU','DESCRIPTION']].drop_duplicates()
    
    # Merge sales with mapping
    merged = pd.merge(agg_sales, sku_map, left_on='sku', right_on='CHILD SKU', how='left')
    merged['MASTER SKU'] = merged['MASTER SKU'].fillna(merged['sku'])
    merged['DESCRIPTION'] = merged['DESCRIPTION'].fillna('')

    # Pivot to heatmap format
    pivot = merged.pivot_table(index=['sku','MASTER SKU','DESCRIPTION'],
                              columns='purchase-month', values='quantity', fill_value=0, aggfunc='sum')
    pivot = pivot.reset_index()

    # Add stats columns (trimmed mean, 3 month mean, SD)
    month_cols = [col for col in pivot.columns if '-' in col]
    pivot['TRIMMED MEAN'] = pivot[month_cols].apply(lambda x: x.sort_values()[1:-1].mean() if len(x.dropna()) > 2 else x.mean(), axis=1)
    pivot['3 Month MEAN'] = pivot[month_cols].apply(lambda x: x.sort_values(ascending=False)[:3].mean() if len(x.dropna()) >= 3 else x.mean(), axis=1)
    pivot['SD'] = pivot[month_cols].std(axis=1)

    # Reorder columns to match example
    out_cols = ['sku','MASTER SKU','DESCRIPTION'] + month_cols + ['TRIMMED MEAN','3 Month MEAN','SD']
    out_df = pivot[out_cols]
    out_df.to_csv(out_csv_path, index=False)
    print(f"\nHeatmap CSV saved to: {out_csv_path}")

    # Optionally generate heatmap image
    gen_img = input("Generate heatmap image? (y/n): ").strip().lower()
    if gen_img == 'y':
        # For visualization, use only numeric data
        plt.figure(figsize=(len(month_cols)*0.7+3, max(6, len(out_df)*0.25)))
        sns.heatmap(out_df[month_cols], cmap='YlOrRd', annot=False, cbar=True)
        plt.title('Sales Heatmap by Month')
        plt.xlabel('Month')
        plt.ylabel('SKU Row')
        img_path = os.path.splitext(out_csv_path)[0] + '_heatmap.png'
        plt.savefig(img_path, bbox_inches='tight')
        print(f"Heatmap image saved to: {img_path}")

if __name__ == '__main__':
    main()

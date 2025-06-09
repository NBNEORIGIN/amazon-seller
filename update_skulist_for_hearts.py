import pandas as pd
import os

def update_processor_category_for_hearts():
    csv_path = 'assets/SKULIST.csv'

    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        return

    original_columns = df.columns.tolist()

    # Normalize column names for processing, keeping track of original names for lookup
    df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]

    # Find the original casing for 'ProcessorCategory' or use a default
    # This assumes 'processorcategory' is the normalized version.
    processor_category_col_original_casing = 'ProcessorCategory' # Default
    normalized_to_original_map = {col.lower().strip().replace(' ', '_'): orig_col for orig_col, col in zip(original_columns, df.columns)}

    # Attempt to find the original 'ProcessorCategory' column name more robustly
    # We need the key that *became* 'processorcategory' after normalization
    found_original_proc_cat_col = False
    for original_col_name in original_columns:
        if original_col_name.lower().strip().replace(' ', '_') == 'processorcategory':
            processor_category_col_original_casing = original_col_name
            found_original_proc_cat_col = True
            break

    if not found_original_proc_cat_col:
        # If 'ProcessorCategory' (or any variant) wasn't in the original CSV,
        # this script assumes it should add it.
        # However, the problem states it should exist from previous steps.
        # If it *must* exist, this could be an error. For now, let's use the default.
        print(f"Warning: Original 'ProcessorCategory' column not explicitly found. Using default '{processor_category_col_original_casing}'.")
        # If the normalized 'processorcategory' isn't in df.columns, it means it was never there.
        if 'processorcategory' not in df.columns:
            print(f"Error: Column 'processorcategory' (normalized) not found in DataFrame. Cannot update.")
            # Restore original column names before exiting if there was an issue.
            df.columns = original_columns
            return


    updated_rows_count = 0

    # Define target values for heart stakes
    target_type = 'heart stake'
    target_colours = ['copper', 'gold', 'silver', 'marble', 'stone']
    target_decoration_type = 'graphic'
    new_processor_category = "heart_stakes_graphic_coloured"

    for index, row in df.iterrows():
        # Ensure all key columns exist before trying to access them
        row_type = str(row.get('type', '')).lower().strip()
        row_colour = str(row.get('colour', '')).lower().strip()
        row_decoration_type = str(row.get('decorationtype', '')).lower().strip() # Corrected key

        type_check = (row_type == target_type)
        colour_check = (row_colour in target_colours)
        decoration_type_check = (row_decoration_type == target_decoration_type)

        if type_check and colour_check and decoration_type_check:
            # Update using the normalized column name 'processorcategory'
            df.loc[index, 'processorcategory'] = new_processor_category
            updated_rows_count += 1

    print(f"Number of rows updated to '{new_processor_category}': {updated_rows_count}")

    # Restore original column names before saving
    # Create a mapping from current (normalized) to original
    current_to_original_map = {norm_col: orig_col for norm_col, orig_col in zip(df.columns, original_columns)}
    df.rename(columns=current_to_original_map, inplace=True)

    # Ensure the final DataFrame uses the original column order
    # If new columns were added (like ProcessorCategory for the first time, though not expected here),
    # they might not be in original_columns.
    # For this task, we assume ProcessorCategory exists.
    final_ordered_columns = [col for col in original_columns if col in df.columns]
    # Add any new columns that weren't in original_columns (e.g. if ProcessorCategory was newly created)
    for col in df.columns:
        if col not in final_ordered_columns:
            final_ordered_columns.append(col)
    df = df[final_ordered_columns]


    try:
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"Successfully updated {csv_path}")
    except Exception as e:
        print(f"Error writing updated {csv_path}: {e}")

if __name__ == '__main__':
    update_processor_category_for_hearts()

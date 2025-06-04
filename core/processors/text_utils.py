"""
Text Utilities for Stake Processors
-----------------------------------
Shared text wrapping and grammar/typo checking functions.
"""
import textwrap
import re
from datetime import datetime
import pandas as pd
import os # Added os import

def split_line_to_fit(line, max_chars):
    """Split a single line into lines that fit max_chars."""
    return textwrap.wrap(line, width=max_chars)

def check_grammar_and_typos(line):
    """Perform grammar and typo checks on a single text line."""
    # a. Spaces before commas or periods
    if line and re.search(r"\s+[,\.]", line):
        print(f"Warning: Extra space before comma/period: '{line}'")
    # b. Future death dates (try to find DD/MM/YYYY or MM/DD/YYYY)
    date_pattern = r'(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)'
    if line:
        for match in re.findall(date_pattern, line):
            try:
                dt = datetime.strptime(match, "%d/%m/%Y")
            except ValueError:
                try:
                    dt = datetime.strptime(match, "%m/%d/%Y")
                except ValueError:
                    continue
            if dt.year > datetime.now().year:
                print(f"Warning: Future year found: '{match}' in '{line}'")
    # c. Capitalization of names (for potential name lines)
    if line and len(line.split()) <= 6 and not line.istitle(): # Simple check, might need refinement
        # Check if the line is fully uppercase, if so, it might be intentional
        if not line.isupper():
            print(f"Warning: Name not title case: '{line}'")
    return line # Return the line, though original didn't modify it

def split_line_to_fit_multiline(text_content, max_chars_per_line, max_lines):
    """
    Splits text content into multiple lines, each fitting max_chars_per_line,
    and limits the total number of lines.
    """
    if not text_content:
        return []

    # First, split by existing newlines, then wrap each of those.
    initial_lines = str(text_content).split('\n')
    processed_lines = []
    for l in initial_lines:
        if l.strip(): # Only process non-empty lines
            wrapped_sublines = textwrap.wrap(l, width=max_chars_per_line, break_long_words=True, replace_whitespace=False)
            processed_lines.extend(wrapped_sublines)
        elif processed_lines: # Preserve empty lines if they are not leading/trailing overall
             processed_lines.append("") # Add it as an empty line if it's intentional (not just spaces)

    # Trim to max_lines
    final_lines = processed_lines[:max_lines]

    # Ensure no leading/trailing empty strings if the result is just one line of empty string
    if len(final_lines) == 1 and not final_lines[0].strip():
        return []

    return final_lines

def create_batch_csv(orders_list_of_dicts, batch_num, category, output_dir, date_str=None):
    """
    Creates a CSV file for a batch of processed orders.

    Args:
        orders_list_of_dicts (list): A list of dictionaries, where each dict represents an order.
        batch_num (int): The batch number.
        category (str): The processor category (e.g., "REGULAR_STAKES").
        output_dir (str): The directory to save the CSV file.
        date_str (str, optional): Date string for the filename. Defaults to current date YYYYMMDD.
    """
    if not orders_list_of_dicts:
        print(f"No orders in batch {batch_num} for category {category} to create CSV.")
        return

    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")

    # Convert list of dicts to DataFrame
    df_batch = pd.DataFrame(orders_list_of_dicts)

    # Define a common set of columns to ensure consistency.
    # These should match the main columns used across different order types.
    common_columns = [
        'order-id', 'order-item-id', 'purchase-date', 'payments-date',
        'buyer-email', 'buyer-name', 'buyer-phone-number',
        'recipient-name', 'recipient-email', 'recipient-phone-number',
        'ship-address-1', 'ship-address-2', 'ship-city', 'ship-state',
        'ship-postal-code', 'ship-country', 'ship-phone-number',
        'product-name', 'sku', 'quantity-purchased', 'currency',
        'item-price', 'item-tax', 'shipping-price', 'shipping-tax',
        'gift-wrap-price', 'gift-wrap-tax', 'ship-service-level',
        'sales-channel',
        # Customization fields often start with 'customization-info;'
        # It might be better to handle them dynamically or ensure they are flattened
        # For now, let's list common flattened custom fields if known
        'line_1', 'line_2', 'line_3', 'graphic', 'image_path', 'photo_path',
        'type', 'colour', 'decorationtype', 'theme', 'number-of-items', 'Warnings'
    ]

    # Ensure all common_columns are present, adding them with NaN if missing
    # Append any other columns that were in the original DataFrame
    existing_common_cols = [col for col in common_columns if col in df_batch.columns]
    other_cols = [col for col in df_batch.columns if col not in common_columns]
    final_ordered_columns = existing_common_cols + other_cols

    df_batch = df_batch.reindex(columns=final_ordered_columns)

    csv_filename = f"{category}_{date_str}_batch_{batch_num:03d}.csv"
    csv_filepath = os.path.join(output_dir, csv_filename)

    try:
        os.makedirs(output_dir, exist_ok=True)
        df_batch.to_csv(csv_filepath, index=False, encoding='utf-8-sig')
        print(f"Successfully generated CSV: {csv_filepath}")
    except Exception as e:
        print(f"Error generating CSV {csv_filepath}: {e}")

# Example of a more advanced check_grammar_and_typos if needed later:
# def check_grammar_and_typos_v2(text, context=None):
#     # Placeholder for more advanced checks, potentially using a library
#     # For example, language_tool_python
#     # import language_tool_python
#     # tool = language_tool_python.LanguageTool('en-US')
#     # matches = tool.check(text)
#     # for match in matches:
#     #     print(f"Potential issue: {match.message} in '{text}' (Rule: {match.ruleId})")
#     # return tool.correct(text) # Or return messages/corrected text
#     return text

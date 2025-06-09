import pandas as pd

def determine_processor_category(row):
    # Normalize inputs
    type_norm = str(row.get('TYPE_norm', '')).lower().strip()
    colour_norm = str(row.get('COLOUR_norm', '')).lower().strip()
    decoration_type_norm = str(row.get('DecorationType_norm', '')).lower().strip()

    # Handle missing or empty DecorationType early for categories that require it
    if not decoration_type_norm and (type_norm not in ['large metal', 'medium metal', 'small metal']):
        # If decoration type is missing and it's not a metal product that could be raw
        pass # allow it to be classified by other rules if possible, or fall to unclassified

    # Category 1: regular_stakes_graphic_coloured
    if type_norm in ['regular stake', 'regular plaque'] and \
       colour_norm in ['copper', 'gold', 'silver', 'stone', 'marble'] and \
       decoration_type_norm == 'graphic':
        return 'regular_stakes_graphic_coloured'

    # Category 2: regular_stakes_graphic_bw
    if type_norm == 'regular stake' and \
       colour_norm in ['black', 'slate'] and \
       decoration_type_norm == 'graphic':
        return 'regular_stakes_graphic_bw'

    # Category 3: regular_stakes_photo_coloured
    if type_norm in ['regular stake', 'regular plaque'] and \
       colour_norm in ['copper', 'gold', 'silver', 'stone', 'marble'] and \
       decoration_type_norm == 'photo':
        return 'regular_stakes_photo_coloured'

    # Category 4: regular_stakes_photo_bw
    if type_norm == 'regular stake' and \
       colour_norm in ['black', 'slate'] and \
       decoration_type_norm == 'photo':
        return 'regular_stakes_photo_bw'

    # Category 5: large_stakes_graphic_coloured
    if type_norm == 'large stake' and \
       colour_norm in ['copper', 'gold', 'silver', 'stone', 'marble'] and \
       decoration_type_norm == 'graphic':
        return 'large_stakes_graphic_coloured'

    # Category 6: large_stakes_graphic_bw
    if type_norm == 'large stake' and \
       colour_norm in ['black', 'slate'] and \
       decoration_type_norm == 'graphic':
        return 'large_stakes_graphic_bw'

    # Category 7: large_stakes_photo_coloured
    if type_norm == 'large stake' and \
       colour_norm in ['copper', 'gold', 'silver', 'stone', 'marble'] and \
       decoration_type_norm == 'photo':
        return 'large_stakes_photo_coloured'

    # Category 8: large_stakes_photo_bw
    if type_norm == 'large stake' and \
       colour_norm in ['black', 'slate'] and \
       decoration_type_norm == 'photo':
        return 'large_stakes_photo_bw'

    # Category 9: small_stakes_graphic_coloured
    if type_norm in ['small stake', 'small metal'] and \
       colour_norm in ['copper', 'gold', 'silver', 'stone', 'marble'] and \
       decoration_type_norm == 'graphic':
        return 'small_stakes_graphic_coloured'

    # Category 10: small_stakes_graphic_bw
    if type_norm in ['small stake', 'small metal'] and \
       colour_norm in ['black', 'slate'] and \
       decoration_type_norm == 'graphic':
        return 'small_stakes_graphic_bw'

    # Category 11: heart_stakes_graphic
    if type_norm == 'heart stake' and decoration_type_norm == 'graphic':
        return 'heart_stakes_graphic'

    # Category 12: metal_products_raw
    # Ensure DecorationType is 'none' or empty for this category
    if ('metal' in type_norm or type_norm in ['large metal', 'medium metal', 'small metal']) and \
       (decoration_type_norm == 'none' or not decoration_type_norm) :
        return 'metal_products_raw'

    return 'unclassified'

def main():
    try:
        df = pd.read_csv('assets/SKULIST.csv')
    except FileNotFoundError:
        print("Error: 'assets/SKULIST.csv' not found.")
        return

    # Normalize relevant columns for processing
    # Ensure columns exist before trying to access .str attribute
    if 'TYPE' in df.columns:
        df['TYPE_norm'] = df['TYPE'].astype(str).str.lower().str.strip()
    else:
        df['TYPE_norm'] = '' # Create empty column if original is missing
        print("Warning: 'TYPE' column missing from CSV. ProcessorCategory may be inaccurate.")

    if 'COLOUR' in df.columns:
        df['COLOUR_norm'] = df['COLOUR'].astype(str).str.lower().str.strip()
    else:
        df['COLOUR_norm'] = ''
        print("Warning: 'COLOUR' column missing from CSV. ProcessorCategory may be inaccurate.")

    if 'DecorationType' in df.columns:
        df['DecorationType_norm'] = df['DecorationType'].astype(str).str.lower().str.strip()
    else:
        df['DecorationType_norm'] = ''
        print("Warning: 'DecorationType' column missing from CSV. ProcessorCategory may be inaccurate.")

    df['ProcessorCategory'] = df.apply(determine_processor_category, axis=1)

    # Log category counts
    category_counts = df['ProcessorCategory'].value_counts()
    print("SKU Counts per ProcessorCategory:")
    for category, count in category_counts.items():
        print(f"- {category}: {count}")

    # Drop temporary normalized columns before saving
    df.drop(columns=['TYPE_norm', 'COLOUR_norm', 'DecorationType_norm'], inplace=True)

    try:
        df.to_csv('assets/SKULIST.csv', index=False)
        print("\nSuccessfully processed SKULIST.csv and added ProcessorCategory column.")
    except Exception as e:
        print(f"\nError writing to 'assets/SKULIST.csv': {e}")

if __name__ == '__main__':
    main()

# Detailed Project Description: Amazon Order Processor & SVG Generator

This document provides a detailed description of the core application logic, including order processing, SVG generation, and GUI interactions.

## Order Processing Workflow

The order processing workflow begins with user input and culminates in a structured dataset ready for SVG generation.

1.  **Order File Ingestion:**
    *   Users initiate the process by dragging and dropping Amazon order files (typically `.txt` format) onto a designated "DropZone" in the PyQt5 GUI (`main_gui_qt_clean.py`).
    *   The application can handle multiple files dropped simultaneously.

2.  **Data Parsing and Processing (`001 AMAZON DATA DOWNLOAD/order_pipeline.py`):**
    *   When the "Process" button is clicked in the GUI, the `process_orders` method in `main_gui_qt_clean.py` is invoked. This method calls `order_pipeline.process_amazon_orders` from the `001 AMAZON DATA DOWNLOAD` directory.
    *   The `order_pipeline.py` script (assisted by parsing logic likely adapted from `app.py` in the same directory) handles the core data extraction:
        *   It reads the input `.txt` report files, which are expected to be tab-separated value (TSV) files.
        *   It extracts URLs pointing to ZIP files that contain detailed order customization data (XML) and customer-uploaded images.
        *   For each order, it downloads the ZIP file using the `requests` library.
        *   The ZIP file is extracted into a temporary directory.
        *   An XML file within the extracted contents is parsed using `xml.etree.ElementTree` to find customization details like chosen graphics and personalized text lines (e.g., "Line 1", "Line 2", "Line 3").
    *   The pipeline script iterates through all orders from the input files, compiling a list of dictionaries or a pandas DataFrame.

3.  **Role of `assets/SKULIST.csv`:**
    *   During processing by `order_pipeline.py` (and potentially referenced again in `main_gui_qt_clean.py` during table rendering or SVG processor selection), the `assets/SKULIST.csv` file is crucial.
    *   This CSV file acts as a lookup table. The SKU (Stock Keeping Unit) from the Amazon order data is used to find corresponding product information in `SKULIST.csv`.
    *   This enriches the order data with vital details like `Type` (e.g., "Regular Stake", "Large Photo Stake", "Small Metal"), `Colour`, and `Theme`. This information is essential for determining which SVG processor to use and for applying correct design attributes.

4.  **Product Image Handling:**
    *   If the order involves a customer image (e.g., for photo memorial stakes), the `order_pipeline.py` script identifies image files (typically JPEGs) within the downloaded ZIP archive.
    *   The script usually selects the largest JPG file (if multiple are present) and copies it to a dedicated `images/` directory in the project's root.
    *   The image is typically renamed using the `order-item-id` to ensure a unique filename. The path to this local image is then stored with the order data, making it accessible for the SVG generation phase.

## SVG Generation Process

Once orders are processed into a structured format (usually a pandas DataFrame displayed in the GUI), SVGs can be generated.

1.  **Invoking SVG Processors (from `002 D2C WRITER/`):**
    *   The `main_gui_qt_clean.py` application contains methods like `create_all_svgs` (for batch generation) and `create_design_for_selected` (for a single ticked row).
    *   These methods iterate through the processed orders (or the selected order).
    *   Based on the normalized `type`, `colour`, and `decorationtype` fields (often derived from `SKULIST.csv` or edited by the user), the GUI logic determines which specific SVG processor class to use from the `002 D2C WRITER/` directory.
    *   Examples of processors include `RegularStakesProcessor`, `PhotoStakesProcessor`, `BWLargeStakesProcessor`, `ColouredSmallStakesTemplateProcessor`, etc. Each is a Python class tailored to a specific product style.
    *   An instance of the chosen processor is created, passing paths to graphics assets and the output directory.

2.  **Use of Graphics and Templates from `assets/`:**
    *   **`assets/graphics/`**: The SVG processor classes heavily rely on this directory. It contains PNG and SVG files that are embedded or referenced in the generated SVGs (e.g., decorative borders, specific icons like angels or pets, background patterns). The processor selects the appropriate graphic based on the order's 'graphic' or 'theme' attribute.
    *   **`assets/002_svg_templates/`**: Some processors (e.g., `ColouredSmallStakesTemplateProcessor`, `BlackAndWhiteSmallStakesTemplateProcessor`) use base SVG files from this directory as templates. These templates contain placeholders or defined structures that the processor populates with specific text, colors, and graphics from the order. Other processors might construct the SVG from scratch using an SVG writing library like `svgwrite`.

3.  **Generating SVGs (Individual/All Orders):**
    *   **All Orders (`create_all_svgs`):** The application iterates through the entire list of processed orders in the main table. For each order, it determines the appropriate processor and calls its `process_orders` method (which typically handles filtering for relevant orders and then calls a `create_memorial_svg` or similar method for each).
    *   **Individual Order (`create_design_for_selected`):** Only the single row that has its "Tick" checkbox marked in the GUI table is processed. The logic extracts data for this row, determines the processor, and calls its SVG creation method (often `create_memorial_svg` or `populate_svg`).

4.  **Output to `SVG_OUTPUT/` Directory:**
    *   All generated SVG files are saved to the `SVG_OUTPUT/` directory within the project's root.
    *   Filenames for the SVGs are typically constructed dynamically, often including elements like `order-id`, `sku`, `type`, `colour`, and `graphic` to ensure uniqueness and traceability.
    *   The GUI also lists these generated SVG files and provides clickable links to open them.

## GUI Interactions (`main_gui_qt_clean.py`)

The PyQt5 GUI provides a central hub for managing the entire workflow.

1.  **Data Display:**
    *   Processed order data (from `order_pipeline.py`) is displayed in a `QTableWidget`.
    *   Columns include order details, `SKULIST.csv` derived data, customization text, image paths, and any warnings generated during processing.
    *   A `No.` column provides sequential numbering, and a `Tick` column allows users to select individual rows for actions.

2.  **Editing, Filtering, and Sorting:**
    *   **Editing:** Cells in the table are generally editable (double-click or select and press F2), allowing users to correct or modify data before SVG generation. Changes made in the table update the underlying pandas DataFrame. Some columns like 'Type' and 'Colour' might use QComboBoxes for controlled input.
    *   **Filtering:** A search box allows users to filter the displayed orders based on keywords. A "Show Only Warnings" checkbox filters orders that have issues flagged during processing.
    *   **Sorting:** The table can be sorted by clicking on column headers. The application also applies a default sort order (e.g., by Stake Type, Colour, DecorationType) after processing.

3.  **Triggering SVG Generation:**
    *   "Create SVGs" button: Triggers the `create_all_svgs` method to generate SVGs for all orders currently loaded and displayed in the table (respecting filters if any are applied to `last_df` before this call, though typically it uses `last_df`).
    *   "Create Design for Selected" button (and context menu option): Triggers `create_design_for_selected` for the single row whose "Tick" checkbox is checked.
    *   The GUI includes a log output area (QTextEdit) that displays messages about the progress of processing and SVG generation, including any errors.
    *   An SVG thumbnail preview area dynamically updates to show previews of generated SVGs, which are clickable to open the actual file.

4.  **Exporting Data and Managing State:**
    *   **Export:** "Export as CSV" and "Export as TXT" buttons allow users to save the current table data (respecting filters) to external files.
    *   **Copy to Clipboard:** A button allows copying the table data to the clipboard, typically in a tab-separated format for pasting into spreadsheets.
    *   **State Management:** The application uses `pickle` to save the current state of the main DataFrame (`last_df`) to `last_state.pkl` when closed and reloads it on startup, providing some persistence.
    *   **File/Folder Operations:** Buttons to "Open Output Folder" (opens `SVG_OUTPUT/`) and clear the table are also provided.
    *   The GUI lists generated SVG and associated CSV (if any) files in a separate table, allowing users to open them directly.
```

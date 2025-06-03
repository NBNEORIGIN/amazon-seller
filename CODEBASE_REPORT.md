# Codebase Report

# Overall Project Summary
# Project Overall Summary: Amazon Order Processor & SVG Generator

## Purpose and Use Case

This application serves as an **Amazon Seller Order Processor**, specifically designed to streamline and automate the workflow for handling personalized product orders, primarily memorial stakes. It caters to sellers who offer products with customizable text, graphics, and customer-uploaded photos. The core problem it solves is the manual effort and potential for error involved in translating Amazon order details into production-ready design files.

## Core Workflow

The application follows a clear workflow:

1.  **Order Ingestion & Processing:** Users input Amazon order report files (typically `.txt` files) into a PyQt5-based Graphical User Interface (GUI). The system, driven by scripts in the `001 AMAZON DATA DOWNLOAD` directory (notably `order_pipeline.py`), parses these reports. This involves downloading associated ZIP files containing XML customization data and customer images, extracting relevant details (SKU, personalized text, graphic choices, image paths), and enriching this data using a central `assets/SKULIST.csv` for product type, color, and theme mapping. Downloaded images are stored in the `images/` folder.

2.  **SVG Generation:** Based on the processed and enriched order data, the application generates Scalable Vector Graphics (SVG) files suitable for manufacturing. This is handled by a suite of specialized Python "processor" classes located in the `002 D2C WRITER/` directory. Each processor is tailored to a specific product type (e.g., regular stake, photo stake, B&W, colored, different sizes). These processors utilize predefined graphics from `assets/graphics/` and SVG templates from `assets/002_svg_templates/` to create the final designs. Generated SVGs are saved in the `SVG_OUTPUT/` directory.

3.  **GUI Management & Interaction:** The `main_gui_qt_clean.py` script provides the user interface for managing this entire process. It allows users to:
    *   Drag and drop order files.
    *   View processed orders in an editable table.
    *   Manually correct or adjust order details.
    *   Filter and sort orders.
    *   Trigger SVG generation for individual or all orders.
    *   Preview generated SVG thumbnails.
    *   Export data to CSV/TXT and manage application state.

## Key Technologies

The application is built primarily with **Python**. Core technologies include:

*   **PyQt5:** For the graphical user interface.
*   **pandas:** For robust data handling and manipulation of order information.
*   **requests:** For downloading order-related files from URLs.
*   **xml.etree.ElementTree:** For parsing XML customization data.
*   **svgwrite** (implied): For programmatic creation of SVG files by the various processors.
*   Standard Python libraries for file I/O and system interaction.

## Structure Overview

The project is organized into functional directories: `001 AMAZON DATA DOWNLOAD/` for initial data capture, `002 D2C WRITER/` for SVG generation logic, `assets/` for essential resources (SKU lists, graphics, templates), and `core/` for some underlying business logic modules. Output files are directed to `images/` (for customer photos) and `SVG_OUTPUT/` (for final production SVGs). An `llm_integration/` directory suggests ongoing or future development of AI-powered features.

In essence, this application transforms raw Amazon order data into actionable manufacturing designs, significantly improving efficiency for sellers of personalized goods.

# Project Summary
# Project Summary: Amazon Seller Order Processor & SVG Generator

## Project Purpose

This project is designed as an **Amazon Seller Order Processor**. Its primary purpose is to automate the workflow for processing personalized product orders from Amazon. It involves parsing Amazon order files, extracting customization details (text, graphics, images), and preparing them for manufacturing by generating Scalable Vector Graphics (SVG) files for various product types, primarily memorial stakes.

## Core Functionality

The application integrates several core functionalities:

1.  **Order Processing:**
    *   Ingests Amazon order files (typically `.txt` files which may contain links to ZIP archives with XML and image data).
    *   Parses these files to extract order details such as Order ID, SKU, quantity, customer-provided text lines, and graphic/image choices.
    *   Utilizes a `SKULIST.csv` file to map SKUs to specific product attributes like type (e.g., "Regular Stake", "Large Photo Stake"), color, and theme.
    *   Downloads and processes associated images for photo-based products.
    *   Includes data validation and warning generation for potential issues in order data (e.g., formatting, future dates).

2.  **SVG Generation:**
    *   Generates SVG files based on the processed order data, tailored for manufacturing.
    *   Supports a variety of product types and styles, including:
        *   Regular stakes
        *   Photo stakes
        *   Black & White (B&W) stakes
        *   Coloured stakes
        *   Small and Large variants of the above.
    *   Different Python classes (processors) handle the specific SVG generation logic for each product type, incorporating text, graphics, and images into predefined templates or structures.

3.  **Graphical User Interface (GUI):**
    *   Provides a user-friendly interface built with PyQt5.
    *   Allows users to drag and drop Amazon order files for processing.
    *   Displays processed order data in an editable table format.
    *   Enables users to trigger SVG generation for individual orders or in batch.
    *   Features an SVG thumbnail preview pane for generated designs.
    *   Offers functionality to export order data to CSV or TXT files.
    *   Includes basic table manipulation features like adding or deleting rows.

## Key Technologies Used

*   **Programming Language:** Python
*   **GUI Framework:** PyQt5
*   **Data Handling & Manipulation:** pandas (for managing order data in DataFrames)
*   **SVG Generation:** Likely `svgwrite` (listed as a dependency and common for Python SVG creation) and custom SVG templating/generation logic within processor classes.
*   **Web Requests:** `requests` (for downloading order-related files like ZIP archives from URLs).
*   **XML Parsing:** `xml.etree.ElementTree` (for extracting data from XML files within order downloads).
*   **File Handling:** Standard Python libraries for file I/O, ZIP file extraction.
*   **Clipboard:** `pyperclip` (for copying table data).
*   **Other Dependencies:** NumPy, Matplotlib, Seaborn (their specific use in the primary workflow is less prominent but they are listed as dependencies, potentially for auxiliary tasks like sales analysis).

# Project Structure Summary
# Project Structure Summary

This document outlines the directory structure and key files of the Amazon Seller Order Processor project.

## Main Directories and Their Roles

*   **`/` (Root Directory):**
    *   Contains the main application script (`main_gui_qt_clean.py`), startup scripts (`run_gui.bat`), dependency management (`requirements.txt`, `install_requirements.py`), and various configuration/utility files. Also, houses top-level project documentation like this summary.

*   **`000 ARCHIVE/`:**
    *   Appears to hold older versions of the codebase, experimental features (like `SPAPI_Python_SDK`), previous configurations, and recovery points. This directory is likely for historical reference and not part of the active application.

*   **`001 AMAZON DATA DOWNLOAD/`:**
    *   This directory is crucial for the initial order processing steps.
    *   Contains scripts for fetching, parsing, and processing Amazon order report files (often `.txt` files containing links to ZIPs with XML/image data).
    *   Key scripts like `app.py` (likely a standalone script for this part) and `order_pipeline.py` (used by the main GUI) orchestrate the download, extraction of order details (SKU, customization, image paths), and initial data structuring.
    *   Also holds sample order files (`.txt`) and test CSVs.

*   **`002 D2C WRITER/` (Direct-to-Customer Writer):**
    *   This directory is central to the SVG generation process.
    *   It contains various Python scripts, each responsible for generating SVGs for specific types of memorial stakes (e.g., `regular_stakes.py`, `photo_stakes.py`, `bw_large_stakes.py`, `coloured_small_stakes_template_processor.py`). These are referred to as "processors."
    *   `main.py` in this directory seems to be a script for batch processing orders using these SVG generators, possibly for testing or an older workflow.
    *   The main GUI application directly imports and uses these processor classes.

*   **`003 SALES/`:**
    *   Contains sales-related data, such as sample sales reports (`.txt`, `.csv`) and potentially scripts or outputs related to sales analysis (e.g., `output_heatmap.csv`). Its direct integration with the main order processing GUI is not immediately apparent but might be a separate utility.

*   **`assets/`:**
    *   Stores essential data and resources required by the application.
    *   `assets/SKULIST.csv`: A critical file that maps Amazon SKUs to product types, colors, themes, and other attributes used in order processing and SVG generation.
    *   `assets/graphics/`: Contains various graphic files (PNG, SVG) used as design elements in the SVG generation process (e.g., celtic patterns, floral designs, specific product graphics).
    *   `assets/002_svg_templates/`: Holds base SVG template files (e.g., `small_colour.svg`) that are populated with order-specific data by some of the SVG processors.

*   **`core/`:**
    *   This directory seems to represent an effort to structure the application's logic more formally.
    *   `core/order_manager.py`: Aims to handle order data loading, validation, and manipulation independently of the GUI.
    *   `core/svg_generator.py`: Intended to be a centralized module for SVG creation, delegating to different stake processors.
    *   `core/processors/`: Likely planned to contain the individual SVG processor modules (though many are still in `002 D2C WRITER/`).
    *   While present, the main GUI (`main_gui_qt_clean.py`) still directly uses many components from `002 D2C WRITER/` and `001 AMAZON DATA DOWNLOAD/`.

*   **`images/`:**
    *   The default output directory where images downloaded from Amazon orders (e.g., customer photos for photo stakes) are stored.

*   **`SVG_OUTPUT/`:** (Not listed in `ls()` root, but created by the application)
    *   This is the default output directory where the generated SVG files are saved by the application.

*   **`llm_integration/`:**
    *   Contains scripts and files related to integrating Large Language Models (LLMs), possibly for tasks like text processing, summarization, or other AI-driven features. This includes scripts for downloading models from Hugging Face (`download_from_hf.py`, `download_llama.py`), model conversion (`convert_to_gguf.py`), and interfacing with LLMs (`llm_interface.py`). This functionality might be experimental or a newer addition.

*   **`BACKUP SCRIPTS/`:**
    *   Contains backup versions of key scripts, like `main_gui_qt_clean backup 040525 1520.txt`.

## Key Files and Their Responsibilities

*   **`main_gui_qt_clean.py`:**
    *   The main executable Python script for the application.
    *   Launches the PyQt5-based graphical user interface.
    *   Integrates functionalities for order processing (by calling `order_pipeline.py`) and SVG generation (by instantiating and using processor classes from `002 D2C WRITER/`).
    *   Handles user interactions, table display, file operations, and SVG preview.

*   **`run_gui.bat`:**
    *   A batch script for easily running the main GUI application (`main_gui_qt_clean.py`) on Windows.

*   **`001 AMAZON DATA DOWNLOAD/order_pipeline.py`:**
    *   A core script responsible for the Amazon order processing workflow.
    *   Takes order file paths, orchestrates the downloading of ZIP files, parsing of XML data, extraction of image URLs, and consolidates order information using `SKULIST.csv`.
    *   Called by `main_gui_qt_clean.py` to process dropped/selected order files.

*   **`001 AMAZON DATA DOWNLOAD/app.py`:**
    *   Appears to be a standalone script or an earlier version for processing Amazon data downloads, similar in function to `order_pipeline.py` but potentially run independently.

*   **SVG Processor Scripts (in `002 D2C WRITER/`):**
    *   Examples: `regular_stakes.py`, `photo_stakes.py`, `bw_large_stakes.py`, `coloured_small_stakes_template_processor.py`, etc.
    *   Each script defines a class (processor) that takes order data (usually a pandas DataFrame row or subset) and generates an SVG file tailored to that specific product type and its customizations.

*   **`assets/SKULIST.csv`:**
    *   A crucial CSV file acting as a database that maps product SKUs to their characteristics (type, color, theme, etc.). This information is vital for both displaying order details correctly and for selecting the appropriate SVG generation logic.

*   **`requirements.txt`:**
    *   Lists the Python dependencies required to run the project (e.g., PyQt5, pandas, requests).

*   **`install_requirements.py`:**
    *   A utility script to automatically check for and install missing dependencies listed in `requirements.txt`.

*   **`last_state.pkl`:**
    *   A pickle file used by `main_gui_qt_clean.py` to save and load the last DataFrame state, allowing some persistence between sessions.
```

# Detailed Project Description
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

# Project Dependencies
# Project Dependencies

This project relies on the following Python packages. These are listed in `requirements.txt` and can be installed using `pip install -r requirements.txt`.

## Core Dependencies

*   **pandas**: Used for data manipulation and analysis, particularly for handling order data in DataFrames.
*   **numpy**: A fundamental package for numerical computation in Python; often a dependency of pandas and other data science libraries.
*   **matplotlib**: A comprehensive library for creating static, animated, and interactive visualizations in Python. Its direct use in the main application is not prominent but might be used for utilities or is a dependency of seaborn.
*   **seaborn**: A Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.
*   **PyQt5**: Used as the GUI framework for building the desktop application interface.
*   **pyperclip**: A cross-platform Python module for copy and paste clipboard functions. Used in the GUI to copy table data.
*   **svgwrite**: A Python library to create SVG drawings. Used by the various SVG processors to generate the final manufacturing files.
*   **requests**: An elegant and simple HTTP library for Python, used for making web requests, particularly for downloading ZIP files containing order details from Amazon.

## Installation

The recommended way to install these dependencies is by running the following command in your terminal, within the project's root directory:

```bash
pip install -r requirements.txt
```

Alternatively, the project includes an `install_requirements.py` script that attempts to check for and install missing dependencies automatically.

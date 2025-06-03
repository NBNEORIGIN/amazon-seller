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

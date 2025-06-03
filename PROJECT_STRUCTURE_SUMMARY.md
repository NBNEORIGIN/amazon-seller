# Project Structure & File Purpose Summary

_Last updated: 2025-05-05 08:02 BST_

This document provides an overview of the purpose of each major file and folder in the project directory. It is intended as a reference and backup for onboarding, troubleshooting, and general understanding of the codebase.

---

## Top-Level Project Directory

- **.env**  
  Environment variables for API keys or configuration (may be used by scripts or for local settings).

- **.git, .gitignore**  
  Git version control folder and ignore rules.

- **.venv**  
  Python virtual environment for dependencies (local to this project).

- **000 ARCHIVE/**  
  Archive of old or backup files (not directly used in current processing).

- **001 AMAZON DATA DOWNLOAD/**  
  All scripts and data for downloading, parsing, and processing Amazon order data (see below for details).

- **002 D2C WRITER/**  
  All scripts for generating SVGs, batch CSVs, and handling product/stake design logic (see below for details).

- **003 SALES/**  
  Contains sales data files, heatmap outputs, and analysis scripts or results.

- **004 IMAGES/**  
  Contains all product/customer images referenced by orders and used in SVG generation.

- **005 Assets/**  
  Contains graphics assets (e.g., icons, backgrounds) and the `SKULIST.csv` file, which maps SKUs to product metadata.

- **BACKUP SCRIPTS/**  
  Folder for backup versions of main scripts (e.g., backup of main_gui_qt_clean).

- **PROJECT_SUMMARY.md**  
  Project overview, features, structure, and known issues—serves as a quick reference.

- **PrivateApp_API/**  
  (Purpose not clear from name—likely for private API integration or credentials.)

- **RECOVERY_POINT_*.md**  
  Recovery checkpoint files for restoring project state.

- **SVG_OUTPUT/**  
  Output folder for generated SVG and CSV files for processed orders.

- **create_recovery_point.bat / .py**  
  Scripts to create project recovery checkpoints.

- **llm_integration/**  
  Scripts and tools for integrating and managing local AI models (Llama, etc.). See below for details.

- **main_gui.py, main_gui_qt.py, main_gui_qt_clean.py**  
  Main GUI application scripts.  
  - `main_gui_qt_clean.py` is the primary, most up-to-date GUI for order processing and SVG generation.
  - Others are older or alternative versions.

- **main_gui_qt_clean_backup_20250504.py**  
  Backup of the main GUI script.

- **pyqt_test_qpushbutton.py**  
  Minimal test script for PyQt button functionality.

- **requirements.txt**  
  List of required Python packages for the project.

- **run_gui.bat, run_gui_with_update.bat**  
  Batch files to launch the GUI (with or without update steps).

---

## 001 AMAZON DATA DOWNLOAD/

- **app.py**  
  Main script for downloading and parsing Amazon order reports.

- **order_pipeline.py**  
  Orchestrates the order processing pipeline, including calling download, parsing, and output functions.

- **order_parser.py**  
  Parses individual Amazon order files into structured data.

- **api_client.py, auth_direct.py, get_auth_token.py, self_auth.py, self_authorize.py, test_api.py**  
  Scripts for authentication and API interaction (some may be legacy or for future Amazon API integration).

- **output.csv, output.txt**  
  Processed order data output files.

- **run_amazon_xml_processing.bat**  
  Batch file to run the Amazon XML processing pipeline.

- **004 IMAGES/**, **SVG_OUTPUT/**, **__pycache__/**  
  Output and cache folders for images, SVGs, and compiled Python files.

---

## 002 D2C WRITER/

- **regular_stakes.py, bw_stakes.py, photo_stakes.py, bw_large_stakes.py, bw_large_photo_stakes.py, coloured_large_stakes.py, coloured_large_photo_stakes.py, bw_photo_stakes.py**  
  Scripts for generating SVGs and batch CSVs for each product/stake type (regular, B&W, photo, large, coloured, etc.).

- **memorial_base.py**  
  Shared base logic for stake/memorial processing (e.g., QA, warnings, text formatting).

- **design_writer.py**  
  Likely handles the writing of design files or templates.

- **main.py**  
  Entry point for running stake processing from the command line.

- **run_memorial_processor.bat**  
  Batch file to run the memorial processor.

- **bw_photo_stakes BACKUP.py**  
  Backup of the B&W photo stakes script.

- **__pycache__/**  
  Python bytecode cache.

---

## 003 SALES/

- **AMAZON UK HEATMAP EXAMPLE.csv, ASSEMBLY.csv, SAMPLE SALES DATA.txt, output_heatmap.csv, output_heatmap_heatmap.png**  
  Sales data and analysis outputs (e.g., heatmaps, assembly data, sales samples).

- **Other .txt files**  
  Likely raw or processed sales/order data.

---

## 004 IMAGES/

- **(JPG files)**  
  All order- or product-related images referenced by the pipeline for SVG generation.

---

## 005 Assets/

- **001 Graphics/**  
  Graphics assets (icons, backgrounds, etc.) used in SVGs.

- **SKULIST.csv**  
  Master list mapping SKUs to product metadata (stake type, color, decoration, etc.).

---

## BACKUP SCRIPTS/

- **main_gui_qt_clean backup 040525 1520.txt**  
  Backup of the main GUI script as of a specific date.

---

## llm_integration/

- **configure_hf.py, configure_hf_direct.py, configure_token.py**  
  Scripts for configuring HuggingFace API/token for model downloads.

- **convert_model.py, convert_to_gguf.py**  
  Scripts for converting models to required formats.

- **download_from_hf.py, download_llama.py, download_llama_direct.py**  
  Scripts to download Llama or other models.

- **install_git_lfs.ps1**  
  PowerShell script to install Git LFS (Large File Storage).

- **llm_interface.py**  
  Main interface for interacting with local AI models.

- **models/**  
  Folder for storing downloaded or converted models.

- **requirements.txt**  
  Requirements for LLM integration.

- **setup_llama.py**  
  Script to set up the Llama model environment.

---

## SVG_OUTPUT/

- **(SVG and CSV files)**  
  Output files for each processed batch of orders and product type.

---

## Other Files

- **PrivateApp_API/**  
  (Unclear—likely for private API integration, credentials, or legacy code.)

---

If you want a more detailed summary or have questions about specific files, see the main `PROJECT_SUMMARY.md` or ask your AI assistant.

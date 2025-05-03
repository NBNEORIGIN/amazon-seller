# Project Summary: Automated Memorial Product Design & Order Management

**Date:** 2025-05-02

## Overview
This project automates the design, QA, and order management for memorial products sold across Amazon, Etsy, and eBay. It includes SVG generation, batch processing, and is being enhanced with AI (Llama 3.2-1B) for design and order QA.

---

## Key Features & Progress

### 1. Order Data Extraction & QA
- `app.py` processes Amazon order reports, extracting all required metadata and memorial text.
- Output files (`output.csv`, `output.txt`) now include a `Warnings` column that flags typos, grammar issues, future dates, and formatting problems in memorial text.
- All output rows correspond to a single memorial, correctly duplicated by the `number-of-items` field.

### 2. Stake/Product Processing
- `regular_stakes.py` and `bw_stakes.py` generate SVGs and batch CSVs for regular and black/white stakes.
- Batch CSVs now include:
  - `SVG FILE` (the exact SVG filename for each batch)
  - `DESIGN FILE`
  - All relevant memorial/order details
  - `WARNINGS` column for QA, using a shared warning generator in `memorial_base.py`
- Color support includes copper, gold, silver, marble, and stone.
- Logic is robust to missing or malformed fields.

### 3. AI Integration (In Progress)
- Llama 3.2-1B model integration for:
  - Design file QA
  - Inventory analysis
  - Order validation
- Local model deployment for data security
- Build environment (Python 3.11+, Visual Studio Build Tools, Git) is set up
- `llama-cpp-python` installation pending

### 4. Project Structure
- `001 AMAZON DATA DOWNLOAD/`: Data extraction and QA
- `002 D2C WRITER/`: Stake and product processing (SVG/CSV)
- `llm_integration/`: AI model integration
- `SVG_OUTPUT/`: Generated design files
- `main_gui.py`: Main application interface

---

## Known Issues & Next Steps
- Some rows in `output.csv` may be skipped if not meeting filter criteria (logging for skipped rows is a TODO).
- Awaiting Amazon SP-API access for full automation.
- Need to maintain `requirements.txt` and keep the virtual environment in sync.
- Complete `llama-cpp-python` installation and test AI-powered QA features.
- Continue development of new stake types and regular environment maintenance.

---

## Environment Setup
- Python 3.11+
- Visual Studio Build Tools
- Git
- Model Path: `C:/Users/zentu/.llama/checkpoints/Llama3.2-1B/`

---

**This summary is a checkpoint for quick project resumption after a restart.**

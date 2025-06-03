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

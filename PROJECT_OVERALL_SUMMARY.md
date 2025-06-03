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

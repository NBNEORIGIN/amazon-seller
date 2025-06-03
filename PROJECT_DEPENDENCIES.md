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

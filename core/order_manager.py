"""
Order Manager Module
-------------------
Handles order data loading, validation, and manipulation (add/delete row, renumber, etc).
This module is independent of the GUI and can be tested separately.
"""

import pandas as pd
from typing import Optional

class OrderManager:
    def __init__(self):
        self.orders = pd.DataFrame()

    def load_orders(self, filepath: str) -> pd.DataFrame:
        """Load orders from a CSV or Excel file."""
        if filepath.lower().endswith('.csv'):
            self.orders = pd.read_csv(filepath)
        elif filepath.lower().endswith(('.xls', '.xlsx')):
            self.orders = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file type: {filepath}")
        return self.orders

    def add_row(self, row_data: dict) -> None:
        """Add a new row to the orders DataFrame."""
        self.orders = pd.concat([self.orders, pd.DataFrame([row_data])], ignore_index=True)
        self.renumber()

    def delete_row(self, index: int) -> None:
        """Delete a row by index and renumber."""
        self.orders = self.orders.drop(index).reset_index(drop=True)
        self.renumber()

    def renumber(self) -> None:
        """Reassign 'No.' column for sequential numbering."""
        if 'No.' in self.orders.columns:
            self.orders['No.'] = range(1, len(self.orders) + 1)

    def remove_duplicates(self, column: str) -> None:
        """Remove duplicate rows based on a column (e.g., 'No.' or 'Tick')."""
        self.orders = self.orders.drop_duplicates(subset=[column]).reset_index(drop=True)

    def validate(self) -> Optional[str]:
        """Perform basic validation; return error message or None if OK."""
        if self.orders.empty:
            return "Order table is empty."
        # Add more validation as needed
        return None

# Example usage (for testing, not run by GUI):
if __name__ == "__main__":
    om = OrderManager()
    om.load_orders("example_orders.csv")
    om.add_row({'No.': 5, 'Name': 'Test'})
    om.delete_row(0)
    om.remove_duplicates('No.')
    print(om.orders)

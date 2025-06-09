print("RUNNING main_gui_qt.py FROM:", __file__)
import sys
import os
# --- Auto-install dependencies if missing ---
try:
    import pandas
    import numpy
    import matplotlib
    import seaborn
    import PyQt5
    import pyperclip
    import svgwrite
    import requests
except ImportError:
    import subprocess
    import pathlib
    installer = pathlib.Path(__file__).parent / 'install_requirements.py'
    print('Some dependencies are missing. Attempting to install them...')
    subprocess.check_call([sys.executable, str(installer)])
    print('Dependencies installed. Please restart the application if you see errors.')
    sys.exit(0)
# --- End auto-install block ---
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QSplitter, QHBoxLayout, QLineEdit, QCheckBox, QTextBrowser, QAction,
    QScrollArea, QTabWidget
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

# Import RegularStakesProcessor for SVG generation
from pathlib import Path
import pandas as pd
import sys
sys.path.append(str(Path(__file__).parent / '002 D2C WRITER'))
from regular_stakes import RegularStakesProcessor
from bw_stakes import BWStakesProcessor
from photo_stakes import PhotoStakesProcessor
from bw_large_stakes import BWLargeStakesProcessor
from coloured_large_photo_stakes import ColouredLargePhotoStakesProcessor
from bw_photo_stakes import BWPhotoStakesProcessor
from coloured_small_stakes_template_processor import ColouredSmallStakesTemplateProcessor
from coloured_large_stakes import ColouredLargeStakesProcessor
from bw_small_stakes_template_processor import BlackAndWhiteSmallStakesTemplateProcessor # Added this import

class DropZone(QLabel):
    file_dropped = pyqtSignal(list)  # Signal to emit list of file paths

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText('Drag and drop your Amazon order .txt file here')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont('Arial', 14))
        self.setStyleSheet('border: 2px dashed #aaa; padding: 40px; background: #fafafa;')
        self.setAcceptDrops(True)
        self.dropped_file = None
        self._drag_active = False

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._drag_active = True
            # Table-like appearance on drag
            self.setStyleSheet('border: 2px solid #1976d2; background: #fff; padding: 40px;'
                               'box-shadow: 0 0 8px #1976d2;'
                               'border-radius: 4px;'
                               'outline: 2px solid #1976d2;'
                               'outline-offset: -4px;'
                               'background-image: linear-gradient(90deg, #f8f8f8 49%, #e0e0e0 51%);'
                               'background-size: 20px 20px;'
                               'background-position: 0 0, 10px 10px;'
                               'background-repeat: repeat;')
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._drag_active = False
        self.setStyleSheet('border: 2px dashed #aaa; padding: 40px; background: #fafafa;')

    def dropEvent(self, event: QDropEvent):
        self._drag_active = False
        self.setStyleSheet('border: 2px dashed #aaa; padding: 40px; background: #fafafa;')
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            txt_files = [u.toLocalFile() for u in urls if u.toLocalFile().lower().endswith('.txt')]
            if txt_files:
                file_names = '\n'.join([os.path.basename(f) for f in txt_files])
                self.setText(f'Files selected:\n{file_names}')
                self.dropped_file = txt_files
                self.file_dropped.emit(txt_files)  # Emit all file paths as a list
            else:
                self.setText('Please drop .txt files!')
        else:
            event.ignore()

import pickle

class MainWindow(QMainWindow):
    # create_coloured_regular_photo_stake_for_selected method is now removed.
    # Its functionality is covered by the generalized create_design_for_selected.

    def contextMenuEvent(self, event):
        from PyQt5.QtWidgets import QMenu
        active_tab_widget = self.tabs.currentWidget()
        if not active_tab_widget: return
        active_table = active_tab_widget.findChild(QTableWidget)
        if not active_table: return

        pos = active_table.viewport().mapFromGlobal(event.globalPos())
        row = active_table.rowAt(pos.y())
        # column = active_table.columnAt(pos.x()) # If needed later

        if row < 0: # No row under cursor
            # Optionally, create a context menu for "add row" if table is empty or no specific row clicked
            # For now, only show if a valid row is clicked.
            return

        menu = QMenu(self)
        insert_above = menu.addAction("Insert Row Above")
        insert_below = menu.addAction("Insert Row Below")
        delete_row = menu.addAction("Delete Row")
        create_design = menu.addAction("Create Design for Selected")
        # create_coloured_regular_photo_stake action is removed
        action = menu.exec_(event.globalPos())
        if action == insert_above:
            self.insert_row_at(row)
        elif action == insert_below:
            self.insert_row_at(row + 1)
        elif action == delete_row:
            self.delete_row_at(row)
        elif action == create_design:
            self.create_design_for_selected()
        # elif action == create_coloured_regular_photo_stake: # Removed
            # self.create_coloured_regular_photo_stake_for_selected()

    def insert_row_at(self, row_index):
        import pandas as pd
        active_tab_widget = self.tabs.currentWidget()
        if not active_tab_widget: return
        active_table = active_tab_widget.findChild(QTableWidget)
        if not active_table: return
        category_name = active_table.property("category_name")
        if not category_name or category_name not in self.categorized_dfs:
            self.log("Cannot insert row: active category data not found.")
            return

        df = self.categorized_dfs[category_name]
        if df is None: # Should not happen if category_name is in categorized_dfs
            self.log("Cannot insert row: DataFrame for category is None.")
            return

        # Ensure 'No.' and 'Tick' columns exist, handle if not.
        if 'No.' not in df.columns: df.insert(0, 'No.', "") # Or some default logic
        if 'Tick' not in df.columns: df.insert(1, 'Tick', "") # Or some default logic

        blank_row_data = {col: "" for col in df.columns}
        # 'No.' will be reassigned later, 'Tick' is blank by default for new row.

        # Insert blank row into DataFrame
        if row_index > len(df): row_index = len(df) # Append if index is out of bounds
        df_top = df.iloc[:row_index]
        df_bottom = df.iloc[row_index:]
        new_df = pd.concat([df_top, pd.DataFrame([blank_row_data]), df_bottom], ignore_index=True)

        # Reassign 'No.' column sequentially
        new_df['No.'] = range(1, len(new_df) + 1)

        self.categorized_dfs[category_name] = new_df
        self.active_category_df = new_df # Update active_category_df as well

        # Re-render the table for the current tab (or call filter_table which should also re-render)
        self._render_table(new_df, active_table) # Or self.filter_table()
        self.log(f'Inserted a new blank row at position {row_index + 1} in tab "{category_name}".')

    def delete_row(self): # Button action
        active_tab_widget = self.tabs.currentWidget()
        if not active_tab_widget: return
        active_table = active_tab_widget.findChild(QTableWidget)
        if not active_table: return

        selected_row_index = active_table.currentRow()
        if selected_row_index < 0:
            self.log('No row selected to delete.')
            return
        self.delete_row_at(selected_row_index)

    def delete_row_at(self, row_index): # Context menu or direct call
        active_tab_widget = self.tabs.currentWidget()
        if not active_tab_widget: return
        active_table = active_tab_widget.findChild(QTableWidget)
        if not active_table: return
        category_name = active_table.property("category_name")

        if not category_name or category_name not in self.categorized_dfs:
            self.log("Cannot delete row: active category data not found.")
            return

        df = self.categorized_dfs[category_name]
        if row_index < 0 or row_index >= len(df):
            self.log(f"Cannot delete row: index {row_index} out of bounds for DataFrame of length {len(df)}.")
            return

        new_df = df.drop(df.index[row_index]).reset_index(drop=True)
        if 'No.' in new_df.columns:
            new_df['No.'] = range(1, len(new_df) + 1) # Re-number

        self.categorized_dfs[category_name] = new_df
        self.active_category_df = new_df

        self._render_table(new_df, active_table) # Or self.filter_table()
        self.log(f'Deleted row {row_index + 1} from tab "{category_name}".')
        # Update button states as table content changed
        self.on_tab_changed(self.tabs.currentIndex())


    def add_row(self): # Button action, adds to end
        active_tab_widget = self.tabs.currentWidget()
        if not active_tab_widget:
            self.log("No active tab to add a row to.")
            return
        active_table = active_tab_widget.findChild(QTableWidget)
        if not active_table:
            self.log("No table in active tab to add a row to.")
            return

        category_name = active_table.property("category_name")
        if not category_name or category_name not in self.categorized_dfs:
            self.log(f"Cannot add row: data for category '{category_name}' not found.")
            return

        df = self.categorized_dfs[category_name]

        # Ensure essential columns exist, add if not (especially for an empty initial DF)
        expected_cols = ['No.', 'Tick', 'order-id', 'sku', 'type', 'colour', 'graphic', 'line_1', 'line_2', 'line_3', 'decorationtype', 'processor_category', 'Warnings'] # Add more as needed
        for col_name in expected_cols:
            if col_name not in df.columns:
                df[col_name] = "" # Initialize with empty string or appropriate default

        blank_row_data = {col: "" for col in df.columns}
        blank_row_data['No.'] = len(df) + 1 # Temp 'No.', will be reassigned by _render_table or here
        blank_row_data['Tick'] = ''

        new_df = pd.concat([df, pd.DataFrame([blank_row_data])], ignore_index=True)
        new_df['No.'] = range(1, len(new_df) + 1) # Re-number

        self.categorized_dfs[category_name] = new_df
        self.active_category_df = new_df

        self._render_table(new_df, active_table) # Or self.filter_table()
        self.log(f'Added a new blank row to tab "{category_name}".')
        self.on_tab_changed(self.tabs.currentIndex()) # Update button states

    def create_design_for_selected(self):
        from PyQt5.QtWidgets import QMessageBox
        import pandas as pd

        active_tab_widget = self.tabs.currentWidget()
        if not active_tab_widget:
            self.log("No active tab for creating design.")
            return
        active_table = active_tab_widget.findChild(QTableWidget)
        if not active_table:
            self.log("No table in active tab for creating design.")
            return

        category_name = active_table.property("category_name")
        if not category_name:
            self.log("Could not determine category for the active tab.")
            return

        tick_col_idx = None
        for col_idx_loop in range(active_table.columnCount()):
            header_item = active_table.horizontalHeaderItem(col_idx_loop)
            if header_item and header_item.text().strip().lower() == 'tick':
                tick_col_idx = col_idx_loop
                break

        if tick_col_idx is None:
            self.log('No "Tick" column found in the active table.')
            return

        checked_rows_indices = []
        for row_idx_loop in range(active_table.rowCount()):
            item = active_table.item(row_idx_loop, tick_col_idx)
            if item and item.checkState() == Qt.Checked:
                checked_rows_indices.append(row_idx_loop)

        self.log(f"Checked rows in active table: {checked_rows_indices}")
        if len(checked_rows_indices) != 1:
            QMessageBox.warning(self, 'Select One Row', 'Please tick exactly one row in the active table to create a design.')
            return

        selected_row_view_index = checked_rows_indices[0]

        # Map view index to DataFrame index if filtering/sorting is active
        # For now, assume view index directly maps to self.active_filtered_df or self.active_category_df
        # This needs robust handling if self.active_filtered_df is the source for rendering.

        category_name = active_table.property("category_name")
        source_df = None
        if hasattr(self, 'active_filtered_df') and self.active_filtered_df is not None and category_name == self.active_filtered_df.get('category_name_prop_if_set'): # Check if active_filtered_df is for current tab
             # This comparison is tricky. Need a reliable way to know if active_filtered_df is for current tab.
             # Simplification: If filter is active, it's assumed active_filtered_df is the source.
             if self.search_box.text().strip() or self.warnings_only_checkbox.isChecked():
                 source_df = self.active_filtered_df
             else: # No filter active, use active_category_df
                 source_df = self.active_category_df
        elif self.active_category_df is not None:
            source_df = self.active_category_df

        if source_df is None or selected_row_view_index >= len(source_df):
             self.log("Cannot create design: selected row index out of bounds for source DataFrame.")
             return

        selected_row_data_series = source_df.iloc[selected_row_view_index]
        single_df = pd.DataFrame([selected_row_data_series.to_dict()]) # Create a new DF with just this row

        # Remove 'No.' and 'Tick' columns from the data sent to the processor
        # Ensure 'data' variable from original code is correctly replaced by selected_row_data_series.to_dict()
        # The original code had: single_df = pd.DataFrame([data])
        # where data was a dict built from table items.
        # Now, single_df is built from source_df.iloc[selected_row_view_index]
        # So, we operate on this single_df
        cols_to_drop = [col for col in ['No.', 'Tick'] if col in single_df.columns]
        if cols_to_drop:
            single_df = single_df.drop(columns=cols_to_drop)

        try:
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SVG_OUTPUT")
            graphics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "graphics")
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(graphics_path, exist_ok=True)


            processor_class = self.processor_map.get(category_name)

            if processor_class:
                self.log(f"Using processor {processor_class.__name__} for category '{category_name}' to create design for selected row.")

                processor_instance = None
                # Handle processors that might need a template path differently
                if category_name in ["small_stakes_graphic_coloured", "small_stakes_graphic_bw"]:
                    template_name = "small_colour.svg" if category_name == "small_stakes_graphic_coloured" else "small_bw.svg"
                    template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "002_svg_templates", template_name)
                    if not os.path.exists(template_file_path):
                        self.log(f"Error: Template file not found for {category_name}: {template_file_path}")
                        QMessageBox.warning(self, "Template Missing", f"Template file {template_name} not found.")
                        return
                    processor_instance = processor_class(template_file_path, output_dir, graphics_path)
                else:
                    processor_instance = processor_class(graphics_path, output_dir)

                df_for_processor = single_df.copy()
                df_for_processor.columns = [col.lower() for col in df_for_processor.columns]


                # Processors might need a specific method for single items or handle DataFrame with one row in process_orders
                if hasattr(processor_instance, 'populate_svg') and category_name in ["small_stakes_graphic_coloured", "small_stakes_graphic_bw"]:
                    # Construct a filename. This logic should ideally be part of the processor itself.
                    order_data_series = df_for_processor.iloc[0] # populate_svg usually expects a Series or dict
                    order_id_val = str(order_data_series.get('order-id', 'NA')).strip()
                    sku_val = str(order_data_series.get('sku', 'NA')).strip()
                    # Customize filename based on what makes sense for single file generation
                    # Using order_item_id if available, else part of order_id and sku
                    order_item_id_val = str(order_data_series.get('order-item-id', '')).strip()
                    if order_item_id_val :
                        filename_base = order_item_id_val
                    else:
                        filename_base = f"{order_id_val}_{sku_val}_selected_design"

                    output_svg_path = os.path.join(output_dir, f"{filename_base.replace(' ', '_').replace('/', '_')}.svg")
                    processor_instance.populate_svg(order_data_series, output_svg_path)
                    self.log(f"SVG generated for selected row: {output_svg_path}")
                else: # Default to process_orders for other processors
                    processor_instance.process_orders(df_for_processor)
                    self.log(f"SVG generation initiated for selected row using {processor_class.__name__}. Check SVG_OUTPUT folder for file(s).")

                self.list_output_files(output_dir)
                self.refresh_svg_thumbnails()
            else:
                QMessageBox.warning(self, 'No Matching Processor', f"No SVG processor is mapped for category '{category_name}'.")
                self.log(f"No SVG processor mapped for category '{category_name}'.")

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(f'Error during single design generation for category {category_name}:\n{tb}')
            QMessageBox.critical(self, "Error Generating Design", f"An error occurred: {e}")

    def log(self, message):
        # Append message to the log output widget and print to console
        if hasattr(self, 'log_output') and self.log_output is not None:
            self.log_output.append(message)
        print(message)

    def on_table_cell_changed(self, item, column=None):
        from PyQt5.QtCore import Qt
        # Support both (item: QTableWidgetItem) and (row: int, column: int) signatures
        # This method is connected to itemChanged signal of QTableWidget.
        # The 'item' argument is the QTableWidgetItem that was changed.

        if not item: return

        row = item.row()
        column = item.column()

        active_tab_widget = self.tabs.currentWidget()
        if not active_tab_widget: return
        active_table = active_tab_widget.findChild(QTableWidget)
        if not active_table: return

        category_name = active_table.property("category_name")
        if not category_name or category_name not in self.categorized_dfs:
            self.log(f"Error in on_table_cell_changed: Category '{category_name}' not found in data.")
            return

        # Determine which DataFrame to update: the filtered one or the original one for the category.
        # It's generally safer to update the original DataFrame (self.categorized_dfs[category_name])
        # and then re-apply filters if necessary. Mapping view row to original DF row is key.

        # For now, let's assume row index from view maps to active_category_df (which could be filtered or original)
        # This is a simplification. A robust solution needs to map view index to original DF index.
        target_df = self.active_category_df
        if hasattr(self, 'active_filtered_df') and self.active_filtered_df is not None:
            # If filter is active, assume 'row' is an index into active_filtered_df
            # However, we need to update the *original* DataFrame in self.categorized_dfs
            # This requires finding the original index from the filtered index.
            # This is complex if active_filtered_df is a sliced copy.
            # For simplicity now, if active_filtered_df exists, we might be updating a copy, which is not ideal.
            # A better approach: on_table_cell_changed ALWAYS updates self.categorized_dfs[category_name]
            # and then calls self.filter_table() to refresh the view.

            # Let's try to update self.categorized_dfs[category_name]
            # This requires knowing the original index of the row in self.categorized_dfs[category_name]
            # that corresponds to `row` in the potentially filtered `active_table`.
            # If `_render_table` uses a direct copy for filtering, `row` is the index in that copy.
            # If `_render_table` uses original df's indices, then `row` could be non-contiguous.

            # Simplification: Assume `_render_table` populates table from a df (filtered or not)
            # and `row` is the direct index into *that* df.
            # The challenge is ensuring `self.active_category_df` is the correct reference or copy.

            # If self.active_category_df is a *copy* (e.g. from filtering), changes here won't persist to self.categorized_dfs
            # Let's assume self.active_category_df IS self.categorized_dfs[category_name] when no filter is active,
            # and self.active_filtered_df is a separate copy when filter is active.

            # The current filter_table renders from a copy. So, if a filter is active,
            # item.row() refers to a row in self.active_filtered_df.
            # We need to find the corresponding row in self.categorized_dfs[category_name].
            # This requires the original index to be preserved in active_filtered_df.

            # Let's assume for now: if self.active_filtered_df exists, `row` is its index.
            # And we need to find the *original* index from it.
            # If active_filtered_df was created with reset_index(drop=True), original index is lost.
            # If created with reset_index(drop=False), original index is in 'index' column.

            # Current filter_table does df_to_filter = self.active_category_df.copy() then filters.
            # So self.active_filtered_df has its own index.

            # This part is tricky and needs a consistent strategy for index mapping.
            # For now, let's try to update self.categorized_dfs[category_name]
            # This means `row` from the view must map to an index in self.categorized_dfs[category_name]
            # This is only true if the table is rendered directly from self.categorized_dfs[category_name] (i.e. no filter)

            # Let's assume the `row` is an index for `self.active_category_df` which should be `self.categorized_dfs[category_name]`
            # (This assumption breaks if filtering is active and `active_category_df` isn't updated to point to the filtered copy correctly)

            df_to_update = self.categorized_dfs[category_name] # Always aim to update the source

            # What is 'row'? It's the view row. Does it map to df_to_update's index?
            # If filter_table uses df_to_update to render, then yes.
            # Current filter_table uses a copy, then renders. So 'row' is index of that copy.

            # This needs a robust way to get the original index.
            # Simplest (but not fully robust if sorting/filtering changes index mapping without explicit index column):
            # Assume `row` is the index in the *currently displayed* table.
            # If `active_filtered_df` is displayed, `row` is its index.
            # If `active_category_df` (the original) is displayed, `row` is its index.

            displayed_df = self.active_filtered_df if hasattr(self, 'active_filtered_df') and self.active_filtered_df is not None and (self.search_box.text().strip() or self.warnings_only_checkbox.isChecked()) else self.categorized_dfs[category_name]

            if row >= len(displayed_df):
                 self.log(f"Warning: Row index {row} out of bounds for displayed DataFrame in on_table_cell_changed.")
                 return

            original_index = displayed_df.index[row] # Get the actual index label from the displayed DataFrame

            header_item = active_table.horizontalHeaderItem(column)
            if not header_item: return
            col_name = header_item.text()
            new_value = item.text()

            if item.flags() & Qt.ItemIsUserCheckable: # Handle checkbox for 'Tick' column
                if col_name.lower() == 'tick':
                    new_value = '1' if item.checkState() == Qt.Checked else '0'
                    self.log(f"Tickbox changed: row={row}, col_name={col_name}, new_value='{new_value}' (orig_idx={original_index})")

            # Update the original DataFrame in self.categorized_dfs
            if original_index in self.categorized_dfs[category_name].index and col_name in self.categorized_dfs[category_name].columns:
                self.categorized_dfs[category_name].loc[original_index, col_name] = new_value
                self.log(f"Updated DataFrame for '{category_name}': row_orig_idx={original_index}, col='{col_name}', new_val='{new_value}'")

                # If a filter is active, we might need to update active_filtered_df too, or just re-filter
                if hasattr(self, 'active_filtered_df') and self.active_filtered_df is not None and (self.search_box.text().strip() or self.warnings_only_checkbox.isChecked()):
                    # Option 1: Try to update active_filtered_df in place (if `row` is its index and `original_index` was for the source)
                    if row < len(self.active_filtered_df) and col_name in self.active_filtered_df.columns:
                         self.active_filtered_df.loc[self.active_filtered_df.index[row], col_name] = new_value # Assuming 'row' is index for this filtered df
                    # Option 2: Re-filter (safer for complex filters/sorts) - but avoid recursion if cell change triggers filter_table
                    # self.filter_table() # This might cause issues if not handled carefully.
            else:
                self.log(f"Warning: Could not update DataFrame. Original index {original_index} or column '{col_name}' not found in self.categorized_dfs['{category_name}'].")

        self.update_preview_pane() # Currently a no-op but good to keep



    def create_all_svgs(self):
        if not self.categorized_dfs:
            self.log('No categorized orders available for SVG generation.')
            return

        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SVG_OUTPUT")
        # Ensure graphics_path is defined correctly, assuming it's relative to the script or a fixed path
        graphics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "graphics")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(graphics_path, exist_ok=True) # Ensure graphics path also exists

        self.log(f"SVG Output Directory: {output_dir}")
        self.log(f"Graphics Path: {graphics_path}")

        # Simplified logging for now, can re-introduce detailed svg_log later if needed
        # svg_log_all_categories = []
        # total_svgs_generated_all_categories = 0

        for category_name, category_df in self.categorized_dfs.items():
            if category_df.empty:
                self.log(f"Skipping category '{category_name}': No orders.")
                continue

            processor_class = self.processor_map.get(category_name)

            if category_name == 'unclassified' or category_name == 'metal_products_raw':
                self.log(f"Skipping SVG generation for category '{category_name}' by rule.")
                continue

            if not processor_class:
                self.log(f"Warning: Skipping category '{category_name}': No processor mapped in self.processor_map.")
                continue

            self.log(f"Processing category '{category_name}' with {processor_class.__name__}...")
            try:
                processor_instance = None
                # Handle processors that might need a template path differently
                if category_name in ["small_stakes_graphic_coloured", "small_stakes_graphic_bw"]:
                    template_name = "small_colour.svg" if category_name == "small_stakes_graphic_coloured" else "small_bw.svg"
                    template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "002_svg_templates", template_name)
                    if not os.path.exists(template_file_path):
                        self.log(f"Error: Template file not found for {category_name}: {template_file_path}")
                        continue
                    processor_instance = processor_class(template_file_path, output_dir, graphics_path)
                else:
                    processor_instance = processor_class(graphics_path, output_dir)

                # Ensure a fresh copy of the DataFrame is passed to the processor
                # Also, ensure all column names are lowercase as processors might expect that
                df_copy = category_df.copy()
                df_copy.columns = [col.lower() for col in df_copy.columns]

                # Some processors might expect specific column names like 'Order ID' instead of 'order-id'
                # This renaming should be standardized or handled by processors.
                # For now, assume processors handle lowercase column names from the DataFrame.

                processor_instance.process_orders(df_copy)
                self.log(f"Completed SVG generation for category '{category_name}'. SVGs should be in {output_dir}.")

            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                self.log(f"Error processing category '{category_name}' with {processor_class.__name__}:\n{tb}")

        self.log("Finished processing all SVG categories.")
        self.list_output_files(output_dir)
        self.refresh_svg_thumbnails()

    def save_state(self):
        try:
            with open("app_state.pkl", "wb") as f: # Changed filename for clarity
                pickle.dump(self.categorized_dfs, f)
            self.log("Saved application state (categorized DataFrames).")
        except Exception as e:
            self.log(f"Error saving state: {e}")

    def load_state(self):
        import os
        import pandas as pd # Ensure pandas is imported for pd.isna
        state_file = "app_state.pkl"
        try:
            if os.path.exists(state_file):
                with open(state_file, "rb") as f:
                    loaded_categorized_dfs = pickle.load(f)

                if not isinstance(loaded_categorized_dfs, dict):
                    self.log(f"Error loading state: Expected a dictionary, got {type(loaded_categorized_dfs)}. Initializing empty state.")
                    self.categorized_dfs = {}
                else:
                    self.categorized_dfs = loaded_categorized_dfs
                    self.log(f"Loaded application state. Found {len(self.categorized_dfs)} categories.")

                self.tabs.clear() # Clear existing tabs before loading new ones

                if not self.categorized_dfs:
                    self.active_category_df = None
                    # Consider disabling buttons here if no data loaded
                    return

                def prefix_small(val):
                    if pd.isna(val) or str(val).strip() == '':
                        return val
                    s = str(val)
                    return s if s.lower().startswith('small ') else 'Small ' + s

                for category_name, category_df in self.categorized_dfs.items():
                    if not isinstance(category_df, pd.DataFrame):
                        self.log(f"Warning: Category '{category_name}' does not contain a DataFrame. Skipping.")
                        continue

                    # Apply 'prefix_small' logic to 'graphic' column if conditions met
                    if 'type' in category_df.columns and 'graphic' in category_df.columns:
                        mask = category_df['type'].astype(str).str.lower().isin(['small stake', 'small metal'])
                        category_df.loc[mask, 'graphic'] = category_df.loc[mask, 'graphic'].apply(prefix_small)

                    tab_content_widget = QWidget()
                    tab_layout = QVBoxLayout(tab_content_widget)
                    table_widget = QTableWidget()
                    table_widget.setProperty("category_name", category_name)

                    table_widget.setAlternatingRowColors(True)
                    table_widget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
                    table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
                    table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
                    table_widget.verticalHeader().setVisible(False)
                    table_widget.horizontalHeader().setStretchLastSection(True)

                    table_widget.itemSelectionChanged.connect(self.update_preview_pane)
                    table_widget.itemChanged.connect(self.on_table_cell_changed)

                    self._render_table(category_df, table_widget)
                    tab_layout.addWidget(table_widget)
                    self.tabs.addTab(tab_content_widget, category_name)

                if self.tabs.count() > 0:
                    self.tabs.setCurrentIndex(0) # Triggers on_tab_changed
                    self.on_tab_changed(0) # Explicit call to ensure active_df and buttons are set.
                else:
                    self.active_category_df = None
                    # Disable buttons if no tabs loaded
                    self.copy_button.setEnabled(False)
                    self.export_csv_button.setEnabled(False)
                    # ... etc for other buttons

            else:
                self.log("No saved state file found. Starting with a fresh session.")
                self.categorized_dfs = {} # Ensure it's initialized
        except Exception as e:
            import traceback
            self.log(f"Error loading state: {e}\n{traceback.format_exc()}")
            self.categorized_dfs = {} # Reset to a known empty state on error
            self.tabs.clear() # Clear tabs on error too
            self.active_category_df = None

    def closeEvent(self, event):
        self.save_state()
        event.accept()

    def refresh_svg_thumbnails(self):
        import os
        from PyQt5.QtSvg import QSvgWidget
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtCore import QSize
        # Clear previous thumbnails
        for i in reversed(range(self.svg_thumbnails_layout.count())):
            widget = self.svg_thumbnails_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Find SVG files
        app_dir = os.path.dirname(os.path.abspath(__file__))
        svg_dir = os.path.join(app_dir, "SVG_OUTPUT")
        if not os.path.isdir(svg_dir):
            label = QLabel('No SVG_OUTPUT folder found.')
            label.setAlignment(Qt.AlignCenter)
            self.svg_thumbnails_layout.addWidget(label)
            self.svg_thumbnails_container.adjustSize()
            return
        svg_files = [f for f in os.listdir(svg_dir) if f.lower().endswith('.svg')]
        svg_files = sorted(svg_files, key=lambda f: os.path.getmtime(os.path.join(svg_dir, f)), reverse=True)
        for svg_file in svg_files:
            svg_path = os.path.join(svg_dir, svg_file)
            thumb_widget = QWidget()
            thumb_layout = QVBoxLayout(thumb_widget)
            thumb_layout.setContentsMargins(4, 4, 4, 4)
            thumb_layout.setSpacing(2)
            try:
                svg = QSvgWidget(svg_path)
                svg.setFixedSize(192, 192)  # 100% larger
                svg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                # Add black bounding box
                svg.setStyleSheet('border: 2.5px solid black; background: #fff;')
                # Make SVG clickable
                def make_mouse_press_event(path):
                    return lambda event, p=path: self.open_svg_file(p)
                svg.mousePressEvent = make_mouse_press_event(svg_path)
                thumb_layout.addWidget(svg, alignment=Qt.AlignCenter)
            except Exception:
                fallback = QLabel(svg_file)
                fallback.setFixedSize(192, 192)
                fallback.setAlignment(Qt.AlignCenter)
                fallback.setStyleSheet('border:2.5px solid black; background:#eee;')
                fallback.mousePressEvent = lambda e, path=svg_path: self.open_svg_file(path)
                thumb_layout.addWidget(fallback)
            label = QLabel(svg_file)
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            thumb_layout.addWidget(label)
            self.svg_thumbnails_layout.addWidget(thumb_widget)
        self.svg_thumbnails_container.adjustSize()

    def open_svg_file(self, svg_path):
        import subprocess
        if os.path.exists(svg_path):
            subprocess.Popen(['start', '', svg_path], shell=True)
        else:
            self.log(f'SVG file not found: {svg_path}')

    def open_output_file_table(self, item):
        # Open the file on double click in the file output table
        import subprocess
        file_path = item.data(Qt.UserRole)
        if file_path and os.path.exists(file_path):
            subprocess.Popen(['start', '', file_path], shell=True)
        else:
            self.log(f'File not found: {file_path}')

    def __init__(self):
        super().__init__()
        self.filtered_df = None  # Always initialize filtered_df

        super().__init__()
        self.setWindowTitle('AmazonSeller Order Processor')
        # --- Menu Bar ---
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        save_action = QAction('Save State', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_state)
        file_menu.addAction(save_action)

        # --- Edit Menu ---
        edit_menu = menubar.addMenu('Edit')
        copy_action = QAction('Copy Table to Clipboard', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy_table_to_clipboard)
        edit_menu.addAction(copy_action)

        add_row_action = QAction('Add Row', self)
        add_row_action.setShortcut('Insert')
        add_row_action.triggered.connect(self.add_row)
        edit_menu.addAction(add_row_action)

        delete_row_action = QAction('Delete Row', self)
        delete_row_action.setShortcut('Delete')
        delete_row_action.triggered.connect(self.delete_row)
        edit_menu.addAction(delete_row_action)

        create_design_action = QAction('Create Design for Selected', self)
        create_design_action.setShortcut('Ctrl+D')
        create_design_action.triggered.connect(self.create_design_for_selected)
        edit_menu.addAction(create_design_action)

        self.last_df = None # This will be replaced by categorized_dfs
        self.categorized_dfs = {}
        self.active_category_df = None
        self.setMinimumSize(600, 400)

        self.processor_map = {
            "regular_stakes_graphic_coloured": RegularStakesProcessor,
            "regular_stakes_graphic_bw": BWStakesProcessor,
            "regular_stakes_photo_coloured": PhotoStakesProcessor,
            "regular_stakes_photo_bw": BWPhotoStakesProcessor,
            "large_stakes_graphic_coloured": ColouredLargeStakesProcessor,
            "large_stakes_graphic_bw": BWLargeStakesProcessor,
            "large_stakes_photo_coloured": ColouredLargePhotoStakesProcessor,
            # "large_stakes_photo_bw": BWPhotoStakesProcessor, # Removed as BWPhotoStakesProcessor is for regular stakes. No specific processor for large B&W photo.
            "small_stakes_graphic_coloured": ColouredSmallStakesTemplateProcessor,
            "small_stakes_graphic_bw": BlackAndWhiteSmallStakesTemplateProcessor,
            # "heart_stakes_graphic": None, # Explicitly unmapped as no processor exists. Or simply omit the key.
            # 'unclassified' and 'metal_products_raw' will be skipped by default in create_all_svgs
        }

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_vlayout = QVBoxLayout(central_widget)

        # --- Left pane: DropZone and Process Orders button ---
        left_widget_top = QWidget()
        left_layout = QVBoxLayout(left_widget_top)
        left_layout.setContentsMargins(4, 4, 4, 4)
        left_layout.setSpacing(8)
        self.drop_zone = DropZone(self)
        self.drop_zone.setFont(QFont('Arial', 10))
        self.drop_zone.setStyleSheet('border: 2px dashed #aaa; padding: 18px; background: #fafafa;')
        self.drop_zone.setFixedWidth(270)
        left_layout.addWidget(self.drop_zone)
        self.drop_zone.file_dropped.connect(self.on_file_dropped)
        self.process_button = QPushButton('Process')
        self.process_button.setFixedWidth(120)
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_orders)
        left_layout.addWidget(self.process_button)
        # Add Create SVGs button (combined)
        self.create_svgs_button = QPushButton('Create SVGs')
        self.create_svgs_button.setFixedWidth(120)
        self.create_svgs_button.setEnabled(True)
        self.create_svgs_button.clicked.connect(self.create_all_svgs)
        left_layout.addWidget(self.create_svgs_button)
        # --- Move main action buttons to left pane only ---
        self.copy_button = QPushButton('Copy Table to Clipboard')
        self.copy_button.setEnabled(False)
        self.copy_button.setFixedWidth(120)
        self.copy_button.clicked.connect(self.copy_table_to_clipboard)
        left_layout.addWidget(self.copy_button)

        self.add_row_button = QPushButton('Add Row')
        self.add_row_button.setFixedWidth(120)
        self.add_row_button.clicked.connect(self.add_row)
        left_layout.addWidget(self.add_row_button)

        self.delete_row_button = QPushButton('Delete Row')
        self.delete_row_button.setFixedWidth(120)
        self.delete_row_button.clicked.connect(self.delete_row)
        left_layout.addWidget(self.delete_row_button)

        self.create_design_button = QPushButton('Create Design for Selected')
        self.create_design_button.setFixedWidth(120)
        self.create_design_button.setEnabled(True)
        self.create_design_button.clicked.connect(self.create_design_for_selected)
        left_layout.addWidget(self.create_design_button)

        left_layout.addStretch(1)
        # Terminal/log output at bottom of left pane (in splitter)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(100)
        # Splitter for left pane (controls on top, terminal at bottom)
        left_splitter = QSplitter(Qt.Vertical)
        left_splitter.addWidget(left_widget_top)
        left_splitter.addWidget(self.log_output)
        left_splitter.setSizes([400, 150])

        # --- Center pane: Table and controls ---
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(6)

        # --- New control bar ---
        control_bar = QHBoxLayout()
        self.clear_button = QPushButton('Clear Table')
        self.clear_button.clicked.connect(self.clear_table)
        control_bar.addWidget(self.clear_button)
        self.export_csv_button = QPushButton('Export as CSV')
        self.export_csv_button.clicked.connect(self.export_table_csv)
        control_bar.addWidget(self.export_csv_button)
        self.export_txt_button = QPushButton('Export as TXT')
        self.export_txt_button.clicked.connect(self.export_table_txt)
        control_bar.addWidget(self.export_txt_button)
        self.open_output_button = QPushButton('Open Output Folder')
        self.open_output_button.clicked.connect(self.open_output_folder)
        control_bar.addWidget(self.open_output_button)
        self.warnings_only_checkbox = QCheckBox('Show Only Warnings')
        self.warnings_only_checkbox.stateChanged.connect(self.filter_table)
        control_bar.addWidget(self.warnings_only_checkbox)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Search orders...')
        self.search_box.textChanged.connect(self.filter_table)
        control_bar.addWidget(self.search_box)
        center_layout.addLayout(control_bar)

        # Tab widget for categorized tables (center)
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        center_layout.addWidget(self.tabs)

        # --- Right pane: Output SVG/CSV file list ---
        preview_widget_top = QWidget()
        preview_layout = QVBoxLayout(preview_widget_top)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(4)
        self.file_output_title = QLabel('File Output')
        self.file_output_title.setAlignment(Qt.AlignCenter)
        self.file_output_title.setStyleSheet('font-weight: bold; font-size: 16px; padding: 8px 0;')
        self.file_output_table = QTableWidget()
        self.file_output_table.setColumnCount(2)
        self.file_output_table.setHorizontalHeaderLabels(['SVGs', 'CSVs'])
        self.file_output_table.setAlternatingRowColors(True)
        self.file_output_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_output_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_output_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.file_output_table.verticalHeader().setVisible(False)
        self.file_output_table.horizontalHeader().setStretchLastSection(True)
        self.file_output_table.setStyleSheet('font-size: 15px; font-family: Arial;')
        self.file_output_table.itemDoubleClicked.connect(self.open_output_file_table)
        preview_layout.addWidget(self.file_output_title)
        preview_layout.addWidget(self.file_output_table)
        # SVG Preview Pane (with clickable thumbnails)

        self.svg_preview_area = QScrollArea()
        self.svg_preview_area.setWidgetResizable(True)
        self.svg_thumbnails_title = QLabel('SVG Previews')
        self.svg_thumbnails_title.setAlignment(Qt.AlignCenter)
        self.svg_thumbnails_title.setStyleSheet('font-weight: bold; font-size: 16px; padding: 8px 0;')
        self.svg_thumbnails_container = QWidget()
        self.svg_thumbnails_layout = QVBoxLayout(self.svg_thumbnails_container)
        self.svg_thumbnails_layout.setContentsMargins(0, 0, 0, 0)
        self.svg_thumbnails_layout.setSpacing(2)
        self.svg_thumbnails_scroll = QScrollArea()
        self.svg_thumbnails_scroll.setWidgetResizable(True)
        self.svg_thumbnails_scroll.setWidget(self.svg_thumbnails_container)
        preview_layout.addWidget(self.svg_thumbnails_title)
        preview_layout.addWidget(self.svg_thumbnails_scroll, stretch=1)
        # Splitter for right pane (links on top, SVG preview at bottom)
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(preview_widget_top)
        right_splitter.addWidget(self.svg_preview_area)
        right_splitter.setSizes([200, 200])
        self.refresh_svg_thumbnails()


        # --- Main horizontal splitter: left (controls+terminal), center (table), right (links+svg preview) ---
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Horizontal)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(center_widget)
        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([240, 600, 400])
        main_vlayout.addWidget(main_splitter, stretch=1)

        self.log_output.setFont(QFont('Consolas', 10))
        main_vlayout.addWidget(self.log_output)

        self.selected_files = None
        # self.last_df = None # Replaced by categorized_dfs
        # Restore last state after all widgets are initialized
        self.load_state()

    def on_tab_changed(self, index):
        if index >= 0 and self.tabs.widget(index): # Check if widget exists
            current_tab_content_widget = self.tabs.widget(index)
            current_tab_table = current_tab_content_widget.findChild(QTableWidget)
            if current_tab_table and hasattr(current_tab_table, 'property') and current_tab_table.property('category_name'):
                category_name = current_tab_table.property('category_name')
                if self.categorized_dfs and category_name in self.categorized_dfs:
                    self.active_category_df = self.categorized_dfs[category_name]
                    self.log(f"Switched to tab: {category_name}. Active DataFrame contains {len(self.active_category_df)} rows.")
                    # Potentially call filter_table here if filters are per tab
                    self.filter_table() # Assuming filter_table will use active_category_df
                else:
                    self.active_category_df = None
                    self.log(f"Switched to tab: {category_name}, but no corresponding DataFrame found in categorized_dfs.")
            else:
                self.active_category_df = None
                self.log(f"Switched to tab index {index}, but table or category_name property not found.")
        else:
            self.active_category_df = None
            self.log(f"Switched to an invalid tab index: {index} or tab has no widget.")

        # Enable/disable buttons based on active tab
        self.copy_button.setEnabled(self.active_category_df is not None and not self.active_category_df.empty)
        self.export_csv_button.setEnabled(self.active_category_df is not None and not self.active_category_df.empty)
        self.export_txt_button.setEnabled(self.active_category_df is not None and not self.active_category_df.empty)
        self.add_row_button.setEnabled(self.active_category_df is not None) # Can add row to empty df
        self.delete_row_button.setEnabled(self.active_category_df is not None and not self.active_category_df.empty)
        self.create_design_button.setEnabled(self.active_category_df is not None and not self.active_category_df.empty)


    def on_file_dropped(self, file_path):
        # Support multiple files (comma-separated or list)
        if isinstance(file_path, list):
            self.selected_files = file_path
        elif isinstance(file_path, str) and ',' in file_path:
            self.selected_files = [f.strip() for f in file_path.split(',')]
        else:
            self.selected_files = [file_path]
        self.process_button.setEnabled(True)
        self.log(f'Files dropped: {self.selected_files}')

    def process_orders(self):
        if not hasattr(self, 'selected_files') or not self.selected_files:
            self.log('No files selected!')
            return
        self.log(f'Processing files: {self.selected_files}')
        try:
            import os
            import sys
            pipeline_dir = os.path.join(os.path.dirname(__file__), "001 AMAZON DATA DOWNLOAD")
            if pipeline_dir not in sys.path:
                sys.path.insert(0, pipeline_dir)
            import order_pipeline
            # Use the application directory for outputs (portable)
            app_dir = os.path.dirname(os.path.abspath(__file__))
            images_dir = os.path.join(app_dir, "images")
            output_dir = os.path.join(app_dir, "SVG_OUTPUT")
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)
            self.log(f'Processing Amazon order files ({len(self.selected_files)}), downloading images, parsing XML...')
            # Always use SKULIST.csv from the current project root
            skulist_path = os.path.join(app_dir, "assets", "SKULIST.csv")
            # process_amazon_orders now returns a dictionary of DataFrames
            categorized_dfs_from_pipeline = order_pipeline.process_amazon_orders(
                self.selected_files, images_dir, output_dir, skulist_path=skulist_path, status_callback=self.log
            )
            self.categorized_dfs = categorized_dfs_from_pipeline
            self.tabs.clear() # Clear previous tabs

            if not self.categorized_dfs:
                self.log("No data returned from order processing or no categories found.")
                self.active_category_df = None
                # Disable buttons if no data
                self.copy_button.setEnabled(False)
                self.export_csv_button.setEnabled(False)
                self.export_txt_button.setEnabled(False)
                self.add_row_button.setEnabled(False)
                self.delete_row_button.setEnabled(False)
                self.create_design_button.setEnabled(False)
                return

            for category_name, category_df in self.categorized_dfs.items():
                tab_content_widget = QWidget()
                tab_layout = QVBoxLayout(tab_content_widget)
                table_widget = QTableWidget()
                table_widget.setProperty("category_name", category_name) # Store category name

                # Common table settings from original self.table setup
                table_widget.setAlternatingRowColors(True)
                table_widget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
                table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
                table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
                table_widget.verticalHeader().setVisible(False)
                table_widget.horizontalHeader().setStretchLastSection(True)

                # Connect signals for this specific table
                table_widget.itemSelectionChanged.connect(self.update_preview_pane)
                table_widget.itemChanged.connect(self.on_table_cell_changed)

                self._render_table(category_df, table_widget) # Pass df and the new table_widget
                tab_layout.addWidget(table_widget)
                self.tabs.addTab(tab_content_widget, category_name)

            self.log(f'Order processing complete. {sum(len(df) for df in self.categorized_dfs.values())} orders processed into {len(self.categorized_dfs)} categories.')

            # Set active_category_df for the first tab (if any)
            if self.tabs.count() > 0:
                self.tabs.setCurrentIndex(0) # This will trigger on_tab_changed
                # self.on_tab_changed(0) # Call explicitly if setCurrentIndex doesn't trigger it reliably enough for button states
            else: # No tabs created
                self.active_category_df = None
                self.copy_button.setEnabled(False)
                self.export_csv_button.setEnabled(False)
                self.export_txt_button.setEnabled(False)
                self.add_row_button.setEnabled(False)
                self.delete_row_button.setEnabled(False)
                self.create_design_button.setEnabled(False)

            # Log SKUs in specific categories that might need attention
            unhandled_sku_messages = []
            categories_to_report = ["unclassified", "large_stakes_photo_bw", "heart_stakes_graphic"]
            for category_name_to_check in categories_to_report:
                if category_name_to_check in self.categorized_dfs and not self.categorized_dfs[category_name_to_check].empty:
                    num_skus = len(self.categorized_dfs[category_name_to_check])
                    # Sanitize category_name for filename
                    safe_category_filename = category_name_to_check.replace(' ', '_').lower()
                    message = (f"- Category '{category_name_to_check}': Contains {num_skus} order(s). "
                               f"These may not have a dedicated SVG processor or are unclassified. "
                               f"Please review 'output_category_{safe_category_filename}.csv'.")
                    unhandled_sku_messages.append(message)

            if unhandled_sku_messages:
                full_log_message = "Attention: Some SKUs require review:\n" + "\n".join(unhandled_sku_messages)
                self.log(full_log_message)

        except Exception as e:
            import traceback
            self.log(f"Error in process_orders: {e}\n{traceback.format_exc()}")
            # Ensure buttons are disabled on error
            self.copy_button.setEnabled(False)
            self.export_csv_button.setEnabled(False)
            self.export_txt_button.setEnabled(False)
            self.add_row_button.setEnabled(False)
            self.delete_row_button.setEnabled(False)
            self.create_design_button.setEnabled(False)
            # Old error handling, column reordering, and sorting logic that was here
            # has been removed as it acted on a single 'df'. If this logic is
            # still needed, it would have to be adapted to work with categorized_dfs,
            # possibly by applying it to each DataFrame within the dictionary.
            # For now, focusing on getting tabs to work.

    def _render_table(self, df, table_widget): # Added table_widget argument
        # SVG Processor column is no longer needed as categorization handles this.
        # df = df.copy() # df passed in should be ready or copied by caller if needed

        # Ensure correct graphic for OM008021 (This logic might need to be category specific or global)
        # For now, applying it to any df passed.
        if 'sku' in df.columns and 'graphic' in df.columns: # Operate on df directly before copy
            mask = df['sku'].astype(str).str.upper() == 'OM008021'
            df.loc[mask, 'graphic'] = 'OM008021.png'

        import os
        import pandas as pd
        from PyQt5.QtCore import Qt

        current_df = df.copy() # Work on a copy for rendering specific modifications

        # Always show only the image filename in the table
        if 'image_path' in current_df.columns:
            current_df['image_path'] = current_df['image_path'].apply(lambda p: os.path.basename(str(p)) if pd.notna(p) else p)

        # --- Fix order-id persistence: (Commented out, needs original_df context)
        # if hasattr(self, 'original_df') and 'order-id' in current_df.columns and 'order-id' in self.original_df.columns:
        #     mask_blank = current_df['order-id'].isnull() | (current_df['order-id'].astype(str).str.strip() == '')
        #     current_df.loc[mask_blank, 'order-id'] = self.original_df.loc[mask_blank, 'order-id']

        # --- Patch: for sku == 'M0634S - CAT - RAINBOW BRIDGE', set graphic ---
        if 'sku' in current_df.columns and 'graphic' in current_df.columns:
            mask = current_df['sku'].astype(str).str.strip().str.upper() == 'M0634S - CAT - RAINBOW BRIDGE'
            current_df.loc[mask, 'graphic'] = 'Small Rainbow Bridge.png'

        # Ensure 'No.' is always the first column and always sequential 1-based numbers
        if 'No.' not in current_df.columns:
            current_df.insert(0, 'No.', range(1, len(current_df) + 1))
        else:
            current_df['No.'] = range(1, len(current_df) + 1)
            cols = list(current_df.columns)
            if cols[0] != 'No.':
                cols.remove('No.')
                cols.insert(0, 'No.')
                current_df = current_df[cols]

        # Ensure 'Tick' is always the second column
        if 'Tick' not in current_df.columns:
            current_df.insert(1, 'Tick', ['' for _ in range(len(current_df))])
        else:
            cols = list(current_df.columns)
            if cols[1] != 'Tick':
                cols.remove('Tick')
                cols.insert(1, 'Tick')
                current_df = current_df[cols]

        tick_col_index = 1 # 'Tick' is now at index 1

        # Find the index of the order-id column (case-insensitive) - not used later, can remove if confirmed
        # order_id_col = None
        # for i, col_name in enumerate(current_df.columns):
        #     if col_name.lower().replace('_', '').replace('-', '') == 'orderid':
        #         order_id_col = i
        #         break

        table_widget.setRowCount(len(current_df))
        table_widget.setColumnCount(len(current_df.columns))
        table_widget.setHorizontalHeaderLabels(current_df.columns)
        table_widget.blockSignals(True)  # Prevent itemChanged from firing during setup
        type_options = [
            "Small Metal", "Medium Metal", "Large Metal", "XL Metal",
            "Small Stake", "Regular Stake", "Large Stake", "Heart Stake", "" # Added empty for clearing
        ]
        colour_options = [
            "Aluminium", "Brass", "Black", "Slate", "Copper", "Gold", "Silver", "Stone", "Marble", "" # Added empty for clearing
        ]

        type_col_idx_render = None
        colour_col_idx_render = None
        sku_col_idx_render = None
        for idx, col_name in enumerate(current_df.columns):
            if col_name.strip().lower() == 'type': type_col_idx_render = idx
            if col_name.strip().lower() == 'colour': colour_col_idx_render = idx
            if col_name.strip().lower() == 'sku': sku_col_idx_render = idx

        skulist_type_map_render = {}
        try:
            import csv
            # Path to SKULIST.csv should be robust, e.g., relative to script or configurable
            csv_path_render = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'SKULIST.csv')
            with open(csv_path_render, newline='', encoding='utf-8-sig') as f_render:
                reader_render = csv.DictReader(f_render)
                if reader_render.fieldnames:
                    header_map_render = {k.strip().upper(): k for k in reader_render.fieldnames}
                    sku_key_render = header_map_render.get('SKU')
                    type_key_render = header_map_render.get('TYPE')
                    if sku_key_render and type_key_render:
                        for r_item in reader_render: # Changed loop var from row to r_item
                            sku_val = str(r_item.get(sku_key_render, '')).strip()
                            type_val = str(r_item.get(type_key_render, '')).strip()
                            if sku_val and type_val:
                                skulist_type_map_render[sku_val.upper()] = type_val
        except Exception as e:
            self.log(f"Could not load SKULIST.csv in _render_table for type prefill: {e}")

        for row_idx in range(len(current_df)): # Changed loop var from row to row_idx
            for col_idx in range(len(current_df.columns)): # Changed loop var from col to col_idx
                if col_idx == tick_col_index:
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    df_tick_val = str(current_df.iat[row_idx, col_idx]).strip().lower()
                    if df_tick_val == '1' or df_tick_val == 'true' or df_tick_val == 'checked':
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                    table_widget.setItem(row_idx, col_idx, item)
                elif type_col_idx_render is not None and col_idx == type_col_idx_render:
                    cell_value = str(current_df.iat[row_idx, col_idx])
                    if not cell_value or cell_value.lower() == 'nan':
                        if sku_col_idx_render is not None:
                            sku_for_lookup = str(current_df.iat[row_idx, sku_col_idx_render]).strip().upper()
                            if sku_for_lookup in skulist_type_map_render:
                                cell_value = skulist_type_map_render[sku_for_lookup]

                    item = QTableWidgetItem(cell_value)
                    # Make type column editable as a standard QTableWidgetItem for now
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    table_widget.setItem(row_idx, col_idx, item)
                elif colour_col_idx_render is not None and col_idx == colour_col_idx_render:
                    from PyQt5.QtWidgets import QComboBox
                    combo = QComboBox()
                    combo.addItems(colour_options) # Use predefined colour_options
                    cell_value = str(current_df.iat[row_idx, col_idx])
                    if cell_value in colour_options:
                        combo.setCurrentText(cell_value)
                    elif cell_value: # If value exists and not in standard options
                        combo.addItem(cell_value) # Add it to this instance's list
                        combo.setCurrentText(cell_value) # And select it
                    else: # If empty or None
                        combo.setCurrentIndex(combo.findText("")) # Select empty string if available, else -1

                    # This handler updates the QTableWidgetItem when QComboBox changes,
                    # which then allows on_table_cell_changed to pick it up.
                    def create_combo_handler_local(r, c, current_combo_box):
                        def on_combo_changed_local(new_text):
                            table_widget.blockSignals(True)
                            # Ensure an item exists to set its text, which then triggers itemChanged
                            # This is crucial because cellWidget does not inherently do this.
                            table_item = table_widget.item(r, c)
                            if not table_item: # If no item, create one
                                table_item = QTableWidgetItem()
                                table_widget.setItem(r, c, table_item)
                            table_item.setText(new_text) # Set text of the item
                            table_widget.blockSignals(False)
                            # Manually trigger on_table_cell_changed if needed, but setText should do it if signals are unblocked.
                            # self.on_table_cell_changed(table_item)
                        return on_combo_changed_local

                    combo.currentTextChanged.connect(create_combo_handler_local(row_idx, col_idx, combo))
                    table_widget.setCellWidget(row_idx, col_idx, combo)
                else:
                    item_text = str(current_df.iat[row_idx, col_idx])
                    item = QTableWidgetItem(item_text)
                    if col_idx != 0 : # Assuming 'No.' is always at col_idx 0 and non-editable
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
                    table_widget.setItem(row_idx, col_idx, item)

        table_widget.blockSignals(False) # Restore signals for the specific table_widget
        table_widget.resizeColumnsToContents()
        # Edit triggers and itemChanged connection are handled in process_orders for each table_widget

    def clear_table(self):
        self.tabs.clear() # Clear all tabs
        self.categorized_dfs = {} # Clear the data
        self.active_category_df = None # Reset active df
        # self.last_df = None # Old single df, already removed from some places
        self.filtered_df = None # This will become active_filtered_df or similar
        self.log('All tabs and data cleared.')
        # Update button states
        self.copy_button.setEnabled(False)
        self.export_csv_button.setEnabled(False)
        self.export_txt_button.setEnabled(False)
        self.add_row_button.setEnabled(False)
        self.delete_row_button.setEnabled(False)
        self.create_design_button.setEnabled(False)

    def export_table_csv(self):
        # This should export the active, possibly filtered, tab's data
        if self.active_category_df is None:
            self.log('No active table to export.')
            return

        # Use self.active_filtered_df if it exists and filter_table maintains it,
        # otherwise, use self.active_category_df.
        df_to_export = self.active_category_df
        if hasattr(self, 'active_filtered_df') and self.active_filtered_df is not None:
            df_to_export = self.active_filtered_df

        if df_to_export is not None and not df_to_export.empty:
            category_name = "unknown_category"
            current_tab_widget_for_name = self.tabs.currentWidget()
            if current_tab_widget_for_name:
                current_table_for_name = current_tab_widget_for_name.findChild(QTableWidget)
                if current_table_for_name and current_table_for_name.property("category_name"):
                    category_name = current_table_for_name.property("category_name")

            suggested_filename = f"{category_name}_export.csv"
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as CSV', suggested_filename, 'CSV Files (*.csv)')
            if path:
                df_to_export.to_csv(path, index=False, encoding='utf-8-sig')
                self.log(f'Table for category "{category_name}" exported as CSV: {path}')
        else:
            self.log('No data in active table to export.')

    def export_table_txt(self):
        if self.active_category_df is None:
            self.log('No active table to export.')
            return

        df_to_export = self.active_category_df
        if hasattr(self, 'active_filtered_df') and self.active_filtered_df is not None:
            df_to_export = self.active_filtered_df

        if df_to_export is not None and not df_to_export.empty:
            category_name = "unknown_category"
            current_tab_widget_for_name = self.tabs.currentWidget()
            if current_tab_widget_for_name:
                current_table_for_name = current_tab_widget_for_name.findChild(QTableWidget)
                if current_table_for_name and current_table_for_name.property("category_name"):
                    category_name = current_table_for_name.property("category_name")

            suggested_filename = f"{category_name}_export.txt"
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as TXT', suggested_filename, 'Text Files (*.txt)')
            if path:
                df_to_export.to_csv(path, sep='\t', index=False, encoding='utf-8')
                self.log(f'Table for category "{category_name}" exported as TXT: {path}')
        else:
            self.log('No data in active table to export.')

    def open_output_folder(self):
        # Always open SVG_OUTPUT relative to the application directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(app_dir, "SVG_OUTPUT")
        if os.path.exists(folder):
            import subprocess
            subprocess.Popen(['start', '', folder], shell=True)
            self.log(f'Opened output folder: {folder}')
            self.refresh_svg_thumbnails()
        else:
            self.log('Output folder does not exist.')


    def filter_table(self): # Needs to operate on active tab
        if self.active_category_df is None:
            self.log("No active table to filter.")
            # If there's an active QTableWidget, clear it if no active_category_df
            current_tab_widget = self.tabs.currentWidget()
            if current_tab_widget:
                active_table_to_clear = current_tab_widget.findChild(QTableWidget)
                if active_table_to_clear:
                    active_table_to_clear.setRowCount(0)
            return

        df_to_filter = self.active_category_df.copy()

        # Filter by warnings (ensure 'Warnings' column exists)
        if 'Warnings' in df_to_filter.columns and self.warnings_only_checkbox.isChecked():
            df_to_filter = df_to_filter[df_to_filter['Warnings'].astype(str).str.strip() != '']

        # Filter by search
        search_text = self.search_box.text().strip().lower()
        if search_text:
            # Apply search to all columns converted to string, case-insensitive
            df_to_filter = df_to_filter[df_to_filter.apply(lambda row: search_text in ' '.join(row.astype(str)).lower(), axis=1)]

        # Store the filtered DataFrame for the active tab, perhaps in a new instance variable
        self.active_filtered_df = df_to_filter

        current_tab_render_widget = self.tabs.currentWidget()
        if current_tab_render_widget:
            active_table_to_render = current_tab_render_widget.findChild(QTableWidget)
            if active_table_to_render:
                category_name = active_table_to_render.property("category_name")
                self._render_table(df_to_filter, active_table_to_render)
                self.log(f"Filtered '{category_name}' tab. Showing {len(df_to_filter)} rows.")
            else:
                self.log("Could not find QTableWidget in current tab to render filtered data.")
        else:
            self.log("No current tab selected to render filtered data.")

    def copy_table_to_clipboard(self): # Operates on active tab
        df_to_copy = None
        # Prefer to copy the filtered data if it exists
        if hasattr(self, 'active_filtered_df') and self.active_filtered_df is not None:
            df_to_copy = self.active_filtered_df
        elif self.active_category_df is not None: # Fallback to unfiltered active df
            df_to_copy = self.active_category_df

        current_tab_text = "Unknown Tab"
        if self.tabs.currentIndex() != -1:
            current_tab_text = self.tabs.tabText(self.tabs.currentIndex())

        if df_to_copy is not None and not df_to_copy.empty:
            # Exclude 'No.' and 'Tick' columns for a cleaner copy, if they exist
            cols_to_copy = [col for col in df_to_copy.columns if col.lower() not in ['no.', 'tick']]
            text_to_copy = df_to_copy[cols_to_copy].to_csv(sep='\t', index=False)
            QApplication.clipboard().setText(text_to_copy)
            self.log(f'Data from tab "{current_tab_text}" copied to clipboard!')
        else:
            self.log(f'No data in active table ("{current_tab_text}") to copy.')

    def update_preview_pane(self):
        # No-op: preview pane now lists output SVG/CSV files instead of per-row preview
        pass

    def open_output_file(self, url):
        import subprocess
        try:
            # url can be QUrl or str
            if hasattr(url, 'toLocalFile'):
                path = url.toLocalFile()
            elif isinstance(url, str):
                from PyQt5.QtCore import QUrl
                path = QUrl(url).toLocalFile()
            else:
                self.log(f'Unknown URL type: {url}')
                return
            if not path:
                self.log(f'Invalid file path from URL: {url}')
                return
            if os.path.exists(path):
                try:
                    subprocess.Popen(['start', '', path], shell=True)
                except Exception as e:
                    self.log(f'Failed to open file: {path}\nError: {e}')
            else:
                self.log(f'File not found: {path}')
            # Refresh the file list for the output directory
            output_dir = os.path.dirname(path)
            self.list_output_files(output_dir)
        except Exception as e:
            self.log(f'Error handling SVG/CSV link:\n{e}')


    def list_output_files(self, output_dir):
        # List SVGs and their CSVs in the file output table (top left)
        self._last_output_dir = output_dir  # Store for later use if needed
        try:
            svg_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.svg')]
            # Sort SVGs by last modified time, most recent first
            svg_files = sorted(svg_files, key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
            self.file_output_table.setRowCount(0)
            for svg in svg_files:
                svg_path = os.path.abspath(os.path.join(output_dir, svg))
                csv_path = os.path.splitext(svg_path)[0] + '.csv'
                row = self.file_output_table.rowCount()
                self.file_output_table.insertRow(row)
                svg_item = QTableWidgetItem(os.path.basename(svg_path))
                svg_item.setData(Qt.UserRole, svg_path)
                svg_item.setFont(QFont('Arial', 15))
                self.file_output_table.setItem(row, 0, svg_item)
                if os.path.exists(csv_path):
                    csv_item = QTableWidgetItem(os.path.basename(csv_path))
                    csv_item.setData(Qt.UserRole, csv_path)
                    csv_item.setFont(QFont('Arial', 15))
                    self.file_output_table.setItem(row, 1, csv_item)
                else:
                    self.file_output_table.setItem(row, 1, QTableWidgetItem(''))
        except Exception as e:
            self.log(f'Error listing output files: {e}')



def filter_table(self):
    if self.last_df is None:
        return
    df = self.last_df.copy()
    # Filter by warnings
    if self.warnings_only_checkbox.isChecked():
        df = df[df['Warnings'].astype(str).str.strip() != '']
    # Filter by search
    search = self.search_box.text().strip().lower()
    if search:
        df = df[df.apply(lambda row: search in ' '.join(map(str, row.values)).lower(), axis=1)]
    self.filtered_df = df
    self._render_table(df)

def copy_table_to_clipboard(self):
    if self.filtered_df is not None and not self.filtered_df.empty:
        text = self.filtered_df.to_csv(sep='\t', index=False)
        QApplication.clipboard().setText(text)
        self.log('Order data copied to clipboard! Paste into Google Sheets (Ctrl+V).')
    else:
        self.log('No data to copy.')

def update_preview_pane(self):
    # No-op: preview pane now lists output SVG/CSV files instead of per-row preview
    pass

def open_output_file(self, url):
    import subprocess
    path = url.toLocalFile()
    if os.path.exists(path):
        subprocess.Popen(['start', '', path], shell=True)
    else:
        self.log(f'File not found: {path}')
    processor.process_orders(df)
    self.log('B&W Large Stakes SVG generation complete!')
    try:
        # --- Coloured Large Photo Stakes SVGs ---
        self.log(f'Generating Coloured Large Photo Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
        processor = ColouredLargePhotoStakesProcessor(graphics_path, output_dir)
        processor.process_orders(df)
        self.log('Coloured Large Photo Stakes SVG generation complete!')
        # --- B&W Photo Stakes SVGs ---
        self.log('=== ENTERING B&W PHOTO STAKES BLOCK ===')
        self.log(f'Generating B&W Photo Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
        # Log DataFrame columns and first 5 rows before processing
        self.log(f"[BWPhotoStakes] DataFrame columns: {list(df.columns)}")
        self.log(f"[BWPhotoStakes] First 5 rows:\n{df.head().to_string()}")
        processor = BWPhotoStakesProcessor(graphics_path, output_dir)
        processor.process_orders(df)
        # Count SVGs generated for BW_PHOTO
        bw_svg_count = len([f for f in os.listdir(output_dir) if f.startswith('BW_PHOTO') and f.lower().endswith('.svg')])
        self.log(f"B&W Photo Stakes SVG generation complete! SVGs generated: {bw_svg_count}")
        # Update right pane with SVG/CSV hyperlinks
        self.list_output_files(output_dir)
        self.log('All SVG file links updated.')
        self.refresh_svg_thumbnails()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        self.log(f'Error during SVG generation:\n{tb}')


def create_all_svgs(self):
    """Generate all SVGs for different stake types and handle errors/logging."""
    if not hasattr(self, 'last_df') or self.last_df is None or self.last_df.empty:
        self.log('No processed orders available for SVG generation.')
        return
    def create_all_svgs(self):
        """Generate all SVGs for different stake types and handle errors/logging."""
        if not hasattr(self, 'last_df') or self.last_df is None or self.last_df.empty:
            self.log('No processed orders available for SVG generation.')
            return
        try:
            import os
            df = self.last_df.copy()
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SVG_OUTPUT")
            graphics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "graphics")
            os.makedirs(output_dir, exist_ok=True)
            # --- Regular SVGs ---
            self.log(f'Generating Regular SVGs in {output_dir} using graphics from {graphics_path}...')
            processor = RegularStakesProcessor(graphics_path, output_dir)
            processor.process_orders(df)
            self.log('Regular SVG generation complete!')
            # --- B&W SVGs ---
            self.log(f'Generating B&W SVGs in {output_dir} using graphics from {graphics_path}...')
            processor = BWStakesProcessor(graphics_path, output_dir)
            processor.process_orders(df)
            self.log('B&W SVG generation complete!')
            # --- Photo SVGs ---
            self.log(f'Generating Photo SVGs in {output_dir} using graphics from {graphics_path}...')
            processor = PhotoStakesProcessor(graphics_path, output_dir)
            processor.process_orders(df)
            self.log('Photo SVG generation complete!')
            # --- B&W Large Stakes SVGs ---
            self.log(f'Generating B&W Large Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
            processor = BWLargeStakesProcessor(graphics_path, output_dir)
            processor.process_orders(df)
            self.log('B&W Large Stakes SVG generation complete!')
            # --- Coloured Large Stakes SVGs ---
            self.log(f'Generating Coloured Large Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
            df_coloured_large = df[
                (df['type'].str.strip().str.lower() == 'large stake') &
                (df['colour'].str.strip().str.lower().isin(['copper', 'gold', 'silver', 'stone', 'marble'])) &
                (df['decorationtype'].str.strip().str.lower() == 'graphic')
            ].copy()
            if not df_coloured_large.empty:
                # Convert columns to uppercase to match processor expectations
                df_coloured_large.columns = [c.upper() for c in df_coloured_large.columns]
                processor = ColouredLargeStakesProcessor(graphics_path, output_dir)
                processor.process_orders(df_coloured_large)
                self.log(f'Coloured Large Stakes SVG generation complete! SVGs generated: {len(df_coloured_large)}')
            else:
                self.log('No Coloured Large Stakes orders found for SVG generation.')
            # --- Coloured Large Photo Stakes SVGs ---
            self.log(f'Generating Coloured Large Photo Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
            processor = ColouredLargePhotoStakesProcessor(graphics_path, output_dir)
            processor.process_orders(df)
            self.log('Coloured Large Photo Stakes SVG generation complete!')
            # --- B&W Photo Stakes SVGs ---
            self.log('=== ENTERING B&W PHOTO STAKES BLOCK ===')
            self.log(f'Generating B&W Photo Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
            self.log(f"[BWPhotoStakes] DataFrame columns: {list(df.columns)}")
            self.log(f"[BWPhotoStakes] First 5 rows:\n{df.head().to_string()}")
            processor = BWPhotoStakesProcessor(graphics_path, output_dir)
            processor.process_orders(df)
            bw_svg_count = len([f for f in os.listdir(output_dir) if f.startswith('BW_PHOTO') and f.lower().endswith('.svg')])
            self.log(f"B&W Photo Stakes SVG generation complete! SVGs generated: {bw_svg_count}")
            self.list_output_files(output_dir)
            self.log('All SVG file links updated.')
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(f'Error during SVG generation:\n{tb}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

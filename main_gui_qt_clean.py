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
    QScrollArea
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

# Import RegularStakesProcessor for SVG generation
from pathlib import Path
import pandas as pd
import sys
sys.path.append(str(Path(__file__).parent / '002 D2C WRITER'))
# Removed direct processor imports, will use discovery
from core.processors import discover_processors, get_all_processors

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
    def create_coloured_regular_photo_stake_for_selected(self):
        # Get the currently selected row in the table
        selected = self.table.selectedItems()
        if not selected:
            self.log('No row selected.')
            return
        row_idx = selected[0].row()
        # Extract row data as dict
        row_data = {}
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text().strip().lower()
            value = self.table.item(row_idx, col).text() if self.table.item(row_idx, col) else ''
            row_data[header] = value
        import pandas as pd
        # Map/rename columns to match processor expectations
        col_map = {
            'order-id': 'order-id',
            'order-item-id': 'order-item-id',
            'sku': 'sku',
            'number-of-items': 'number-of-items',
            'type': 'type',
            'colour': 'colour',
            'graphic': 'graphic',
            'line_1': 'line_1',
            'line 1': 'line_1',
            'line_2': 'line_2',
            'line 2': 'line_2',
            'line_3': 'line_3',
            'line 3': 'line_3',
            'image_path': 'image_path',
            'theme': 'theme',
            'decorationtype': 'decorationtype',
        }
        clean_row = {}
        for k, v in row_data.items():
            mapped = col_map.get(k, None)
            if mapped:
                clean_row[mapped] = v
        # Fill missing expected columns with blank
        for col in ['order-id','order-item-id','sku','number-of-items','type','colour','graphic','line_1','line_2','line_3','image_path','theme','decorationtype']:
            if col not in clean_row:
                clean_row[col] = ''
        # Normalize expected fields
        for norm_col in ['type','colour','graphic','decorationtype']:
            clean_row[norm_col] = clean_row[norm_col].strip().lower()
        df = pd.DataFrame([clean_row])
        self.log(f'[DEBUG] DataFrame sent to PhotoStakesProcessor:\n{df.to_string(index=False)}')
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SVG_OUTPUT")
        graphics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "graphics")
        os.makedirs(output_dir, exist_ok=True)
        from photo_stakes import PhotoStakesProcessor
        self.log(f'Generating Coloured Regular Photo Stake SVG in {output_dir} using graphics from {graphics_path}...')
        processor = PhotoStakesProcessor(graphics_path, output_dir)
        processor.process_orders(df)
        self.log('Coloured Regular Photo Stake SVG generation complete!')
    def contextMenuEvent(self, event):
        from PyQt5.QtWidgets import QMenu
        if not hasattr(self, 'table') or self.table is None:
            return
        pos = self.table.viewport().mapFromGlobal(event.globalPos())
        row = self.table.rowAt(pos.y())
        if row < 0:
            return
        menu = QMenu(self)
        insert_above = menu.addAction("Insert Row Above")
        insert_below = menu.addAction("Insert Row Below")
        delete_row = menu.addAction("Delete Row")
        create_design = menu.addAction("Create Design for Selected")
        create_coloured_regular_photo_stake = menu.addAction("Create Coloured Regular Photo Stake")
        action = menu.exec_(event.globalPos())
        if action == insert_above:
            self.insert_row_at(row)
        elif action == insert_below:
            self.insert_row_at(row + 1)
        elif action == delete_row:
            self.delete_row_at(row)
        elif action == create_design:
            self.create_design_for_selected()
        elif action == create_coloured_regular_photo_stake:
            self.create_coloured_regular_photo_stake_for_selected()

    def insert_row_at(self, row):
        import pandas as pd
        if hasattr(self, 'last_df') and self.last_df is not None and not self.last_df.empty:
            df = self.last_df.copy()
            # Remove duplicate 'No.' and 'Tick' columns if present
            cols = [c for i, c in enumerate(df.columns) if c not in df.columns[:i]]
            df = df[cols]
            # Ensure 'No.' and 'Tick' columns exist in correct positions
            if 'No.' not in df.columns:
                df.insert(0, 'No.', range(1, len(df) + 1))
            if 'Tick' not in df.columns:
                df.insert(1, 'Tick', ['' for _ in range(len(df))])
            blank_row = {col: "" for col in df.columns}
            blank_row['No.'] = row + 1
            blank_row['Tick'] = ''
            df_top = df.iloc[:row]
            df_bottom = df.iloc[row:]
            df = pd.concat([df_top, pd.DataFrame([blank_row]), df_bottom], ignore_index=True)
            # Reassign No. column after insert
            df['No.'] = range(1, len(df) + 1)
            self.last_df = df
            self._render_table(self.last_df)
            self.log(f'Inserted a new blank row at position {row + 1}.')
        else:
            self.log('No DataFrame loaded or table is empty. Please import or create a table first.')
    def delete_row(self):
        # Delete the currently selected row from the table and DataFrame
        selected = self.table.currentRow()
        self.delete_row_at(selected)

    def delete_row_at(self, row):
        if row < 0:
            self.log('No row selected to delete.')
            return
        if hasattr(self, 'last_df') and self.last_df is not None and len(self.last_df) > 0:
            df = self.last_df.copy()
            df = df.drop(df.index[row]).reset_index(drop=True)
            # Reassign No. column after delete
            if 'No.' in df.columns:
                df['No.'] = range(1, len(df) + 1)
            self.last_df = df
            self._render_table(self.last_df)
            self.log(f'Deleted row {row + 1}.')
        else:
            self.log('No DataFrame loaded or table is empty.')

    def add_row(self):
        # Add a blank row to the DataFrame in memory, only if DataFrame exists and is not empty
        if hasattr(self, 'last_df') and self.last_df is not None and not self.last_df.empty:
            df = self.last_df.copy()
            # Remove duplicate 'No.' and 'Tick' columns if present
            cols = [c for i, c in enumerate(df.columns) if c not in df.columns[:i]]
            df = df[cols]
            # Ensure 'No.' and 'Tick' columns exist in correct positions
            if 'No.' not in df.columns:
                df.insert(0, 'No.', range(1, len(df) + 1))
            if 'Tick' not in df.columns:
                df.insert(1, 'Tick', ['' for _ in range(len(df))])
            # Add a blank row with the same columns
            blank_row = {col: "" for col in df.columns}
            blank_row['No.'] = len(df) + 1
            blank_row['Tick'] = ''
            # If SKU column exists, ensure TYPE column is blank (will be filled by lookup on render)
            sku_col = None
            type_col = None
            for idx, col in enumerate(df.columns):
                if col.strip().lower() == 'sku':
                    sku_col = col
                if col.strip().lower() == 'type':
                    type_col = col
            if type_col:
                blank_row[type_col] = ""
            df = pd.concat([df, pd.DataFrame([blank_row])], ignore_index=True)
            # Reassign No. column after add
            df['No.'] = range(1, len(df) + 1)
            self.last_df = df
            self._render_table(self.last_df)
            self.log('Added a new blank row for manual entry.')
        else:
            self.log('No DataFrame loaded or table is empty. Please import or create a table first.')

    def create_design_for_selected(self):
        from PyQt5.QtWidgets import QMessageBox
        import pandas as pd
        # Find the Tick column
        tick_col = None
        for col in range(self.table.columnCount()):
            if self.table.horizontalHeaderItem(col).text().strip().lower() == 'tick':
                tick_col = col
                break
        if tick_col is None:
            self.log('No Tick column found.')
            return
        from PyQt5.QtCore import Qt
        # Debug: log all select_col checkStates before checking checked_rows
        for row in range(self.table.rowCount()):
            item = self.table.item(row, tick_col)
            self.log(f"[create_design_for_selected] Row {row} tick_col item: {item}, id={id(item)}, checkState={item.checkState() if item else 'None'}")
            # Compare with on_table_cell_changed id if available
            # (This requires you to compare the logs manually for now)
        checked_rows = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, tick_col)
            if item is not None and item.flags() & Qt.ItemIsUserCheckable:
                if item.checkState() == Qt.Checked:
                    checked_rows.append(row)
        self.log(f"Checked rows: {checked_rows}")
        if len(checked_rows) != 1:
            QMessageBox.warning(self, 'Select One Row', 'Please tick exactly one row to create a design for that order.')
            return
        selected_row = checked_rows[0]
        # Build a DataFrame with only the selected row (excluding No. and Select columns)
        col_names = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
        data = {}
        for col in range(self.table.columnCount()):
            header = col_names[col]
            item = self.table.item(selected_row, col)
            widget = self.table.cellWidget(selected_row, col)
            if widget is not None and hasattr(widget, "currentText"):
                data[header] = widget.currentText()
            elif item is not None:
                data[header] = item.text()
            else:
                data[header] = ''
        # Remove No. and Tick columns before sending to processor
        for drop_col in ['No.', 'Tick']:
            if drop_col in data:
                del data[drop_col]
        single_df = pd.DataFrame([data])
        # Use the same logic as create_all_svgs, but for this single row
        try:
            import os
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SVG_OUTPUT")
            graphics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "graphics")
            os.makedirs(output_dir, exist_ok=True)
            # ... (keep the existing code for getting single_df, output_dir, graphics_path)
            order = single_df.iloc[0] # This is a pd.Series

            processor_used = False
            generated_svg_path = None

            if not hasattr(self, 'processors') or not self.processors:
                self.log("Processors not loaded. Attempting to discover them now.")
                discover_processors()
                self.processors = get_all_processors()
                if not self.processors:
                    QMessageBox.warning(self, 'Error', 'No processors loaded. Cannot create design.')
                    return
                self.log(f"Loaded processors: {', '.join(self.processors.keys())}")


            for processor_name, processor_class in self.processors.items():
                try:
                    processor_instance = processor_class(graphics_path=graphics_path, output_dir=output_dir)
                    if processor_instance.is_applicable(order):
                        self.log(f"[DEBUG] Using {processor_name} for the selected order.")

                        # Define a unique filename for the single SVG
                        order_id = str(order.get('order-id', 'NO_ORDER_ID')).strip()
                        sku = str(order.get('sku', 'NO_SKU')).strip()
                        graphic_val = str(order.get('graphic', '')).strip()
                        if graphic_val.lower().endswith('.png'):
                            graphic_val = graphic_val[:-4]

                        # Try to get type and colour for filename, default if not present
                        type_val = str(order.get('type', 'TYPE_UNKNOWN')).strip().lower().replace(' ', '_')
                        colour_val = str(order.get('colour', 'COLOUR_UNKNOWN')).strip().lower().replace(' ', '_')

                        custom_filename_parts = [order_id, sku, processor_name, type_val, colour_val, graphic_val]
                        custom_filename = '_'.join(filter(None, custom_filename_parts)).strip() + '.svg'
                        # Sanitize filename (optional, but good practice)
                        custom_filename = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in custom_filename)

                        output_svg_path = os.path.join(output_dir, custom_filename)

                        # The `process` method expects a DataFrame, so convert the Series back to a DataFrame
                        order_df = pd.DataFrame([order])
                        processor_instance.process(order_df, output_dir, graphics_path) # Process expects a DataFrame

                        # Check if the specific file was created by this processor
                        # This assumes the processor creates the file with the exact name or a predictable one.
                        # For more robustness, the `process` method of the processor could return the path of the generated file.
                        # For now, we'll assume the first SVG created in the process call for this single order is the one.

                        # To find the generated SVG, we can check which SVG was created/modified last
                        # or, if the processor.process() is modified to return filename(s)

                        # Simplified: Assume the processor created output_svg_path or similar
                        # This part might need refinement based on how processors name files for single items.
                        # For now, let's assume the `process` method handles naming and we just log what we tried.

                        # We need a reliable way to get the *actual* path of the generated SVG.
                        # Let's assume the processor, when called with a single item DataFrame,
                        # will generate a file with a name we can either predict or it returns.
                        # If `processor_instance.process` is not modified to return the path,
                        # we might need to list files before/after, or make assumptions.

                        # For this refactoring, let's assume the processor creates a file, and we'll log the expected path.
                        # The `list_output_files` and `refresh_svg_thumbnails` will pick up any new SVGs.
                        # A more advanced solution would be for `process` to return the path(s) of generated files.

                        self.log(f"Custom SVG generation attempted with {processor_name}. Expected output like: {output_svg_path}")
                        processor_used = True
                        # Since we don't know the exact filename, we won't set generated_svg_path here.
                        # The user will see all new SVGs in the output list.
                        break # Found an applicable processor
                except Exception as proc_exc:
                    import traceback
                    tb_proc = traceback.format_exc()
                    self.log(f"Error during single design generation with {processor_name}:\n{tb_proc}")

            if not processor_used:
                QMessageBox.warning(self, 'No Matching Processor', 'The selected row does not match any eligible SVG processor. Please check the order data and processor applicability logic.')
                self.log('No eligible processor found for selected row.')
            else:
                self.list_output_files(output_dir) # Refresh file list
                self.refresh_svg_thumbnails()

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(f'Error during single design generation:\n{tb}')

    def log(self, message):
        # Append message to the log output widget and print to console
        if hasattr(self, 'log_output') and self.log_output is not None:
            self.log_output.append(message)
        print(message)

    def on_table_cell_changed(self, item, column=None):
        from PyQt5.QtCore import Qt
        # Support both (item: QTableWidgetItem) and (row: int, column: int) signatures
        if hasattr(item, 'row') and hasattr(item, 'column'):
            row = item.row()
            column = item.column()
        elif isinstance(item, int) and column is not None:
            row = item
            item = self.table.item(row, column)
        else:
            return
        if item is not None and item.flags() & Qt.ItemIsUserCheckable:
            self.log(f"Cell changed: row={row}, col={column}, checkState={item.checkState()}")
            # Sync ticked state to DataFrame
            tick_col = None
            for col in range(self.table.columnCount()):
                if self.table.horizontalHeaderItem(col).text().strip().lower() == 'tick':
                    tick_col = col
                    break
            if tick_col is not None and hasattr(self, 'filtered_df') and self.filtered_df is not None:
                tick_col_name = self.table.horizontalHeaderItem(tick_col).text()
                if row < len(self.filtered_df) and tick_col_name in self.filtered_df.columns:
                    if item.checkState() == Qt.Checked:
                        self.filtered_df.loc[self.filtered_df.index[row], tick_col_name] = '1'
                    else:
                        self.filtered_df.loc[self.filtered_df.index[row], tick_col_name] = ''
                else:
                    self.log(f"[on_table_cell_changed] WARNING: Row {row} or column '{tick_col_name}' out of bounds for filtered_df (len={len(self.filtered_df)}, columns={list(self.filtered_df.columns)})")
                for r in range(self.table.rowCount()):
                    it = self.table.item(r, tick_col)
                    self.log(f"[on_table_cell_changed] Row {r} tick_col item: {it}, id={id(it)}, checkState={it.checkState() if it else 'None'}")
            self.table.viewport().update()
        self.update_preview_pane()
        try:
            if self.last_df is not None and self.filtered_df is not None:
                col_name = self.table.horizontalHeaderItem(column).text()
                new_value = self.table.item(row, column).text()
                # Find the index in last_df that matches the filtered row
                filtered_index = self.filtered_df.index[row]
                self.last_df.at[filtered_index, col_name] = new_value
                self.filtered_df.at[filtered_index, col_name] = new_value
                self.log(f'Cell updated: row {row}, column {col_name} -> {new_value}')
        except Exception as e:
            self.log(f'Error updating DataFrame from table edit: {e}')



    def create_all_svgs(self):
        """Generate all SVGs using discovered processors."""
        if not hasattr(self, 'last_df') or self.last_df is None or self.last_df.empty:
            self.log('No processed orders available for SVG generation.')
            return

        if not hasattr(self, 'processors') or not self.processors:
            self.log('No processors loaded. Please check the processor discovery mechanism.')
            # Attempt to discover processors again if not loaded
            discover_processors()
            self.processors = get_all_processors()
            if not self.processors:
                self.log('Failed to load processors on second attempt.')
                return
            self.log(f"Re-loaded processors: {', '.join(self.processors.keys())}")


        try:
            import os
            import pandas as pd
            df = self.last_df.copy() # Use the full, unfiltered DataFrame

            # Prepare output and graphics paths
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SVG_OUTPUT")
            graphics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "graphics")
            os.makedirs(output_dir, exist_ok=True)

            svg_log = []
            generated_files_count = 0

            self.log(f"Starting SVG generation for {len(df)} orders using {len(self.processors)} processors...")

            for processor_name, processor_class in self.processors.items():
                self.log(f"--- Running processor: {processor_name} ---")
                try:
                    # Instantiate the processor
                    processor_instance = processor_class(graphics_path=graphics_path, output_dir=output_dir)

                    # Filter DataFrame for applicable orders for this processor
                    # The processor instance itself should define what makes an order applicable
                    applicable_orders_df = df[df.apply(processor_instance.is_applicable, axis=1)].copy()

                    if not applicable_orders_df.empty:
                        self.log(f"Processor {processor_name} is applicable to {len(applicable_orders_df)} orders.")

                        # Store list of files before processing
                        before_files = set(os.listdir(output_dir))

                        # Call the process method
                        processor_instance.process(applicable_orders_df, output_dir, graphics_path)

                        # Determine newly created files
                        after_files = set(os.listdir(output_dir))
                        new_files = after_files - before_files

                        for f_name in new_files:
                            if f_name.lower().endswith('.svg'):
                                svg_log.append({'svg_filename': f_name, 'processor_used': processor_name})
                                generated_files_count += 1

                        self.log(f"Processor {processor_name} completed. Generated {len(new_files)} file(s).")
                    else:
                        self.log(f"Processor {processor_name} is not applicable to any of the current orders.")

                except Exception as proc_exc:
                    import traceback
                    tb_proc = traceback.format_exc()
                    self.log(f"Error during {processor_name} execution:\n{tb_proc}")

            self.log(f"--- SVG Generation Summary ---")
            if generated_files_count > 0:
                self.log(f"Successfully generated {generated_files_count} SVG file(s) in total.")
                # Write CSV log
                if svg_log:
                    log_df = pd.DataFrame(svg_log)
                    csv_path = os.path.join(output_dir, 'svg_generation_log.csv')
                    log_df.to_csv(csv_path, index=False)
                    self.log(f'SVG generation log written to {csv_path}')
            else:
                self.log("No SVG files were generated by any processor.")

            self.list_output_files(output_dir) # Update file list in GUI
            self.refresh_svg_thumbnails() # Refresh SVG previews in GUI
            self.log('SVG generation process finished.')

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(f'Critical error during SVG generation process:\n{tb}')

    def save_state(self):
        try:
            with open("last_state.pkl", "wb") as f:
                pickle.dump(self.last_df, f)
            self.log("Saved last DataFrame state.")
        except Exception as e:
            self.log(f"Error saving state: {e}")

    def load_state(self):
        import os
        try:
            if os.path.exists("last_state.pkl"):
                with open("last_state.pkl", "rb") as f:
                    self.last_df = pickle.load(f)
                self.log("Loaded last DataFrame state.")
                if self.last_df is not None:
                    # Prepend 'Small ' to graphic for small stakes
                    mask = self.last_df['type'].astype(str).str.lower().isin(['small stake', 'small metal'])
                    def prefix_small(val):
                        if pd.isna(val) or str(val).strip() == '':
                            return val
                        s = str(val)
                        return s if s.lower().startswith('small ') else 'Small ' + s
                    if 'graphic' in self.last_df.columns:
                        self.last_df.loc[mask, 'graphic'] = self.last_df.loc[mask, 'graphic'].apply(prefix_small)
                    self._render_table(self.last_df)
        except Exception as e:
            self.log(f"Error loading state: {e}")

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

        self.last_df = None
        self.setMinimumSize(600, 400)
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

        # Table widget (center)
        self.table = QTableWidget()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.setAlternatingRowColors(True)  # Enable alternate row coloring
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemSelectionChanged.connect(self.update_preview_pane)
        center_layout.addWidget(self.table)

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
        self.last_df = None  # Store the last loaded DataFrame
        # Restore last state after all widgets are initialized
        self.load_state()

        # Discover and load processors
        discover_processors()
        self.processors = get_all_processors()
        self.log(f"Loaded processors: {', '.join(self.processors.keys())}")

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
            df = order_pipeline.process_amazon_orders(self.selected_files, images_dir, output_dir, skulist_path=skulist_path, status_callback=self.log)
            self.last_df = df  # Store for copy-to-clipboard
            self._render_table(df)
            self.copy_button.setEnabled(True)
            self.log(f'Order processing complete. {len(df)} orders processed. Images saved to images.')
        except Exception as e:
            deco_keys = ['decorationtype', 'decorationtype2', 'decorationtype_', 'decoration', 'decorationtype ', 'decorationtype']
            colour_col = next((normalized_map[k] for k in colour_keys if k in normalized_map), None)
            deco_col = next((normalized_map[k] for k in deco_keys if k in normalized_map), None)
            if colour_col and deco_col:
                cols = original_cols.copy()
                if cols.index(deco_col) != cols.index(colour_col) + 1:
                    cols.remove(deco_col)
                    cols.insert(cols.index(colour_col) + 1, deco_col)
                    df = df[cols]
                    self.log('Reordered columns: moved Decoration next to Colour.')
        except Exception as err:
            self.log(f'Column reorder warning: {err}')
        # --- Sort by Stake, then Colour, then DecorationType ---
        try:
            # Normalize columns for robust matching
            normalized_map = {c.lower().replace(' ', '').replace('_', ''): c for c in df.columns}
            stake_col = next((normalized_map[k] for k in ['stake', 'producttype', 'product'] if k in normalized_map), None)
            colour_col = next((normalized_map[k] for k in ['colour', 'color'] if k in normalized_map), None)
            deco_col = next((normalized_map[k] for k in ['decorationtype', 'decorationtype2', 'decorationtype_', 'decoration', 'decorationtype ', 'decotype'] if k in normalized_map), None)
            sort_cols = [c for c in [stake_col, colour_col, deco_col] if c]
            if sort_cols:
                df = df.sort_values(by=sort_cols, kind='stable', na_position='last').reset_index(drop=True)
                self.log(f"Sorted table by: {', '.join(sort_cols)}.")
        except Exception as err:
            self.log(f'Sort warning: {err}')
        # Store full DataFrame for filtering (with updated column order)
        self.last_df = df.copy()
        self.filtered_df = df.copy()
        # Enable table editing
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        # Connect cellChanged to update DataFrame
        # Disconnect cellChanged if previously connected, only use itemChanged
        try:
            self.table.cellChanged.disconnect()
        except Exception:
            pass
        # itemChanged is connected in _render_table after setup
        self._render_table(df)

    def _render_table(self, df):
        # --- Add SVG Processor column ---
        import pandas as pd
        def get_svg_processor(row):
            # Ensure processors are loaded
            if not hasattr(self, 'processors') or not self.processors:
                # This is a fallback, ideally processors are loaded at init
                discover_processors()
                self.processors = get_all_processors()
                if not self.processors:
                    return "Error: No processors loaded"

            applicable_processor_name = "No matching processor"
            for processor_name, processor_class_ref in self.processors.items():
                # We need an instance to call is_applicable.
                # This means instantiating each processor for each row, which might be inefficient.
                # Consider optimizing if performance becomes an issue (e.g., by passing class and data to a static check method).
                # For now, let's proceed with instantiation.
                # We need dummy paths for instantiation if the processor expects them.
                # A better approach for `is_applicable` would be to make it a static method or class method
                # that doesn't require full instantiation if graphics_path/output_dir aren't needed for the check.
                # Assuming processors can be instantiated without paths for `is_applicable` or handle None.
                try:
                    # Try instantiating with None for paths if constructor allows,
                    # otherwise, this needs a more robust way to check applicability.
                    # For now, this assumes is_applicable can be called on an instance
                    # created without full paths, or that the base class handles this.
                    # This part is tricky without knowing all processor constructors.
                    # A practical approach: is_applicable should ideally be a static method or class method.
                    # If it *must* be an instance method, the instance must be creatable.

                    # Let's assume a temporary, simplified instantiation for the check if possible,
                    # or that the check is robust enough.
                    # This is a placeholder for a potentially more complex instantiation for checking.
                    # A common pattern is to pass graphics_path and output_dir to the constructor.
                    # If is_applicable doesn't use them, it's fine.
                    # For now, we pass dummy values as they are expected by the base class constructor (implicitly).
                    # This will be an issue if processors *require* valid paths in their __init__ for is_applicable to work.

                    # Simplification: We assume `is_applicable` can be called on an instance
                    # created with placeholder paths if the actual paths are not used by `is_applicable`.
                    # This will need to be true for all processor implementations.
                    temp_output_dir = "" # Placeholder
                    temp_graphics_path = "" # Placeholder

                    # A more robust way:
                    # proc_instance = processor_class_ref(graphics_path=self.some_default_graphics_path, output_dir=self.some_default_output_dir)
                    # This requires having default paths available or making is_applicable static.
                    # For now, we'll assume the test below is what's needed.
                    # The GUI needs valid paths for actual processing, but maybe not for this check.
                    # The current ProcessorBase does not define a constructor, so subclasses might.
                    # This is a point of potential fragility.

                    # Let's assume that `is_applicable` does not require initialized paths,
                    # or that processors are robust to being instantiated with dummy paths for this check.
                    # The `process` method will receive the correct paths.

                    # Given the current structure, we must instantiate.
                    # If `graphics_path` and `output_dir` are needed by `is_applicable`,
                    # they should be available here. Let's assume they are not strictly needed for the check.

                    # Create a dummy instance to call is_applicable
                    # This assumes __init__(self, graphics_path, output_dir) signature for all processors
                    # This is a potential issue if processors have different __init__ signatures.
                    # The base class does not enforce __init__ signature.

                    # Fallback: if a processor cannot be instantiated easily for a check,
                    # this logic will fail. The `is_applicable` method should ideally be a
                    # static method on the processor class for this exact reason.
                    # processor_instance = processor_class_ref(None, None) # Simplest attempt

                    # Given the refactored `create_all_svgs`, processors are instantiated with:
                    # processor_class(graphics_path=graphics_path, output_dir=output_dir)
                    # We should mimic this if these are needed for `is_applicable`.
                    # However, `graphics_path` and `output_dir` are not readily available in `_render_table`
                    # without passing them down or making them class attributes.

                    # Simplest approach: Try to call it as a static method if possible,
                    # or assume it can be called on a class instance that might not be fully initialized.
                    # This is a known limitation of this dynamic approach if `is_applicable` is complex.

                    # Let's assume `is_applicable` can be called from a class reference if it's static
                    # or that we can create a temporary instance.
                    # For now, we cannot reliably instantiate here without making assumptions about constructors.
                    #
                    # WORKAROUND/SIMPLIFICATION for get_svg_processor:
                    # Since we cannot reliably instantiate here for all processors without knowing their constructors,
                    # and `is_applicable` is an instance method, this `get_svg_processor` for the table
                    # display becomes problematic.
                    #
                    # Option 1: Make `is_applicable` a @classmethod or @staticmethod. (Best solution, requires processor changes)
                    # Option 2: Attempt a simple instantiation. (Fragile)
                    # Option 3: Remove this "SVG Processor" column from the table if it's too hard to compute reliably.
                    # Option 4: Pass necessary paths to _render_table.
                    #
                    # Let's try Option 2 with a try-except, but acknowledge its fragility.
                    try:
                        # This assumes a constructor that can take no args, or default args,
                        # or that graphics_path/output_dir are not used by is_applicable.
                        # This is a major assumption.
                        # A better way for ProcessorBase would be:
                        # @staticmethod or @classmethod
                        # def is_row_applicable(row_data: pd.Series, config_params_if_needed) -> bool:

                        # If processors follow `__init__(self, graphics_path, output_dir)`:
                        # This is still problematic as we don't have those paths here easily.
                        #
                        # TEMPORARY: Return "Dynamic" as we can't easily determine it per row here
                        # without significant changes to either processors or how this GUI function works.
                        # The actual processing in `create_all_svgs` and `create_design_for_selected` *will* use the correct logic.
                        # This is just for display in the table.
                        #
                        # For the purpose of this refactoring, we will simplify this display part.
                        # The real test is if the `create_all_svgs` and `create_design_for_selected` work.
                        # We can make is_applicable a class method in a follow-up if needed.

                        # Let's assume a simplified check for now for the display column,
                        # or leave it to the processor to have a simple __init__
                        # This is a known weak point in the current design for display purposes.
                        # processor_obj = processor_class_ref(graphics_path="dummy", output_dir="dummy") # Example
                        # if processor_obj.is_applicable(row):
                        # applicable_processor_name = processor_name
                        # break

                        # Given the constraints, we cannot reliably call is_applicable here for display.
                        # The actual processing logic in create_all_svgs and create_design_for_selected is more robust.
                        # So, for this table display column, we might have to simplify or remove it.
                        # To keep the column for now, we'll return a generic value.
                        # This means the "SVG Processor" column will not be accurate until processors are refactored
                        # to support a static check or easier instantiation for this display purpose.
                        pass # Skip trying to determine for display for now.

                    except TypeError: # Catches errors if constructor args are missing
                        # self.log(f"Warning: Could not instantiate {processor_name} for applicability check in table.")
                        pass # Cannot determine here
                    except Exception as e_inst:
                        # self.log(f"Error instantiating {processor_name} for display check: {e_inst}")
                        pass


            # The above loop for display is problematic. We will return a placeholder.
            # The actual processor assignment happens during `create_all_svgs` and `create_design_for_selected`.
            # This column is for display only and its accuracy is secondary to processing.
            # To make this work, `is_applicable` should ideally be a class method or static method.
            # For now, we'll just indicate it's dynamically determined.
            return "Dynamic (see log)" # Placeholder until is_applicable can be called safely here

        df = df.copy()
        df['SVG Processor'] = df.apply(get_svg_processor, axis=1)

        # Ensure correct graphic for OM008021
        if 'sku' in df.columns and 'graphic' in df.columns:
            mask = df['sku'].astype(str).str.upper() == 'OM008021'
            df.loc[mask, 'graphic'] = 'OM008021.png'
        import os
        import pandas as pd
        from PyQt5.QtCore import Qt
        # Always show only the image filename in the table
        if 'image_path' in df.columns:
            df = df.copy()
            df['image_path'] = df['image_path'].apply(lambda p: os.path.basename(str(p)) if pd.notna(p) else p)
        # Add sequential row number column (1-based) if not already present
        df = df.copy()
        # --- Fix order-id persistence: fill blanks with original values if available ---
        if hasattr(self, 'original_df') and 'order-id' in df.columns and 'order-id' in self.original_df.columns:
            mask_blank = df['order-id'].isnull() | (df['order-id'].astype(str).str.strip() == '')
            df.loc[mask_blank, 'order-id'] = self.original_df.loc[mask_blank, 'order-id']
        # --- Patch: for sku == 'M0634S - CAT - RAINBOW BRIDGE', set graphic ---
        if 'sku' in df.columns and 'graphic' in df.columns:
            mask = df['sku'].astype(str).str.strip().str.upper() == 'M0634S - CAT - RAINBOW BRIDGE'
            df.loc[mask, 'graphic'] = 'Small Rainbow Bridge.png'
        # Ensure 'No.' is always the first column and always sequential 1-based numbers
        if 'No.' not in df.columns:
            df.insert(0, 'No.', range(1, len(df) + 1))
        else:
            df['No.'] = range(1, len(df) + 1)
            # If 'No.' is present but not first, move it to first
            cols = list(df.columns)
            if cols[0] != 'No.':
                cols.remove('No.')
                cols.insert(0, 'No.')
                df = df[cols]
        # Ensure 'Tick' is always the second column
        if 'Tick' not in df.columns:
            df.insert(1, 'Tick', ['' for _ in range(len(df))])
        else:
            cols = list(df.columns)
            if cols[1] != 'Tick':
                cols.remove('Tick')
                cols.insert(1, 'Tick')
                df = df[cols]
        tick_col_index = 1
        # Find the index of the order-id column (case-insensitive)
        order_id_col = None
        for i, col in enumerate(df.columns):
            if col.lower().replace('_', '').replace('-', '') == 'orderid':
                order_id_col = i
                break
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.blockSignals(True)  # Prevent cellChanged from firing during setup
        type_options = [
            "Small Metal", "Medium Metal", "Large Metal", "XL Metal",
            "Small Stake", "Regular Stake", "Large Stake", "Heart Stake"
        ]
        colour_options = [
            "Aluminium", "Brass", "Black", "Slate", "Copper", "Gold", "Silver", "Stone", "Marble"
        ]
        type_col_index = None
        colour_col_index = None
        sku_col_index = None
        for idx, col_name in enumerate(df.columns):
            if col_name.strip().lower() == 'type':
                type_col_index = idx
            if col_name.strip().lower() == 'colour':
                colour_col_index = idx
            if col_name.strip().lower() == 'sku':
                sku_col_index = idx
        # Load SKULIST.csv into a dict {SKU: TYPE}
        skulist_type_map = {}
        try:
            import csv
            csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'SKULIST.csv')
            with open(csv_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                # Robust header normalization
                header_map = {k.strip().upper(): k for k in reader.fieldnames}
                sku_key = header_map.get('SKU')
                type_key = header_map.get('TYPE')
                if not sku_key or not type_key:
                    raise Exception(f"SKULIST.csv missing required columns. Found: {reader.fieldnames}")
                for row in reader:
                    sku = str(row[sku_key]).strip()
                    typ = str(row[type_key]).strip()
                    if sku and typ:
                        skulist_type_map[sku.upper()] = typ
        except Exception as e:
            self.log(f"Could not load SKULIST.csv for type dropdown: {e}")
        
        for row in range(len(df)):
            for col in range(len(df.columns)):
                if col == tick_col_index:
                    item = QTableWidgetItem()
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    gui_item = self.table.item(row, col) if self.table.rowCount() > row and self.table.columnCount() > col else None
                    if gui_item is not None and gui_item.flags() & Qt.ItemIsUserCheckable:
                        item.setCheckState(gui_item.checkState())
                        item.setData(Qt.CheckStateRole, gui_item.checkState())
                    else:
                        item.setCheckState(Qt.Unchecked)
                        item.setData(Qt.CheckStateRole, Qt.Unchecked)
                    item.setText("")
                    self.table.setItem(row, col, item)
                elif type_col_index is not None and col == type_col_index:
                    # Always use the DataFrame value for 'type', only pre-fill from SKULIST.csv if cell is empty
                    current_value = str(df.iat[row, col])
                    if not current_value or current_value.lower() == 'nan':
                        value = ""
                        if sku_col_index is not None:
                            sku_val = str(df.iat[row, sku_col_index]).strip().upper()
                            if sku_val in skulist_type_map:
                                value = skulist_type_map[sku_val]
                        current_value = value
                    item = QTableWidgetItem(current_value)
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
                elif colour_col_index is not None and col == colour_col_index:
                    from PyQt5.QtWidgets import QComboBox
                    combo = QComboBox()
                    combo.addItems(colour_options)
                    current_value = str(df.iat[row, col])
                    if current_value in colour_options:
                        combo.setCurrentText(current_value)
                    else:
                        combo.setCurrentIndex(-1)
                    def make_on_colour_changed(r=row, c=col):
                        def on_colour_changed():
                            val = combo.currentText()
                            self.table.blockSignals(True)
                            self.table.setItem(r, c, QTableWidgetItem(val))
                            self.table.blockSignals(False)
                            # Update DataFrame immediately
                            if hasattr(self, 'last_df') and self.last_df is not None:
                                self.last_df.iat[r, c] = val
                        return on_colour_changed
                    combo.currentIndexChanged.connect(make_on_colour_changed())
                    self.table.setCellWidget(row, col, combo)
                else:
                    item = QTableWidgetItem(str(df.iat[row, col]))
                    self.table.setItem(row, col, item)
        self.table.blockSignals(False)
        self.table.resizeColumnsToContents()
        # Explicitly set edit triggers for the table
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        # Ensure on_table_cell_changed is connected
        try:
            self.table.itemChanged.disconnect()
        except Exception:
            pass
        self.table.itemChanged.connect(self.on_table_cell_changed)

    def clear_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.last_df = None
        self.filtered_df = None
        self.log('Table cleared.')

    def export_table_csv(self):
        df_to_export = getattr(self, 'filtered_df', None)
        if df_to_export is None or df_to_export.empty:
            df_to_export = getattr(self, 'last_df', None)
        if df_to_export is not None and not df_to_export.empty:
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as CSV', '', 'CSV Files (*.csv)')
            if path:
                df_to_export.to_csv(path, index=False, encoding='utf-8-sig')
                self.log(f'Table exported as CSV: {path}')
        else:
            self.log('No data to export.')

    def export_table_txt(self):
        df_to_export = getattr(self, 'filtered_df', None)
        if df_to_export is None or df_to_export.empty:
            df_to_export = getattr(self, 'last_df', None)
        if df_to_export is not None and not df_to_export.empty:
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as TXT', '', 'Text Files (*.txt)')
            if path:
                df_to_export.to_csv(path, sep='\t', index=False, encoding='utf-8')
                self.log(f'Table exported as TXT: {path}')
        else:
            self.log('No data to export.')

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

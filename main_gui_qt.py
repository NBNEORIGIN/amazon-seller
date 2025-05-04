print("RUNNING main_gui_qt.py FROM:", __file__)
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QSplitter, QHBoxLayout, QLineEdit, QCheckBox, QMessageBox
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

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

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AmazonSeller Order Processor')
        self.setMinimumSize(600, 400)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_vlayout = QVBoxLayout(central_widget)

        self.drop_zone = DropZone(self)
        main_vlayout.addWidget(self.drop_zone)
        self.drop_zone.file_dropped.connect(self.on_file_dropped)

        self.process_button = QPushButton('Process Orders')
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_orders)
        main_vlayout.addWidget(self.process_button)

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
        self.create_svgs_button = QPushButton('Create SVGs')
        self.create_svgs_button.setEnabled(False)
        self.create_svgs_button.clicked.connect(self.generate_svgs)
        control_bar.addWidget(self.create_svgs_button)
        self.warnings_only_checkbox = QCheckBox('Show Only Warnings')
        self.warnings_only_checkbox.stateChanged.connect(self.filter_table)
        control_bar.addWidget(self.warnings_only_checkbox)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Search orders...')
        self.search_box.textChanged.connect(self.filter_table)
        control_bar.addWidget(self.search_box)
        main_vlayout.addLayout(control_bar)

        # Main splitter: left (table), right (preview)
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Horizontal)

        # Table widget (center-left)
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setFont(QFont('Consolas', 10))
        main_splitter.addWidget(self.table)

        # Preview pane (right)
        self.preview_pane = QWidget()
        preview_layout = QVBoxLayout(self.preview_pane)
        self.svg_widget = QSvgWidget()
        self.svg_widget.setMinimumSize(200, 200)
        preview_layout.addWidget(self.svg_widget)
        self.csv_preview_label = QLabel('CSV Preview:')
        preview_layout.addWidget(self.csv_preview_label)
        self.csv_text = QTextEdit()
        self.csv_text.setReadOnly(True)
        self.csv_text.setMinimumHeight(120)
        preview_layout.addWidget(self.csv_text)
        btn_layout = QHBoxLayout()
        self.open_svg_btn = QPushButton('Open SVG')
        self.open_svg_btn.clicked.connect(self.open_selected_svg)
        btn_layout.addWidget(self.open_svg_btn)
        self.open_csv_btn = QPushButton('Open CSV')
        self.open_csv_btn.clicked.connect(self.open_selected_csv)
        btn_layout.addWidget(self.open_csv_btn)
        preview_layout.addLayout(btn_layout)
        self.preview_label = QLabel('Select a row to preview SVG/CSV.')
        self.preview_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.preview_label)
        self.current_svg_path = None
        self.current_csv_path = None
        self.table.itemSelectionChanged.connect(self.update_preview_pane)
        main_splitter.addWidget(self.preview_pane)
        main_splitter.setSizes([800, 400])  # Table wider than preview by default

        main_vlayout.addWidget(main_splitter, stretch=1)

        # Copy to Clipboard button
        self.copy_button = QPushButton('Copy to Clipboard')
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_table_to_clipboard)
        main_vlayout.addWidget(self.copy_button)

        # Log/terminal output at the bottom
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont('Consolas', 10))
        main_vlayout.addWidget(self.log_output)

        self.selected_files = None
        self.last_df = None  # Store the last loaded DataFrame

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
            # Use the directory of the first file for outputs
            images_dir = os.path.join(os.path.dirname(self.selected_files[0]), "004 IMAGES")
            output_dir = os.path.join(os.path.dirname(self.selected_files[0]), "SVG_OUTPUT")
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)
            self.log(f'Processing Amazon order files ({len(self.selected_files)}), downloading images, parsing XML...')
            skulist_path = r"G:/My Drive/003 APPS/002 AmazonSeller/001 AMAZON DATA DOWNLOAD/SKULIST.csv"
            df = order_pipeline.process_amazon_orders(self.selected_files, images_dir, output_dir, skulist_path=skulist_path)
            self.last_df = df  # Store for copy-to-clipboard
            self.populate_table(df)
            self.copy_button.setEnabled(True)
            self.create_svgs_button.setEnabled(True)
            # Copy output.txt and output.csv to central folder for stake processors
            try:
                import shutil
                src_txt = os.path.join(output_dir, 'output.txt')
                dst_txt = os.path.join(os.path.dirname(__file__), '001 AMAZON DATA DOWNLOAD', 'output.txt')
                if os.path.exists(src_txt):
                    shutil.copy2(src_txt, dst_txt)
                src_csv = os.path.join(output_dir, 'output.csv')
                dst_csv = os.path.join(os.path.dirname(__file__), '001 AMAZON DATA DOWNLOAD', 'output.csv')
                if os.path.exists(src_csv):
                    shutil.copy2(src_csv, dst_csv)
            except Exception as copy_err:
                self.log(f'Warning: could not copy output files for stake scripts: {copy_err}')
            self.log(f'Order processing complete. {len(df)} orders processed. Images saved to 004 IMAGES.')
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(f'Error during processing:\n{tb}')

    def populate_table(self, df):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        if df is None or df.empty:
            self.last_df = None
            return
        # Store full DataFrame for filtering
        self.last_df = df.copy()
        self.filtered_df = df.copy()
        self._render_table(df)

    def _render_table(self, df):
        # Preferred column order
        preferred_columns = [
            'order-id', 'order-item-id', 'sku', 'number-of-items',
            'type', 'colour', 'graphic', 'theme',
            'line_1', 'line_2', 'line_3', 'image_path', 'Warnings'
        ]
        columns = [col for col in preferred_columns if col in df.columns]
        columns += [col for col in df.columns if col not in columns]
        self.table.setColumnCount(len(columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels([str(col) for col in columns])
        for row in range(len(df)):
            for col, colname in enumerate(columns):
                item = QTableWidgetItem(str(df.iloc[row][colname]))
                self.table.setItem(row, col, item)
        self.table.resizeColumnsToContents()

    def clear_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.last_df = None
        self.filtered_df = None
        self.log('Table cleared.')

    def export_table_csv(self):
        if self.filtered_df is not None and not self.filtered_df.empty:
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as CSV', '', 'CSV Files (*.csv)')
            if path:
                self.filtered_df.to_csv(path, index=False, encoding='utf-8-sig')
                self.log(f'Table exported as CSV: {path}')
        else:
            self.log('No data to export.')

    def export_table_txt(self):
        if self.filtered_df is not None and not self.filtered_df.empty:
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as TXT', '', 'Text Files (*.txt)')
            if path:
                self.filtered_df.to_csv(path, sep='\t', index=False, encoding='utf-8')
                self.log(f'Table exported as TXT: {path}')
        else:
            self.log('No data to export.')

    def open_output_folder(self):
        if self.selected_files and len(self.selected_files) > 0:
            folder = os.path.join(os.path.dirname(self.selected_files[0]), "SVG_OUTPUT")
            if os.path.exists(folder):
                import subprocess
                subprocess.Popen(['start', '', folder], shell=True)
                self.log(f'Opened output folder: {folder}')
            else:
                self.log('Output folder does not exist.')
        else:
            self.log('No output folder to open.')

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
        selected = self.table.selectedItems()
        if not selected:
            self.svg_widget.load(b"")
            self.csv_text.setText("")
            self.preview_label.setText("Select a row to preview SVG/CSV.")
            self.current_svg_path = None
            self.current_csv_path = None
            return
        row = selected[0].row()
        svg_path = None
        csv_path = None
        # Try to get SVG path from 'image_path' or similar column
        image_col = None
        for col in range(self.table.columnCount()):
            if self.table.horizontalHeaderItem(col).text().lower() == 'image_path':
                image_col = col
                break
        if image_col is not None:
            svg_path = self.table.item(row, image_col).text()
            if svg_path and svg_path.lower().endswith('.svg') and os.path.exists(svg_path):
                self.svg_widget.load(svg_path)
                self.preview_label.setText(f"Previewing: {os.path.basename(svg_path)}")
                self.current_svg_path = svg_path
            else:
                self.svg_widget.load(b"")
                self.preview_label.setText("No SVG found for this row.")
                self.current_svg_path = None
        else:
            self.svg_widget.load(b"")
            self.preview_label.setText("No SVG found for this row.")
            self.current_svg_path = None
        # Try to get CSV path from SVG path (same basename, .csv extension)
        if self.current_svg_path:
            csv_path = os.path.splitext(self.current_svg_path)[0] + '.csv'
            if os.path.exists(csv_path):
                with open(csv_path, encoding='utf-8') as f:
                    lines = f.readlines()
                    self.csv_text.setText(''.join(lines[:20]))  # Show first 20 lines
                self.current_csv_path = csv_path
            else:
                self.csv_text.setText("No CSV found for this SVG.")
                self.current_csv_path = None
        else:
            self.csv_text.setText("")
            self.current_csv_path = None

    def open_selected_svg(self):
        if self.current_svg_path and os.path.exists(self.current_svg_path):
            import subprocess
            subprocess.Popen(['start', '', self.current_svg_path], shell=True)
        else:
            self.log('No SVG file to open.')

    def open_selected_csv(self):
        if self.current_csv_path and os.path.exists(self.current_csv_path):
            import subprocess
            subprocess.Popen(['start', '', self.current_csv_path], shell=True)
        else:
            self.log('No CSV file to open.')

    def log(self, message):
        self.log_output.append(message)

    def generate_svgs(self):
        """Generate Regular, B&W, and Photo stake SVGs for the currently processed orders."""
        if not hasattr(self, 'selected_files') or not self.selected_files:
            self.log('No order files selected – cannot create SVGs.')
            QMessageBox.warning(self, 'Create SVGs', 'Please process orders first.')
            return

        try:
            import subprocess, sys, os

            svg_output = os.path.join(os.path.dirname(self.selected_files[0]), 'SVG_OUTPUT')
            os.makedirs(svg_output, exist_ok=True)

            script_dir = os.path.join(os.path.dirname(__file__), '002 D2C WRITER')
            graphics_path = r'G:/My Drive/001 NBNE/001 M/M0634 - METALLIC PERSONALISED MEMORIAL - DICK, TOM/001 Design/002 MUTOH/002 AUTODESIGN'
            images_path = r'G:/My Drive/003 APPS/002 AmazonSeller/004 IMAGES'

            self.log('Creating SVGs...')

            subprocess.run([sys.executable, os.path.join(script_dir, 'regular_stakes.py'), svg_output, graphics_path], check=True)
            subprocess.run([sys.executable, os.path.join(script_dir, 'bw_stakes.py'), svg_output, graphics_path], check=True)
            subprocess.run([sys.executable, os.path.join(script_dir, 'photo_stakes.py'), svg_output, graphics_path, images_path], check=True)

            QMessageBox.information(self, 'Create SVGs', f'Regular, B&W, and Photo stake SVGs generated in:\n{svg_output}')
            self.log(f'SVGs generated in {svg_output}')

        except subprocess.CalledProcessError as cpe:
            self.log(f'SVG generation script failed: {cpe}')
            QMessageBox.critical(self, 'Create SVGs', f'SVG script failed:\n{cpe}')
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(f'Error generating SVGs:\n{tb}')
            QMessageBox.critical(self, 'Create SVGs', f'Failed to generate SVGs:\n{e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

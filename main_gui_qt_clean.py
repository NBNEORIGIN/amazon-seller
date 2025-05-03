print("RUNNING main_gui_qt.py FROM:", __file__)
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QSplitter, QHBoxLayout, QLineEdit, QCheckBox, QTextBrowser
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

        # --- Left pane: DropZone and Process Orders button ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(4, 4, 4, 4)
        left_layout.setSpacing(8)
        self.drop_zone = DropZone(self)
        self.drop_zone.setFont(QFont('Arial', 10))
        self.drop_zone.setStyleSheet('border: 2px dashed #aaa; padding: 12px; background: #fafafa;')
        self.drop_zone.setFixedWidth(180)
        left_layout.addWidget(self.drop_zone)
        self.drop_zone.file_dropped.connect(self.on_file_dropped)
        self.process_button = QPushButton('Process')
        self.process_button.setFixedWidth(120)
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_orders)
        left_layout.addWidget(self.process_button)
        left_layout.addStretch(1)

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
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemSelectionChanged.connect(self.update_preview_pane)
        center_layout.addWidget(self.table)

        # --- Right pane: Output SVG/CSV file list ---
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(4)
        self.preview_label = QLabel('Output SVG and CSV Files')
        self.file_links_browser = QTextBrowser()
        self.file_links_browser.setOpenLinks(False)
        self.file_links_browser.anchorClicked.connect(self.open_output_file)
        preview_layout.addWidget(self.file_links_browser)

        # --- Main horizontal splitter: left (drag/drop), center (table/controls), right (preview) ---
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Horizontal)
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(center_widget)
        main_splitter.addWidget(preview_widget)
        main_splitter.setSizes([180, 600, 400])
        main_vlayout.addWidget(main_splitter, stretch=1)

        # Copy to Clipboard button
        self.copy_button = QPushButton('Copy to Clipboard')
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_table_to_clipboard)
        main_vlayout.addWidget(self.copy_button)

        # SVG Generation button
        self.svg_button = QPushButton('Generate Regular SVGs')
        self.svg_button.clicked.connect(self.generate_regular_svgs)
        main_vlayout.addWidget(self.svg_button)

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
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iat[row, col]))
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
        # No-op: preview pane now lists output SVG/CSV files instead of per-row preview
        pass

    def open_output_file(self, url):
        import subprocess
        path = url.toLocalFile()
        if os.path.exists(path):
            subprocess.Popen(['start', '', path], shell=True)
        else:
            self.log(f'File not found: {path}')
        # Always refresh the file list to prevent navigation away from the list
        # Find the output directory from the file path
        output_dir = os.path.dirname(path)
        self.list_output_files(output_dir)

    def list_output_files(self, output_dir):
        # List SVGs and their CSVs as hyperlinks in the right pane
        from PyQt5.QtCore import QUrl
        svg_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.svg')]
        svg_files.sort()
        html = '''<style>
        a { color: #1976d2; text-decoration: underline; cursor: pointer; }
        a:hover { color: #0d47a1; }
        ul { padding-left: 18px; }
        </style>
        <b>SVG and CSV Outputs:</b><br><ul>'''
        for svg in svg_files:
            svg_path = os.path.abspath(os.path.join(output_dir, svg))
            csv_path = os.path.splitext(svg_path)[0] + '.csv'
            svg_link = f'<a href="file:///{svg_path}" title="Open SVG in your vector graphics software">{os.path.basename(svg_path)}</a>'
            if os.path.exists(csv_path):
                csv_link = f'<a href="file:///{csv_path}" title="Open CSV in your spreadsheet software">{os.path.basename(csv_path)}</a>'
                html += f'<li>{svg_link} &nbsp;|&nbsp; {csv_link}</li>'
            else:
                html += f'<li>{svg_link}</li>'
        html += '</ul>'
        self.file_links_browser.setHtml(html)

    def generate_regular_svgs(self):
        # Use the currently filtered DataFrame
        if getattr(self, 'filtered_df', None) is None or self.filtered_df.empty:
            self.log('No data to generate SVGs.')
            return
        df = self.filtered_df.copy()
        # Prompt for output directory
        output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        if not output_dir:
            self.log('SVG generation cancelled (no output directory selected).')
            return
        # Automatically select graphics path
        graphics_path = r'G:/My Drive/003 APPS/002 AmazonSeller/005 Assets/001 Graphics'
        if not os.path.exists(graphics_path):
            self.log(f'Graphics folder not found at {graphics_path}. Defaulting to home directory.')
            graphics_path = str(Path.home())
        self.log(f'Generating Regular SVGs in {output_dir} using graphics from {graphics_path}...')
        try:
            processor = RegularStakesProcessor(graphics_path, output_dir)
            processor.process_orders(df)
            # --- Update table with SVG paths ---
            # Find generated SVGs in output_dir
            svg_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.svg')]
            svg_files.sort()  # rely on batch order
            # Map each row to a generated SVG (batching: 9 per SVG)
            image_paths = [''] * len(df)
            batch_size = 9
            for i, svg_file in enumerate(svg_files):
                svg_path = os.path.join(output_dir, svg_file)
                for j in range(batch_size):
                    idx = i * batch_size + j
                    if idx < len(df):
                        image_paths[idx] = svg_path
            # Add or update 'image_path' column
            df['image_path'] = image_paths
            self.filtered_df = df
            self._render_table(df)
            # Log first 10 image_path values for debugging
            sample_paths = df['image_path'].head(10).tolist()
            self.log('First 10 SVG image_path values: ' + str(sample_paths))
            # Update right pane with SVG/CSV hyperlinks
            self.list_output_files(output_dir)
            self.log('Regular SVG generation complete! SVG file links updated.')
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(f'Error during SVG generation:\n{tb}')

    def log(self, message):
        self.log_output.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

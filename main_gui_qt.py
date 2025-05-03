import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
import os

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
        layout = QVBoxLayout(central_widget)

        self.drop_zone = DropZone(self)
        layout.addWidget(self.drop_zone)
        self.drop_zone.file_dropped.connect(self.on_file_dropped)

        self.process_button = QPushButton('Process Orders')
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_orders)
        layout.addWidget(self.process_button)

        # Table to display order data
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setFont(QFont('Consolas', 10))
        layout.addWidget(self.table)

        # Copy to Clipboard button
        self.copy_button = QPushButton('Copy to Clipboard')
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_table_to_clipboard)
        layout.addWidget(self.copy_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont('Consolas', 10))
        layout.addWidget(self.log_output)

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
            return
        # Preferred column order
        preferred_columns = [
            'order-id', 'order-item-id', 'sku', 'number-of-items',
            'type', 'colour', 'graphic', 'theme',
            'line_1', 'line_2', 'line_3', 'image_path', 'Warnings'
        ]
        # Use columns in preferred order if present, then add any extras
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

    def copy_table_to_clipboard(self):
        if self.last_df is not None and not self.last_df.empty:
            text = self.last_df.to_csv(sep='\t', index=False)
            QApplication.clipboard().setText(text)
            self.log('Order data copied to clipboard! Paste into Google Sheets (Ctrl+V).')
        else:
            self.log('No data to copy.')

    def log(self, message):
        self.log_output.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

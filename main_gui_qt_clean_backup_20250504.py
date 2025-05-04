
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QSplitter, QHBoxLayout, QLineEdit, QCheckBox, QTextBrowser
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
# Import RegularStakesProcessor for SVG generation
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
from pathlib import Path
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
import pandas as pd
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
import sys
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
sys.path.append(str(Path(__file__).parent / '002 D2C WRITER'))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
from regular_stakes import RegularStakesProcessor
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
from bw_stakes import BWStakesProcessor
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
from photo_stakes import PhotoStakesProcessor
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
from bw_photo_stakes import BWPhotoStakesProcessor
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
from bw_large_stakes import BWLargeStakesProcessor
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
from coloured_large_photo_stakes import ColouredLargePhotoStakesProcessor
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
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
                            self.setText('Please drop .txt files!')
                    event.ignore()

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.setFont(QFont('Arial', 14))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.setStyleSheet('border: 2px dashed #aaa; padding: 40px; background: #fafafa;')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.setAcceptDrops(True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.dropped_file = None
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
                    event.ignore()
            event.acceptProposedAction()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            event.ignore()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def dropEvent(self, event: QDropEvent):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if event.mimeData().hasUrls():
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            urls = event.mimeData().urls()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            txt_files = [u.toLocalFile() for u in urls if u.toLocalFile().lower().endswith('.txt')]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if txt_files:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                file_names = '\n'.join([os.path.basename(f) for f in txt_files])
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.setText(f'Files selected:\n{file_names}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.dropped_file = txt_files
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.file_dropped.emit(txt_files)  # Emit all file paths as a list
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.setText('Please drop .txt files!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            event.ignore()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
class MainWindow(QMainWindow):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def __init__(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        super().__init__()
        central_widget = QWidget()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.setCentralWidget(central_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_vlayout = QVBoxLayout(central_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # --- Left pane: DropZone and Process Orders button ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_widget = QWidget()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_layout = QVBoxLayout(left_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_layout.setContentsMargins(4, 4, 4, 4)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_layout.setSpacing(8)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.drop_zone = DropZone(self)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.drop_zone.setFont(QFont('Arial', 10))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.drop_zone.setStyleSheet('border: 2px dashed #aaa; padding: 12px; background: #fafafa;')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.drop_zone.setFixedWidth(180)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_layout.addWidget(self.drop_zone)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.drop_zone.file_dropped.connect(self.on_file_dropped)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.process_button = QPushButton('Process')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.process_button.setFixedWidth(120)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.process_button.setEnabled(False)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.process_button.clicked.connect(self.process_orders)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_layout.addWidget(self.process_button)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Add Create SVGs button (combined)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.create_svgs_button = QPushButton('Create SVGs')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.create_svgs_button.setFixedWidth(120)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.create_svgs_button.setEnabled(True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.create_svgs_button.clicked.connect(self.create_all_svgs)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_layout.addWidget(self.create_svgs_button)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        left_layout.addStretch(1)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # --- Center pane: Table and controls ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        center_widget = QWidget()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        center_layout = QVBoxLayout(center_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        center_layout.setContentsMargins(0, 0, 0, 0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        center_layout.setSpacing(6)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # --- New control bar ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        control_bar = QHBoxLayout()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.clear_button = QPushButton('Clear Table')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.clear_button.clicked.connect(self.clear_table)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        control_bar.addWidget(self.clear_button)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.export_csv_button = QPushButton('Export as CSV')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.export_csv_button.clicked.connect(self.export_table_csv)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        control_bar.addWidget(self.export_csv_button)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.export_txt_button = QPushButton('Export as TXT')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.export_txt_button.clicked.connect(self.export_table_txt)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        control_bar.addWidget(self.export_txt_button)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.open_output_button = QPushButton('Open Output Folder')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.open_output_button.clicked.connect(self.open_output_folder)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        control_bar.addWidget(self.open_output_button)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.warnings_only_checkbox = QCheckBox('Show Only Warnings')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.warnings_only_checkbox.stateChanged.connect(self.filter_table)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        control_bar.addWidget(self.warnings_only_checkbox)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.search_box = QLineEdit()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.search_box.setPlaceholderText('Search orders...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.search_box.textChanged.connect(self.filter_table)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        control_bar.addWidget(self.search_box)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        center_layout.addLayout(control_bar)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Table widget (center)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table = QTableWidget()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setColumnCount(0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setRowCount(0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.verticalHeader().setVisible(False)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.horizontalHeader().setStretchLastSection(True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.itemSelectionChanged.connect(self.update_preview_pane)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        center_layout.addWidget(self.table)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # --- Right pane: Output SVG/CSV file list ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        preview_widget = QWidget()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        preview_layout = QVBoxLayout(preview_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        preview_layout.setContentsMargins(0, 0, 0, 0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        preview_layout.setSpacing(4)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.preview_label = QLabel('Output SVG and CSV Files')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.file_links_browser = QTextBrowser()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.file_links_browser.setOpenLinks(False)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.file_links_browser.anchorClicked.connect(self.open_output_file)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        preview_layout.addWidget(self.file_links_browser)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # --- Main horizontal splitter: left (drag/drop), center (table/controls), right (preview) ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_splitter = QSplitter()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_splitter.setOrientation(Qt.Horizontal)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_splitter.addWidget(left_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_splitter.addWidget(center_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_splitter.addWidget(preview_widget)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_splitter.setSizes([180, 600, 400])
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_vlayout.addWidget(main_splitter, stretch=1)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Copy to Clipboard button
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.copy_button = QPushButton('Copy to Clipboard')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.copy_button.setEnabled(False)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.copy_button.clicked.connect(self.copy_table_to_clipboard)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_vlayout.addWidget(self.copy_button)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Log/terminal output at the bottom
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.log_output = QTextEdit()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.log_output.setReadOnly(True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.log_output.setFont(QFont('Consolas', 10))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        main_vlayout.addWidget(self.log_output)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.selected_files = None
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.last_df = None  # Store the last loaded DataFrame
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def on_file_dropped(self, file_path):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Support multiple files (comma-separated or list)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if isinstance(file_path, list):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.selected_files = file_path
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        elif isinstance(file_path, str) and ',' in file_path:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.selected_files = [f.strip() for f in file_path.split(',')]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.selected_files = [file_path]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.process_button.setEnabled(True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.log(f'Files dropped: {self.selected_files}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def process_orders(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if not hasattr(self, 'selected_files') or not self.selected_files:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('No files selected!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            return
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.log(f'Processing files: {self.selected_files}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        try:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            import os
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            import sys
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            pipeline_dir = os.path.join(os.path.dirname(__file__), "001 AMAZON DATA DOWNLOAD")
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if pipeline_dir not in sys.path:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                sys.path.insert(0, pipeline_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            import order_pipeline
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # Use the directory of the first file for outputs
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            images_dir = os.path.join(os.path.dirname(self.selected_files[0]), "004 IMAGES")
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            output_dir = os.path.join(os.path.dirname(self.selected_files[0]), "SVG_OUTPUT")
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            os.makedirs(images_dir, exist_ok=True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            os.makedirs(output_dir, exist_ok=True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Processing Amazon order files ({len(self.selected_files)}), downloading images, parsing XML...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            skulist_path = r"G:/My Drive/003 APPS/002 AmazonSeller/001 AMAZON DATA DOWNLOAD/SKULIST.csv"
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            df = order_pipeline.process_amazon_orders(self.selected_files, images_dir, output_dir, skulist_path=skulist_path)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.last_df = df  # Store for copy-to-clipboard
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.populate_table(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.copy_button.setEnabled(True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Order processing complete. {len(df)} orders processed. Images saved to 004 IMAGES.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        except Exception as e:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            import traceback
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            tb = traceback.format_exc()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Error during processing:\n{tb}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def populate_table(self, df):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.clear()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setRowCount(0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setColumnCount(0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if df is None or df.empty:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.last_df = None
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            return
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Store full DataFrame for filtering
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.last_df = df.copy()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.filtered_df = df.copy()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Enable table editing
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Connect cellChanged to update DataFrame
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.cellChanged.connect(self.on_table_cell_changed)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self._render_table(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def _render_table(self, df):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Reorder columns so DecorationType is immediately after Colour
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        columns = list(df.columns)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if 'DecorationType' in columns and 'Colour' in columns:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            columns.remove('DecorationType')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            colour_idx = columns.index('Colour')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            columns.insert(colour_idx + 1, 'DecorationType')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            df = df[columns]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        elif 'decorationtype' in columns and 'colour' in columns:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            columns.remove('decorationtype')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            colour_idx = columns.index('colour')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            columns.insert(colour_idx + 1, 'decorationtype')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            df = df[columns]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setRowCount(len(df))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setColumnCount(len(df.columns))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setHorizontalHeaderLabels(df.columns)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.blockSignals(True)  # Prevent cellChanged from firing during setup
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        for row in range(len(df)):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            for col in range(len(df.columns)):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                item = QTableWidgetItem(str(df.iat[row, col]))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.table.setItem(row, col, item)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.blockSignals(False)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.resizeColumnsToContents()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def clear_table(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.clear()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setRowCount(0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.table.setColumnCount(0)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.last_df = None
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.filtered_df = None
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.log('Table cleared.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def export_table_csv(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if self.filtered_df is not None and not self.filtered_df.empty:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as CSV', '', 'CSV Files (*.csv)')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if path:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.filtered_df.to_csv(path, index=False, encoding='utf-8-sig')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.log(f'Table exported as CSV: {path}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('No data to export.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def export_table_txt(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if self.filtered_df is not None and not self.filtered_df.empty:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            path, _ = QFileDialog.getSaveFileName(self, 'Save Table as TXT', '', 'Text Files (*.txt)')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if path:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.filtered_df.to_csv(path, sep='\t', index=False, encoding='utf-8')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.log(f'Table exported as TXT: {path}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('No data to export.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def open_output_folder(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if self.selected_files and len(self.selected_files) > 0:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            folder = os.path.join(os.path.dirname(self.selected_files[0]), "SVG_OUTPUT")
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if os.path.exists(folder):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                import subprocess
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                subprocess.Popen(['start', '', folder], shell=True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.log(f'Opened output folder: {folder}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                self.log('Output folder does not exist.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('No output folder to open.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def filter_table(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if self.last_df is None:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            return
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        df = self.last_df.copy()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Filter by warnings
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if self.warnings_only_checkbox.isChecked():
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            df = df[df['Warnings'].astype(str).str.strip() != '']
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Filter by search
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        search = self.search_box.text().strip().lower()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if search:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            df = df[df.apply(lambda row: search in ' '.join(map(str, row.values)).lower(), axis=1)]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.filtered_df = df
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self._render_table(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def copy_table_to_clipboard(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if self.filtered_df is not None and not self.filtered_df.empty:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            text = self.filtered_df.to_csv(sep='\t', index=False)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            QApplication.clipboard().setText(text)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('Order data copied to clipboard! Paste into Google Sheets (Ctrl+V).')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('No data to copy.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def update_preview_pane(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # No-op: preview pane now lists output SVG/CSV files instead of per-row preview
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        pass
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def open_output_file(self, url):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        import subprocess
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        path = url.toLocalFile()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if os.path.exists(path):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            subprocess.Popen(['start', '', path], shell=True)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'File not found: {path}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
        # Always refresh the file list to prevent navigation away from the list
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Find the output directory from the file path
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        output_dir = os.path.dirname(path)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.list_output_files(output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def list_output_files(self, output_dir):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # List SVGs and their CSVs as hyperlinks in the right pane
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        from PyQt5.QtCore import QUrl
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        svg_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.svg')]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        svg_files.sort()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        html = '''<style>
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        a { color: #1976d2; text-decoration: underline; cursor: pointer; }
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        a:hover { color: #0d47a1; }
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        table { border-collapse: collapse; margin-top: 8px; }
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        th, td { border: 1px solid #ddd; padding: 6px 12px; text-align: left; }
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        th { background: #f5f5f5; }
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        </style>
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        <b>SVG and CSV Outputs:</b><br>
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        <table>
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            <tr><th>SVGs</th><th>CSVs</th></tr>'''
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        for svg in svg_files:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            svg_path = os.path.abspath(os.path.join(output_dir, svg))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            csv_path = os.path.splitext(svg_path)[0] + '.csv'
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            svg_link = f'<a href="file:///{svg_path}" title="Open SVG in your vector graphics software">{os.path.basename(svg_path)}</a>'
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if os.path.exists(csv_path):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                csv_link = f'<a href="file:///{csv_path}" title="Open CSV in your spreadsheet software">{os.path.basename(csv_path)}</a>'
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                csv_link = ''
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            html += f'<tr><td>{svg_link}</td><td>{csv_link}</td></tr>'
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        html += '</table>'
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.file_links_browser.setHtml(html)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def on_table_cell_changed(self, row, column):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Update the filtered DataFrame when a cell is edited
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        new_value = self.table.item(row, column).text()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        col_name = self.table.horizontalHeaderItem(column).text()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Update the DataFrame in place
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if self.filtered_df is not None:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.filtered_df.iat[row, column] = new_value
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Optionally, update self.last_df as well if you want edits to persist through filtering
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
    def create_all_svgs(self):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Use the currently filtered DataFrame
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if getattr(self, 'filtered_df', None) is None or self.filtered_df.empty:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('No data to generate SVGs.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            return
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        df = self.filtered_df.copy()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Prompt for output directory ONCE
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if not output_dir:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('SVG generation cancelled (no output directory selected).')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            return
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        # Use this output_dir for all processors
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        graphics_path = r'G:/My Drive/003 APPS/002 AmazonSeller/005 Assets/001 Graphics'
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        if not os.path.exists(graphics_path):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Graphics folder not found at {graphics_path}. Defaulting to home directory.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            graphics_path = str(Path.home())
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        try:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # --- Regular SVGs ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Generating Regular SVGs in {output_dir} using graphics from {graphics_path}...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor = RegularStakesProcessor(graphics_path, output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor.process_orders(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # --- Update table with SVG paths ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            svg_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.svg')]
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            svg_files.sort()  # rely on batch order
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            image_paths = [''] * len(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            batch_size = 9
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            for i, svg_file in enumerate(svg_files):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                svg_path = os.path.join(output_dir, svg_file)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                for j in range(batch_size):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                    idx = i * batch_size + j
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                    if idx < len(df):
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
                        image_paths[idx] = svg_path
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # df['image_path'] = image_paths  # BUG: Do not overwrite image_path, this field should always point to the photo JPG for photo stakes
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.filtered_df = df
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self._render_table(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            sample_paths = df['image_path'].head(10).tolist()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('First 10 SVG image_path values: ' + str(sample_paths))
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('Regular SVG generation complete!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # --- B&W SVGs ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Generating B&W SVGs in {output_dir} using graphics from {graphics_path}...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor = BWStakesProcessor(graphics_path, output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor.process_orders(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('B&W SVG generation complete!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # --- Photo SVGs ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Generating Photo SVGs in {output_dir} using graphics from {graphics_path}...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor = PhotoStakesProcessor(graphics_path, output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor.process_orders(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('Photo SVG generation complete!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # --- B&W Large Stakes SVGs ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Generating B&W Large Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor = BWLargeStakesProcessor(graphics_path, output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor.process_orders(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('B&W Large Stakes SVG generation complete!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # --- Coloured Large Photo Stakes SVGs ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Generating Coloured Large Photo Stakes SVGs in {output_dir} using graphics from {graphics_path}...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor = ColouredLargePhotoStakesProcessor(graphics_path, output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('Calling ColouredLargePhotoStakesProcessor.process_orders...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            processor.process_orders(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('Coloured Large Photo Stakes SVG generation complete!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # --- B&W Regular Photo Stakes SVGs ---
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('Calling BWPhotoStakesProcessor.process_orders...')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            bw_photo_processor = BWPhotoStakesProcessor(graphics_path, output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            bw_photo_processor.process_orders(df)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log('B&W Regular Photo Stakes SVG generation complete!')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            # Optionally, check eligible rows (requires processor to expose count or print output to log)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        except Exception as e:
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            import traceback
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            tb = traceback.format_exc()
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
            self.log(f'Error during SVG generation (Regular or B&W):\n{tb}')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.list_output_files(output_dir)
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
        self.log('All SVG file links updated.')
if __name__ == "__main__":
    import sys
    try:
        print("Starting GUI main block")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception in main block:", e)
        traceback.print_exc()
        input("Press Enter to exit...")

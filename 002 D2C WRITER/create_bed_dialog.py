import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QSpinBox, QMessageBox, QDoubleSpinBox, QComboBox
)

class CreateBedDialog(QDialog):
    def __init__(self, assets_dir, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Bed Layout")
        self.assets_dir = assets_dir
        self.selected_svg = None
        layout = QVBoxLayout()

        # Bed size
        bed_layout = QHBoxLayout()
        bed_layout.addWidget(QLabel("Bed Width (mm):"))
        self.bed_width = QDoubleSpinBox()
        self.bed_width.setRange(10, 2000)
        self.bed_width.setValue(480)
        bed_layout.addWidget(self.bed_width)
        bed_layout.addWidget(QLabel("Bed Height (mm):"))
        self.bed_height = QDoubleSpinBox()
        self.bed_height.setRange(10, 2000)
        self.bed_height.setValue(290)
        bed_layout.addWidget(self.bed_height)
        layout.addLayout(bed_layout)

        # Grid config
        grid_layout = QHBoxLayout()
        grid_layout.addWidget(QLabel("Columns:"))
        self.grid_cols = QSpinBox()
        self.grid_cols.setRange(1, 20)
        self.grid_cols.setValue(3)
        grid_layout.addWidget(self.grid_cols)
        grid_layout.addWidget(QLabel("Rows:"))
        self.grid_rows = QSpinBox()
        self.grid_rows.setRange(1, 20)
        self.grid_rows.setValue(3)
        grid_layout.addWidget(self.grid_rows)
        layout.addLayout(grid_layout)

        # Part SVG selection
        part_layout = QHBoxLayout()
        part_layout.addWidget(QLabel("Part SVG:"))
        self.part_combo = QComboBox()
        self.populate_svg_parts()
        part_layout.addWidget(self.part_combo)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_svg)
        part_layout.addWidget(browse_btn)
        layout.addLayout(part_layout)

        # Part size
        part_size_layout = QHBoxLayout()
        part_size_layout.addWidget(QLabel("Part Width (mm):"))
        self.part_width = QDoubleSpinBox()
        self.part_width.setRange(1, 1000)
        self.part_width.setValue(108)
        part_size_layout.addWidget(self.part_width)
        part_size_layout.addWidget(QLabel("Part Height (mm):"))
        self.part_height = QDoubleSpinBox()
        self.part_height.setRange(1, 1000)
        self.part_height.setValue(75)
        part_size_layout.addWidget(self.part_height)
        layout.addLayout(part_size_layout)

        # Spacing
        spacing_layout = QHBoxLayout()
        spacing_layout.addWidget(QLabel("Spacing X (mm):"))
        self.spacing_x = QDoubleSpinBox()
        self.spacing_x.setRange(0, 1000)
        self.spacing_x.setValue(0)
        spacing_layout.addWidget(self.spacing_x)
        spacing_layout.addWidget(QLabel("Spacing Y (mm):"))
        self.spacing_y = QDoubleSpinBox()
        self.spacing_y.setRange(0, 1000)
        self.spacing_y.setValue(0)
        spacing_layout.addWidget(self.spacing_y)
        layout.addLayout(spacing_layout)

        # Ok/Cancel
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Create Bed")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def populate_svg_parts(self):
        self.part_combo.clear()
        svg_files = [f for f in os.listdir(self.assets_dir) if f.lower().endswith('.svg')]
        self.part_combo.addItems(svg_files)
        if svg_files:
            self.selected_svg = os.path.join(self.assets_dir, svg_files[0])
        self.part_combo.currentIndexChanged.connect(self.update_selected_svg)

    def update_selected_svg(self, idx):
        svg_files = [f for f in os.listdir(self.assets_dir) if f.lower().endswith('.svg')]
        if 0 <= idx < len(svg_files):
            self.selected_svg = os.path.join(self.assets_dir, svg_files[idx])

    def browse_svg(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select SVG Part", self.assets_dir, "SVG Files (*.svg)")
        if fname:
            self.selected_svg = fname
            self.part_combo.addItem(os.path.basename(fname))
            self.part_combo.setCurrentText(os.path.basename(fname))

    def get_bed_config(self):
        return {
            'bed_width_mm': self.bed_width.value(),
            'bed_height_mm': self.bed_height.value(),
            'grid_cols': self.grid_cols.value(),
            'grid_rows': self.grid_rows.value(),
            'part_svg_path': self.selected_svg,
            'part_width_mm': self.part_width.value(),
            'part_height_mm': self.part_height.value(),
            'spacing_x_mm': self.spacing_x.value(),
            'spacing_y_mm': self.spacing_y.value()
        }

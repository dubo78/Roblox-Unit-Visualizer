import sys
import platform
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QSystemTrayIcon, QMenu, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, QSize, QRect, QPoint
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QPainter, QRegion, QPainterPath, QPixmap

# Unit data from K (10^3) to Vg (10^63) - Total 21 units
UNIT_DATA = [
    ("K", "Thousand", "3"), ("M", "Million", "6"), ("B", "Billion", "9"),
    ("T", "Trillion", "12"), ("Qa", "Quadrillion", "15"), ("Qi", "Quintillion", "18"),
    ("Sx", "Sextillion", "21"), ("Sp", "Septillion", "24"), ("Oc", "Octillion", "27"),
    ("No", "Nonillion", "30"), ("Dc", "Decillion", "33"), ("Ud", "Undecillion", "36"),
    ("Dd", "Duodecillion", "39"), ("Td", "Tredecillion", "42"), ("Qad", "Quattuordecillion", "45"),
    ("Qid", "Quindecillion", "48"), ("Sxd", "Sexdecillion", "51"), ("Spd", "Septendecillion", "54"),
    ("Ocd", "Octodecillion", "57"), ("Nod", "Novemdecillion", "60"), ("Vg", "Vigintillion", "63"),
]

class RoundedWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainFrame")
        self.setStyleSheet("""
            #MainFrame {
                background-color: #F5FFFA;
                border-radius: 16px;
                border: 2px solid #D1E1D1;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 16, 16)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.parentWidget().setMask(region)

class UnitBadge(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(54, 28) # Slightly wider for 7 columns
        self.setStyleSheet("""
            QLabel {
                background-color: #E0EEE0;
                color: #2F4F4F;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #C1D1C1;
            }
        """)

class PopupWindow(QWidget):
    def __init__(self, tray_icon):
        super().__init__()
        self.tray_icon = tray_icon
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = RoundedWidget(self)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 12, 15, 15)
        self.container_layout.setSpacing(0)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.container)

        # --- Top Section (Dashboard Style: 7 cols x 3 rows) ---
        self.top_section = QWidget()
        self.top_section.setFixedHeight(190) # Shorter height because only 3 rows
        self.top_layout = QVBoxLayout(self.top_section)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)
        
        # 1. Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Roblox Unit Visualizer")
        title_font = QFont(".AppleSystemUIFont" if platform.system() == "Darwin" else "Segoe UI Variable Display", 13, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #2F4F4F;")
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("QPushButton { border: none; color: #2F4F4F; font-size: 14px; font-weight: bold; } QPushButton:hover { color: #FF4500; }")
        self.close_btn.clicked.connect(self.hide)
        
        header_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.top_layout.addLayout(header_layout)
        self.top_layout.addSpacing(10)

        # 2. Grid (7 columns x 3 rows)
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(6)
        for i, unit in enumerate(UNIT_DATA):
            badge = UnitBadge(unit[0])
            # 7 columns layout
            self.grid_layout.addWidget(badge, i // 7, i % 7)
            
        self.grid_container.setFixedHeight(105) 
        self.top_layout.addWidget(self.grid_container)
        self.top_layout.addSpacing(12)

        # 3. Toggle Button
        self.toggle_btn = QPushButton("Show Detailed Table v")
        self.toggle_btn.setFixedHeight(32)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #D1E1D1;
                background-color: white;
                color: #556B2F;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #F0FFF0; border: 1px solid #B1C1B1; }
        """)
        self.toggle_btn.clicked.connect(self.toggle_table)
        self.top_layout.addWidget(self.toggle_btn)
        
        self.container_layout.addWidget(self.top_section)

        # --- Bottom Section ---
        self.table_spacer = QWidget()
        self.table_spacer.setFixedHeight(15)
        self.table_spacer.hide()
        self.container_layout.addWidget(self.table_spacer)

        self.table = QTableWidget(len(UNIT_DATA), 3)
        self.table.setHorizontalHeaderLabels(["Sym", "Full Name", "Zeros"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background-color: transparent; border: none; gridline-color: #D1E1D1; color: #2F4F4F; font-size: 11px; }
            QHeaderView::section { background-color: #E0EEE0; color: #2F4F4F; border: 1px solid #D1E1D1; padding: 6px; font-weight: bold; }
        """)
        for i, (sym, name, zeros) in enumerate(UNIT_DATA):
            self.table.setItem(i, 0, QTableWidgetItem(sym))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(zeros))
            for j in range(3):
                item = self.table.item(i, j)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QColor("#2F4F4F"))

        self.table.hide()
        self.container_layout.addWidget(self.table)
        
        # New Dashboard Width: 450px, Initial Height: 220px
        self.setFixedSize(450, 220)

    def toggle_table(self):
        if self.table.isHidden():
            self.table.show()
            self.table_spacer.show()
            self.toggle_btn.setText("Hide Detailed Table ^")
            self.setFixedSize(450, 520)
        else:
            self.table.hide()
            self.table_spacer.hide()
            self.toggle_btn.setText("Show Detailed Table v")
            self.setFixedSize(450, 220)

    def reposition(self):
        screen_geo = QApplication.primaryScreen().availableGeometry()
        tray_geo = self.tray_icon.geometry()
        popup_size = self.size()
        
        if platform.system() == "Darwin":
            x = screen_geo.right() - popup_size.width() - 20
            y = screen_geo.top() + 10
        else:
            if tray_geo.isValid():
                x = tray_geo.center().x() - (popup_size.width() // 2)
                y = tray_geo.top() - popup_size.height() - 10
            else:
                x = screen_geo.right() - popup_size.width() - 20
                y = screen_geo.bottom() - popup_size.height() - 20
        
        x = max(screen_geo.left() + 5, min(x, screen_geo.right() - popup_size.width() - 5))
        y = max(screen_geo.top() + 5, min(y, screen_geo.bottom() - popup_size.height() - 5))
        self.move(x, y)

class TrayApp(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip("Roblox Unit Visualizer")
        self.popup = PopupWindow(self)
        self.activated.connect(self.on_activated)
        
        self.menu = QMenu()
        self.exit_action = self.menu.addAction("Exit App")
        self.exit_action.triggered.connect(QApplication.instance().quit)
        self.setContextMenu(self.menu)

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.popup.isVisible():
                self.popup.hide()
            else:
                self.popup.reposition()
                self.popup.show()
                self.popup.raise_()
                self.popup.activateWindow()

def create_fallback_icon():
    """Creates a much larger and clearer 'U' icon for the tray/menubar."""
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Fill the circle more (smaller margin = 2px instead of 4px)
    painter.setBrush(QColor("#2F4F4F"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(2, 2, 60, 60)
    
    # Larger, bolder font
    font = QFont("Arial", 40, QFont.Weight.Black)
    painter.setFont(font)
    painter.setPen(QColor("white"))
    # Adjust Y offset for better centering of 'U'
    painter.drawText(pixmap.rect().adjusted(0, 0, 0, -2), Qt.AlignmentFlag.AlignCenter, "U")
    painter.end()
    return QIcon(pixmap)

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    icon_path = "icon.png"
    icon = QIcon(icon_path)
    if icon.isNull():
        icon = create_fallback_icon()
    tray = TrayApp(icon)
    tray.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

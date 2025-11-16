import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDesktopWidget

from preview_panel import PreviewPanel
from widgets import Partition


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Content Manager")

        screen_geometry = QDesktopWidget().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.showMaximized()

        central = QWidget()
        self.setCentralWidget(central)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create the top bar
        top = Partition("#999999")
        top.add_widget(QLabel("Top Bar Content"))
        layout.addWidget(top, 0, 0, 1, 3)

        # Create the list menu
        left = Partition("#AAAAAA")
        layout.addWidget(left, 1, 0)

        # Create the selector menu
        middle = Partition("#676767")
        layout.addWidget(middle, 1, 1)

        # Create the preview panel
        preview_panel = PreviewPanel("#333333")
        layout.addWidget(preview_panel, 1, 2)

        # Stretch factors for columns and rows:
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 9)

        # Setting column stretch to enforce the width percentages:
        layout.setColumnStretch(0, 25)
        layout.setColumnStretch(1, 45)
        layout.setColumnStretch(2, 30)

        central.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

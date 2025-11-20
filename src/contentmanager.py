import argparse
import random
import sys
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDesktopWidget

from browser_panel import BrowserPanel
from handler import Media, load_media_from_json
from preview_panel import PreviewPanel
from selector_panel import SelectorPanel
from widgets import Partition


class MainWindow(QMainWindow):
    def __init__(self, media):
        super().__init__()
        self.media = media
        self.filtered_media = []
        self.media.sort(key=lambda m: m.title)
        self.setWindowTitle("Content Manager")

        screen_geometry = QDesktopWidget().availableGeometry()
        self.min_width = int(screen_geometry.width())
        self.min_height = int(screen_geometry.height())
        self.setMinimumSize(self.min_width, self.min_height)
        self.showFullScreen()

        self.font_multiplier = self.min_width / 1280

        self.selected_media = self.media[0]

        central = QWidget()
        self.setCentralWidget(central)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create the top bar
        top = Partition("#141414")
        top.add_widget(QLabel(""))
        top.setMinimumSize(1, int(self.min_height / 8))
        top.setMaximumSize(self.min_width, int(self.min_height / 8))
        layout.addWidget(top, 0, 0, 1, 3)

        # Create a new bar below the top bar
        bottom_bar = Partition("#333333")
        bottom_bar.add_widget(QLabel(""))
        bottom_bar.setMinimumSize(1, int(self.min_height / 12))
        bottom_bar.setMaximumSize(self.min_width, int(self.min_height / 12))
        layout.addWidget(bottom_bar, 1, 0, 1, 3)

        # Create the list menu
        left = BrowserPanel(self, "#222222")
        layout.addWidget(left, 2, 0)

        # Create the selector menu
        self.selector_panel = SelectorPanel(self, "#292929")
        layout.addWidget(self.selector_panel, 2, 1)

        # Create the preview panel
        self.preview_panel = PreviewPanel(self, "#252525", self.selected_media)
        layout.addWidget(self.preview_panel, 2, 2)

        # Stretch factors for columns and rows:
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 8)

        # Setting column stretch to enforce the width percentages:
        layout.setColumnStretch(0, 20)
        layout.setColumnStretch(1, 45)
        layout.setColumnStretch(2, 35)
        central.setLayout(layout)

        QTimer.singleShot(0, lambda: self.filter_media('all', 'all'))

    def filter_media(self, item, filter):
        self.filtered_media = [med for med in self.media]

        if filter == 'cast':
            self.filtered_media = [med for med in self.filtered_media if item in med.cast]

        if item == 'All':
            self.filtered_media = [med for med in self.media]

        self.selector_panel.populate_selector()

    def shuffle(self):
        """
        Removes current selection from filtered media list and picks new random media item.
        """
        shuffle_media = self.filtered_media.copy()

        if self.selected_media in shuffle_media:
            shuffle_media.remove(self.selected_media)

        if len(shuffle_media) > 0:
            self.selected_media = random.choice(shuffle_media)

        self.preview_panel.update_panel(self.selected_media)

    def select_previous(self):
        """
        Selects media item left of current selection from filtered media list
        """
        current_index = self.media.index(self.selected_media)
        self.selected_media = self.filtered_media[(current_index - 1) % len(self.filtered_media)]
        self.preview_panel.update_panel(self.selected_media)

    def select_media(self, index):
        """
        Changes currently selected media item
        """
        self.selected_media = [med for med in self.media if med.code == index][0]
        self.preview_panel.update_panel(self.selected_media)

    def select_next(self):
        """
        Selects media item right of current selection from filtered media list
        """
        current_index = self.media.index(self.selected_media)
        self.selected_media = self.filtered_media[(current_index + 1) % len(self.filtered_media)]
        self.preview_panel.update_panel(self.selected_media)

    def resizeEvent(self, event):
        super().resizeEvent(event)


def main():
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j', '--json_path', type=str, required=True)
    args = parser.parse_args()
    media = load_media_from_json(args.json_path)

    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    win = MainWindow(media)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

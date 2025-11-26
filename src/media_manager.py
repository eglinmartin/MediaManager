import argparse
import os
import random
import shutil
import sys

from datetime import datetime
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QPushButton, QLineEdit, QFileDialog, QComboBox

from browser_panel import BrowserPanel
from constants import Colours
from handler import Media, insert_row, load_media_from_json, update_db
from preview_panel import PreviewPanel
from selector_panel import SelectorPanel


class TopBar(QWidget):
    def __init__(self, player):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Colours.GREY1.value))
        self.setPalette(palette)

        self.top_font = QFont("Bahnschrift Semibold", int(36 / player.screen_scale))

        # Set size
        self.setMinimumSize(1, int(player.min_height / 8))
        self.setMaximumSize(player.min_width, int(player.min_height / 8))

        # --- Layout ---
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # --- Title label ---
        self.title_label = QLabel(f"Media Manager | {player.library_name}")
        self.title_label.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.GREY1.value}")
        self.title_label.setFont(self.top_font)
        layout.addWidget(self.title_label)

        layout.addStretch()

        # Current time
        self.time_label = QLabel()
        self.time_label.setFont(self.top_font)
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.update_time()
        self.time_label.setStyleSheet(f"color: {Colours.WHITE.value};")

        layout.addWidget(self.time_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        layout.addSpacing(20)

        # --- Minimize button ---
        self.minimize_button = QPushButton("—")
        self.minimize_button.setFont(self.top_font)
        self.minimize_button.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.GREY3.value};")
        self.minimize_button.setCursor(Qt.PointingHandCursor)
        self.minimize_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.minimize_button.clicked.connect(lambda: self.window().showMinimized())
        layout.addWidget(self.minimize_button)

        # --- Exit button ---
        self.exit_button = QPushButton("✕")
        self.exit_button.setFont(self.top_font)
        self.exit_button.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.RED.value};")
        self.exit_button.setCursor(Qt.PointingHandCursor)
        self.exit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exit_button.clicked.connect(QApplication.quit)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def update_time(self):
        self.time_label.setText(datetime.now().strftime("%H:%M"))

    def resizeEvent(self, event):
        self.minimize_button.setFixedSize(self.minimize_button.height(), self.minimize_button.height())
        self.time_label.setFixedWidth(int(self.minimize_button.width() * 2))
        self.exit_button.setFixedSize(self.exit_button.height(), self.exit_button.height())
        super().resizeEvent(event)


class BottomBar(QWidget):
    def __init__(self, player):
        super().__init__()
        self.setMinimumSize(1, int(player.min_height / 12))
        self.setMaximumSize(player.min_width, int(player.min_height / 12))
        self.player = player
        self.bottom_bar_font = QFont("Bahnschrift Semibold", int(24 / player.screen_scale))

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Colours.GREY5.value))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.combobox_browse = QComboBox()
        self.combobox_browse.setFont(self.bottom_bar_font)
        self.combobox_browse.setStyleSheet(f"""
             QComboBox {{color: {Colours.WHITE.value}; background-color: {Colours.GREY6.value}; selection-background-color: transparent; padding-left: 10px;}}
             QComboBox:hover {{color: {Colours.RED.value};}}
             QComboBox:drop-down {{border: none; color: {Colours.RED.value};}}
             QComboBox QAbstractItemView {{background-color: {Colours.GREY6.value}; color: {Colours.WHITE.value}; selection-background-color: transparent; selection-color: {Colours.RED.value};}}
             QComboBox::down-arrow {{color: {Colours.WHITE.value};}}
             """)
        self.combobox_browse.setCursor(Qt.PointingHandCursor)
        self.combobox_browse.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combobox_browse.currentTextChanged.connect(self.player.browser_panel.update_listbox)

        # list_options = ['Directors', 'Cast', 'Tags']
        list_options = ['Directors', 'Cast']
        for list_option in list_options:
            self.combobox_browse.addItem(list_option)
        layout.addWidget(self.combobox_browse)

        self.button_sort_browser = QPushButton('A-z')
        self.button_sort_browser.setFont(self.bottom_bar_font)
        self.button_sort_browser.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.GREY6.value};")
        self.button_sort_browser.setCursor(Qt.PointingHandCursor)
        self.button_sort_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_sort_browser.clicked.connect(self.player.browser_panel.set_sort_type)
        layout.addWidget(self.button_sort_browser)

        layout.addSpacerItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.button_zoom = QPushButton()
        self.button_zoom.setFont(self.bottom_bar_font)
        self.button_zoom.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.GREY6.value};")
        current_zoom = self.player.selector_panel.num_columns
        self.button_zoom.setIcon(self.player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\icon_zoom_{current_zoom}"))
        self.button_zoom.setCursor(Qt.PointingHandCursor)
        self.button_zoom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_zoom.clicked.connect(self.switch_size)
        layout.addWidget(self.button_zoom)

        self.button_favourite = QPushButton('★')
        self.button_favourite.setFont(self.bottom_bar_font)
        self.button_favourite.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.YELLOW.value};")
        self.button_favourite.setCursor(Qt.PointingHandCursor)
        self.button_favourite.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_favourite.clicked.connect(player.toggle_favourites)
        layout.addWidget(self.button_favourite)

        self.button_switcher = QPushButton('')
        self.button_switcher.setFont(self.bottom_bar_font)
        self.button_switcher.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.GREY6.value};")
        self.button_switcher.setCursor(Qt.PointingHandCursor)
        self.button_switcher.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.button_switcher)

        layout.addStretch()

        self.searchbar = QLineEdit()
        self.searchbar.setStyleSheet(f"background-color: {Colours.GREY6.value}; color: {Colours.WHITE.value}; border: none; padding: 10px;")
        self.searchbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.searchbar.setFont(self.bottom_bar_font)
        self.searchbar.returnPressed.connect(player.filter_media)
        self.searchbar.setPlaceholderText('Search')
        layout.addWidget(self.searchbar)

        self.button_add = QPushButton('+')
        self.button_add.setFont(self.bottom_bar_font)
        self.button_add.setStyleSheet(f"color: {Colours.WHITE.value}; background-color: {Colours.GREEN.value};")
        self.button_add.setCursor(Qt.PointingHandCursor)
        self.button_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_add.clicked.connect(self.player.add_video)
        layout.addWidget(self.button_add)

        self.setLayout(layout)

    def switch_size(self):
        self.player.selector_panel.switch_size()
        current_zoom = self.player.selector_panel.num_columns
        self.button_zoom.setIcon(self.player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\icon_zoom_{current_zoom}"))

    def resizeEvent(self, event):
        self.button_add.setFixedSize(self.searchbar.height(), self.searchbar.height())

        self.button_sort_browser.setFixedSize(self.searchbar.height(), self.searchbar.height())
        self.combobox_browse.setFixedSize(self.player.browser_panel.list_widget.width() - 60, self.searchbar.height())

        self.searchbar.setFixedWidth(self.player.preview_panel.label_image.width() - 20 - self.button_add.width())
        self.button_switcher.setFixedSize(self.searchbar.height() * 4, self.searchbar.height())

        self.button_favourite.setFixedSize(self.searchbar.height(), self.searchbar.height())
        self.button_zoom.setFixedSize(self.searchbar.height(), self.searchbar.height())
        self.button_zoom.setIconSize(self.button_zoom.size())


class MainWindow(QMainWindow):
    def __init__(self, media, screen, library_name, db, screen_scale):
        super().__init__()
        self.media = media
        self.filtered_media = []
        self.media.sort(key=lambda m: m.title)
        self.setWindowTitle("Media Manager")
        self.library_name = library_name
        self.db_path = db
        self.screen_scale = screen_scale

        self.min_width = int(screen.size().width())
        self.min_height = int(screen.size().height())

        self.screen_scale = screen.devicePixelRatio()

        self.setMinimumSize(self.min_width, self.min_height)
        self.showFullScreen()

        self.font_multiplier = self.min_width / 1280

        self.thumb_cache = {}

        self.selected_media = self.media[0]
        self.favourites_only = False

        central = QWidget()
        self.setCentralWidget(central)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create the top bar
        self.top_bar = TopBar(self)
        layout.addWidget(self.top_bar, 0, 0, 1, 3)

        self.filter_column = 'All'
        self.filter_item = 'All'

        # Create the list menu
        self.browser_panel = BrowserPanel(self)
        layout.addWidget(self.browser_panel, 2, 0)

        # Create the selector menu
        self.selector_panel = SelectorPanel(self)
        layout.addWidget(self.selector_panel, 2, 1)

        # Create the preview panel
        self.preview_panel = PreviewPanel(self)
        layout.addWidget(self.preview_panel, 2, 2)

        # Create a new bar below the top bar
        self.bottom_bar = BottomBar(self)
        layout.addWidget(self.bottom_bar, 1, 0, 1, 3)

        # Stretch factors for columns and rows:
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 8)

        # Setting column stretch to enforce the width percentages:
        layout.setColumnStretch(0, 20)
        layout.setColumnStretch(1, 45)
        layout.setColumnStretch(2, 35)
        central.setLayout(layout)

        QTimer.singleShot(0, lambda: self.filter_media())

    def get_icon(self, path):
        if path not in self.thumb_cache:
            self.thumb_cache[path] = QIcon(path)
        return self.thumb_cache[path]

    def toggle_favourites(self):
        self.favourites_only = not self.favourites_only
        self.filter_media()

    def filter_media(self, filter_item=None, filter_column=None):
        if filter_column:
            self.filter_column = filter_column
        if filter_item:
            self.filter_item = filter_item

        self.filtered_media = [med for med in self.media]

        if self.filter_item == 'All':
            self.filtered_media = [med for med in self.media]

        else:
            if self.filter_column == 'Directors':
                self.filtered_media = [med for med in self.filtered_media if str(self.filter_item).split(' (')[0] in med.director]
            if self.filter_column == 'Cast':
                self.filtered_media = [med for med in self.filtered_media if str(self.filter_item).split(' (')[0] in med.cast]
            elif self.filter_column == 'Tags':
                self.filtered_media = [med for med in self.filtered_media if med.tags and self.filter_item in med.tags]

        if self.bottom_bar.searchbar.text():
            self.search()

        if self.favourites_only:
            self.filtered_media = [m for m in self.filtered_media if int(m.favourite)]

        self.selector_panel.populate_selector()

    def search(self):
        search_text_lower = "".join(self.bottom_bar.searchbar.text().split()).lower()

        self.filtered_media = [
            med for med in self.filtered_media
            if search_text_lower in " ".join([
                (med.title or "").lower(),
                (med.director or "").lower(),
                " ".join(med.cast or []).lower(),
                (med.tags or "").lower()
            ])
        ]

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

    def favourite_media(self):
        """
        Toggles 'favourite' attribute of selected media
        """
        self.selected_media.favourite = not bool(int(self.selected_media.favourite))
        update_db(self, column='Favourite', value=str(int(self.selected_media.favourite)))
        self.selector_panel.populate_selector()

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def add_thumbnail(self):
        src_path, _ = QFileDialog.getOpenFileName(self, "Select an image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not src_path:
            return

        code = self.selected_media.code
        dest_path = fr"C:\Storage\Programming\ContentManager_V3\thumbs\{code}"
        shutil.copyfile(src_path, dest_path)

        for button in self.selector_panel.selector_buttons:
            if button.med_item.code == code:
                button.set_icon(code)

        self.selector_panel.populate_selector()
        self.select_media(code)

    def add_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if not file_path:
            return

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_ext = os.path.splitext(os.path.basename(file_path))[1]
        code = random.randint(10000, 99999)

        insert_row(self, file_name, code)

        self.media.append(Media(
            title=file_name, director='Unknown', cast=['Unknown',], code=code,
            date=datetime.fromisoformat('1900-01-01'), media_type='Video', tags=[], favourite=False)
        )

        src_path = file_path
        dest_path = fr"{os.path.dirname(self.db_path)}\Videos\{code}{file_ext}"
        shutil.copyfile(src_path, dest_path)

        self.media.sort(key=lambda m: m.title)
        self.filter_media()
        self.selector_panel.populate_selector()
        self.select_media(code)

    def play_video(self):
        directory = fr"{os.path.dirname(self.db_path)}\Videos"
        video_fname = [p for p in os.listdir(directory) if str(self.selected_media.code) in p]

        if video_fname:
            video_path = os.path.join(directory, video_fname[0])

            if os.path.exists(video_path):
                os.startfile(video_path)


def main():
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-db', '--db_path', type=str, required=True)
    parser.add_argument('-s', '--screen_scale', type=str, required=True)
    args = parser.parse_args()
    media = load_media_from_json(args.db_path)
    library_name = os.path.basename(args.db_path)
    screen_scale = float(args.screen_scale)

    app = QApplication(sys.argv)
    screen = app.primaryScreen()

    win = MainWindow(media, screen, library_name, args.db_path, screen_scale)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

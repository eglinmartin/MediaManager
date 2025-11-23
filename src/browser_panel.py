import re

from enum import Enum
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget, QListWidget
from PyQt5.QtCore import Qt

from widgets import Partition, ImageWidget, TextWidget


class SortType(Enum):
    AtoZ = 1
    COUNT = 2


class Browser(QListWidget):
    def __init__(self, browser_panel, player, color, screen_scale):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSpacing(0)

        self.setStyleSheet("""
            QListWidget {border: none; color: #ffffff; background-color: #222222;}
            QListWidget::item {padding-top: 5px; padding-bottom: 5px;}
            QListWidget::item:selected {background-color: #1a1a1a; color: white; outline: none; border: none; color: #ff5555;}
            QListWidget::item:hover {background-color: #2a2a2a; outline: none; color: #ff5555;}
            QListView { outline: 0;}
            QScrollBar:vertical {border: 1px solid #222222; background: #292929; width: 15px; margin: 0px 0px 0px 0px;}
            QScrollBar::handle:vertical {background: #191919; min-height: 20px; border-radius: 7px;}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: none; height: 0px;}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: #222222;}
            """)

        self.browser_font = QFont("Bahnschrift Semibold", int(14 / screen_scale))
        self.setFont(self.browser_font)

        self.itemClicked.connect(lambda item: player.filter_media(item.text(), browser_panel.parameter))


class BrowserPanel(Partition):
    def __init__(self, player, colour, screen_scale):
        super().__init__(colour)
        self.setContentsMargins(16, 16, 16, 16)
        self.player = player
        self.colour = colour
        self.screen_scale = screen_scale

        self.parameter = 'Directors'
        self.sort_type = SortType.AtoZ

        self.list_widget = None
        self.update_listbox(self.parameter)

    def set_sort_type(self):
        if self.sort_type == SortType.AtoZ:
            self.sort_type = SortType.COUNT
            self.player.bottom_bar.button_sort_browser.setText('9-1')
        else:
            self.sort_type = SortType.AtoZ
            self.player.bottom_bar.button_sort_browser.setText('A-z')

        self.update_listbox(self.parameter)

    def update_listbox(self, parameter):
        if self.list_widget:
            self.layout.removeWidget(self.list_widget)
            self.list_widget.deleteLater()

        self.parameter = parameter
        self.list_widget = Browser(self, self.player, self.colour, self.screen_scale)
        unique_items = []

        if parameter == 'Directors':
            unique_items = {f'{item.director} ({len([m for m in self.player.media if item.director == m.director])})' for item in self.player.media}
        if parameter == 'Cast':
            unique_items = {f'{actor.strip()} ({len([m for m in self.player.media if actor in m.cast])})' for med in self.player.media for actor in (med.cast if med.cast else [])}
        # elif parameter == 'Tags':
        #     unique_items = {f'{tag.strip()} ({len([m for m in self.player.media if tag in m.tags])})' for med in self.player.media for tag in (med.tags.split(',') if med.tags else [])}

        if self.sort_type == SortType.AtoZ:
            sorted_items = sorted(unique_items)
        elif self.sort_type == SortType.COUNT:
            sorted_items = sorted(unique_items, key=lambda x: (-int(re.search(r'\((\d+)\)', x).group(1)), x))
        appended_items = ['All'] + sorted_items

        for item in appended_items:
            self.list_widget.addItem(item)

        self.layout.addWidget(self.list_widget)

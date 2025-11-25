import re

from enum import Enum
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QListWidget

from constants import Colours
from widgets import Partition


class SortType(Enum):
    AtoZ = 1
    COUNT = 2


class Browser(QListWidget):
    def __init__(self, browser_panel, player):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSpacing(0)
        self.screen_scale = player.screen_scale

        self.setStyleSheet(f"""
            QListWidget {{border: none; color: {Colours.WHITE.value}; background-color: {Colours.GREY3.value};}}
            QListWidget::item {{padding-top: 5px; padding-bottom: 5px;}}
            QListWidget::item:selected {{background-color: {Colours.GREY2.value}; color: {Colours.WHITE.value}; outline: none; border: none; color: {Colours.RED.value};}}
            QListWidget::item:hover {{background-color: {Colours.GREY4.value}; outline: none; color: {Colours.RED.value};}}
            QListView {{ outline: 0;}}
            QScrollBar:vertical {{border: 1px solid {Colours.GREY3.value}; background: {Colours.GREY3.value}; width: 15px; margin: 0px 0px 0px 0px;}}
            QScrollBar::handle:vertical {{background: {Colours.GREY5.value}; min-height: 20px; border-radius: 7px;}}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{background: none; height: 0px;}}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{background: {Colours.GREY3.value};}}
            """)

        self.browser_font = QFont("Bahnschrift Semibold", int(14 / player.screen_scale))
        self.setFont(self.browser_font)

        self.itemClicked.connect(lambda item: player.filter_media(item.text(), browser_panel.parameter))


class BrowserPanel(Partition):
    def __init__(self, player):
        super().__init__(Colours.GREY3.value)
        self.setContentsMargins(16, 16, 16, 16)
        self.player = player
        self.screen_scale = player.screen_scale

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
        self.list_widget = Browser(self, self.player)
        unique_items = []

        if parameter == 'Directors':
            unique_items = {f'{item.director} ({len([m for m in self.player.media if item.director == m.director])})' for item in self.player.media}
        if parameter == 'Cast':
            unique_items = {f'{actor.strip()} ({len([m for m in self.player.media if actor in m.cast])})' for med in self.player.media for actor in (med.cast if med.cast else [])}

        if self.sort_type == SortType.AtoZ:
            sorted_items = sorted(unique_items)
        elif self.sort_type == SortType.COUNT:
            sorted_items = sorted(unique_items, key=lambda x: (-int(re.search(r'\((\d+)\)', x).group(1)), x))
        appended_items = ['All'] + sorted_items

        for item in appended_items:
            self.list_widget.addItem(item)

        self.layout.addWidget(self.list_widget)

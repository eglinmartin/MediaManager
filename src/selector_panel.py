import math

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QSpacerItem, QGridLayout, \
    QLabel
from PyQt5.QtCore import Qt, QSize

from widgets import Partition, ImageWidget, TextWidget


class SelectorItem(QPushButton):
    def __init__(self, player, med_item):
        super().__init__()
        self.setStyleSheet(f"background-color: #000000")
        self.setIcon(QIcon(fr"C:\Storage\Programming\ContentManager_V3\bin\{med_item.code}"))
        self.clicked.connect(lambda: player.select_media(med_item.code))


class SelectorPanel(Partition):
    def __init__(self, player, color, media_list):
        super().__init__(color)

        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignTop)

        grid_layout = QGridLayout()

        self.selector_buttons = []
        for i, med_item in enumerate(media_list):
            button = SelectorItem(player, med_item)
            self.selector_buttons.append(button)
            grid_layout.addWidget(button, i // 3, i % 3)

        self.layout.addLayout(grid_layout)

    def resizeEvent(self, event):
        for button in self.selector_buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMaximumSize(button.width(), int(button.width()* 0.562))
            button.setIconSize(QSize(button.width(), int(button.width()* 0.562)))

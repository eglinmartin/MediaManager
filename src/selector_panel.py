import math

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QSpacerItem, QGridLayout, \
    QLabel
from PyQt5.QtCore import Qt, QSize

from widgets import Partition, ImageWidget, TextWidget


class SelectorItem(QWidget):
    def __init__(self, player, med_item):
        super().__init__()
        self.setStyleSheet(f"background-color: #292929")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_button = QPushButton()
        self.image_button.setIcon(QIcon(fr"C:\Storage\Programming\ContentManager_V3\bin\{med_item.code}"))
        self.image_button.clicked.connect(lambda: player.select_media(med_item.code))
        layout.addWidget(self.image_button, alignment=Qt.AlignTop)

        self.text_button = QLabel(med_item.title)
        self.text_button.setStyleSheet(f"color: #ffffff; text-align: left top; padding: 7px;")
        self.text_font = QFont("Bahnschrift Semibold", int(10 * player.font_multiplier))
        self.text_button.setFont(self.text_font)
        self.text_button.setWordWrap(True)

        self.text_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.text_button.setFixedHeight(int(self.image_button.width() / 4))

        self.text_button.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.text_button.setScaledContents(False)
        self.text_button.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        layout.addWidget(self.text_button, alignment=Qt.AlignTop)

    def resizeEvent(self, event):
        self.image_button.setFixedHeight(int(self.image_button.width() * 0.562))
        self.text_button.setFixedHeight(int(self.image_button.width()/4))
        self.setFixedHeight(int(self.image_button.width()/4) + int(self.image_button.height()))

        # print(int(self.image_button.width()))
        # print(int(self.image_button.height()))
        #
        # print(int(self.image_button.width() / 3))
        # print(int(self.image_button.width()/3) + int(self.image_button.height()))


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
            button.image_button.setIconSize(QSize(button.width(), int(button.width()* 0.562)))

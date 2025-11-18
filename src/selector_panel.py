import math

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QSpacerItem, QGridLayout, \
    QLabel, QScrollArea
from PyQt5.QtCore import Qt, QSize

from widgets import Partition, ImageWidget, TextWidget


class SelectorItem(QWidget):
    def __init__(self, player, med_item):
        super().__init__()
        self.setStyleSheet(f"background-color: #292929")
        # self.setStyleSheet(f"background-color: #dddddd")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_button = QPushButton()
        self.image_button.setIcon(QIcon(fr"C:\Storage\Programming\ContentManager_V3\bin\{med_item.code}"))
        self.image_button.clicked.connect(lambda: player.select_media(med_item.code))
        self.image_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.image_button, alignment=Qt.AlignTop)

        self.text_button = QLabel(med_item.title)
        self.text_button.setStyleSheet(f"color: #ffffff; text-align: left top; padding: 2px;")
        self.text_font = QFont("Bahnschrift Semibold", int(7 * player.font_multiplier))
        self.text_button.setFont(self.text_font)
        self.text_button.setWordWrap(True)

        self.text_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.text_button.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.text_button.setScaledContents(False)
        self.text_button.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        layout.addWidget(self.text_button, alignment=Qt.AlignTop)

    def resizeEvent(self, event):
        self.image_button.setFixedHeight(int(self.image_button.width() * 0.562))
        self.text_button.setFixedWidth(int(self.image_button.width()))
        self.text_button.setFixedHeight(int(self.image_button.width()/4))
        self.setFixedHeight(int(self.image_button.width()/3) + int(self.image_button.height()))


class SelectorPanel(Partition):
    def __init__(self, player, color, media_list):
        super().__init__(color)

        # self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignTop)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
            border: 1px solid #292929;
            background: #292929; /* Track background */
            width: 15px;
            margin: 0px 0px 0px 0px;
        }
            QScrollBar::handle:vertical {
            background: #191919; /* Thumb/marker */
            min-height: 20px;
            border-radius: 7px;
        }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
        }
    
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: #292929; /* the track */
        }
        """)

        # Outer container ensures content aligns to top
        outer_container = QWidget()
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.setAlignment(Qt.AlignTop)  # <- Align content to top
        outer_container.setLayout(outer_layout)

        # Inner content widget with grid layout
        content_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        content_widget.setLayout(grid_layout)

        outer_layout.addWidget(content_widget)  # Add content to top of outer container
        self.scroll_area.setWidget(outer_container)  # Set outer container as scroll widget

        self.selector_buttons = []
        for i, med_item in enumerate(media_list):
            button = SelectorItem(player, med_item)
            self.selector_buttons.append(button)
            grid_layout.addWidget(button, i // 3, i % 3)

        self.layout.addWidget(self.scroll_area)

    def resizeEvent(self, event):
        for button in self.selector_buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMaximumWidth(int(self.width() / 3) - 40)
            button.setMaximumHeight(int(button.width()* 0.562))
            button.image_button.setIconSize(QSize(button.width(), int(button.width()* 0.562)))
            button.text_button.setFixedWidth(button.image_button.width())

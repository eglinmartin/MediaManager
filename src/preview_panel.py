from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt

from widgets import Partition, ImageWidget, TextWidget


class PlayerButton(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(f'color: #ffffff;')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class PreviewPanel(Partition):
    def __init__(self, player, color, selected_media):
        super().__init__(color)

        # Create main image label
        self.label_image = ImageWidget(self, back_col='#000000', font_col='#ffffff', alignment=Qt.AlignCenter)
        self.label_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.label_image, alignment=Qt.AlignTop)

        # Create title label
        self.title_font = QFont("Bahnschrift Semibold", 16)
        self.label_title = TextWidget(self, font_col='#ffffff', font=self.title_font, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label_title, alignment=Qt.AlignTop)

        # Create director label
        self.director_font = QFont("Bahnschrift Semibold", 13)
        self.label_director = TextWidget(self, font_col='#aaaaaa', font=self.director_font, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label_director, alignment=Qt.AlignTop)

        # Create cast label
        self.cast_font = QFont("Bahnschrift Semibold", 10)
        self.label_cast = TextWidget(self, font_col='#777777', font=self.cast_font, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label_cast, alignment=Qt.AlignTop)

        # Create blank space below media metadata
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addStretch()

        # Create a horizontal layout for buttons
        self.player_menu = QWidget(self)
        self.player_menu.setStyleSheet(f"background-color : #1c1c1c")
        self.player_menu.setMinimumSize(1, 100)
        self.player_menu.setFixedHeight(int(self.width()/5.5))

        button_layout = QHBoxLayout(self.player_menu)

        button_shuffle = PlayerButton("Shuffle")
        button_shuffle.clicked.connect(player.shuffle)
        button_layout.addWidget(button_shuffle)

        button_previous = PlayerButton("Previous")
        button_previous.clicked.connect(player.select_previous)
        button_layout.addWidget(button_previous)

        button_play = PlayerButton("Play")
        button_layout.addWidget(button_play)

        button_next = PlayerButton("Next")
        button_next.clicked.connect(player.select_next)
        button_layout.addWidget(button_next)

        button_favourite = PlayerButton("Favourite")
        button_layout.addWidget(button_favourite)

        self.layout.addWidget(self.player_menu)

        self.update_panel(selected_media)

    def resizeEvent(self, event):
        self.label_image.setMaximumSize(self.label_image.width(), int(self.label_image.width()* 0.562))

    def update_panel(self, selected_media):
        self.label_title.set_text(selected_media.title)
        self.label_director.set_text(selected_media.director)
        self.label_cast.set_text(', '.join(selected_media.cast))
        self.label_image.set_image(fr"C:\Storage\Programming\ContentManager_V3\bin\{selected_media.code}")
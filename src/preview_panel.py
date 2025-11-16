from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt

from widgets import Partition, ImageWidget, TextWidget


class PreviewPanel(Partition):
    def __init__(self, color):
        super().__init__(color)

        # Create main image label
        self.label_image = ImageWidget(self, back_col='#694343', font_col='#ffffff', alignment=Qt.AlignCenter)
        self.label_image.set_image(r"C:\Storage\Programming\ContentManager_V3\bin\0")
        self.label_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.label_image, alignment=Qt.AlignTop)

        # Create title label
        self.title_font = QFont("Bahnschrift Semibold", 18)
        self.label_title = TextWidget(self, font_col='#ffffff', font=self.title_font, alignment=Qt.AlignLeft)
        self.label_title.set_text("Indiana Jones and the Raiders of the Lost Ark (1981)")
        self.layout.addWidget(self.label_title, alignment=Qt.AlignTop)

        # Create director label
        self.director_font = QFont("Bahnschrift Semibold", 16)
        self.label_director = TextWidget(self, font_col='#dddddd', font=self.director_font, alignment=Qt.AlignLeft)
        self.label_director.set_text("Steven Spielberg")
        self.layout.addWidget(self.label_director, alignment=Qt.AlignTop)

        # Create cast label
        self.cast_font = QFont("Bahnschrift Semibold", 12)
        self.label_cast = TextWidget(self, font_col='#dddddd', font=self.cast_font, alignment=Qt.AlignLeft)
        self.label_cast.set_text("Harrison Ford, Karen Allen")
        self.layout.addWidget(self.label_cast, alignment=Qt.AlignTop)

        # Create blank space below media metadata
        self.layout.addStretch()

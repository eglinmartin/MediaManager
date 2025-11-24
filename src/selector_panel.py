import math

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QGridLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from widgets import Partition


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class SelectorRow(QWidget):
    def __init__(self, player, med_item, screen_scale, create_image: bool):
        super().__init__()
        self.setStyleSheet(f"background-color: #292929")
        self.player = player
        self.med_item = med_item
        self.create_image = create_image

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create image button
        self.image_button = None
        if self.create_image:
            self.image_button = QPushButton()
            self.image_button.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\{med_item.code}"))
            self.image_button.setStyleSheet(f"border: none;")
            self.image_button.clicked.connect(lambda: player.select_media(med_item.code))
            self.image_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.image_button.setCursor(Qt.PointingHandCursor)
            layout.addWidget(self.image_button, alignment=Qt.AlignTop)

        # Create the overlay image label
        self.overlay_label = QLabel(self)

        if not med_item.tags:
            self.overlay_pixmap = QPixmap(fr"C:\Storage\Programming\ContentManager_V3\bin\overlay_notags.png")
            self.overlay_label.setPixmap(self.overlay_pixmap)

        elif int(med_item.favourite):
            self.overlay_pixmap = QPixmap(fr"C:\Storage\Programming\ContentManager_V3\bin\overlay_favourite.png")
            self.overlay_label.setPixmap(self.overlay_pixmap)
        else:
            self.overlay_pixmap = None
            self.overlay_label.setPixmap(QPixmap())

        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setStyleSheet("background: transparent;")
        self.overlay_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.overlay_label.raise_()

        self.text_font = QFont("Bahnschrift Semibold", int(14 / screen_scale))

        self.text_labels = []
        for label_text in [f"{med_item.title}", f"XX:XX", f"{med_item.director}", f"{', '.join(med_item.cast)}"]:
            label = ClickableLabel(label_text)
            label.setStyleSheet("color: #ffffff; background-color: #1d1d1d; padding-left: 5px; padding-right: 25px;")
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            label.setFont(self.text_font)
            label.setWordWrap(True)
            label.clicked.connect(lambda lt=med_item.code: self.player.select_media(lt))
            label.setCursor(Qt.PointingHandCursor)
            self.text_labels.append(label)
            layout.addWidget(label, alignment=Qt.AlignTop)

        self.text_labels[-1].setWordWrap(False)
        layout.addStretch()

        if self.image_button:
            self.image_button.enterEvent = self.button_enter
            self.image_button.leaveEvent = self.button_leave

    def button_enter(self, event):
        for label in self.text_labels:
            label.setStyleSheet("color: #ff5555; background-color: #1d1d1d; padding-left: 5px; padding-right: 25px;")

    def button_leave(self, event):
        for label in self.text_labels:
            label.setStyleSheet("color: #ffffff; background-color: #1d1d1d; padding-left: 5px; padding-right: 25px;")

    def set_icon(self, code):
        if self.image_button:
            cached_thumb = [thumb for thumb in self.player.thumb_cache if str(code) in thumb][0]
            self.player.thumb_cache.pop(cached_thumb)
            self.image_button.setIcon(self.player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\{code}"))

    def resizeEvent(self, event):
        width_offset = 0
        if self.image_button:
            width_offset = self.image_button.width()

        self.height = int(64 * self.player.screen_scale)
        if self.image_button:
            self.height = int(self.image_button.width() * 0.562)

        label_widths = [0.4, 0.15, 0.2, 0.25]
        for i, label in enumerate(self.text_labels):
            label.setFixedWidth(int((self.width() - width_offset) * label_widths[i]))
            label.setFixedHeight(self.height)
            label.enterEvent = self.button_enter
            label.leaveEvent = self.button_leave
        self.text_labels[-1].setFixedWidth(int((self.width() - width_offset) * label_widths[-1]) - 8)

        if self.image_button:
            self.image_button.setFixedHeight(self.height)
            if self.overlay_pixmap:
                self.overlay_label.setFixedSize(self.image_button.size())
                scaled_pixmap = self.overlay_pixmap.scaled(self.image_button.width(), self.image_button.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.overlay_label.setPixmap(scaled_pixmap)

        self.setFixedHeight(self.height)


class SelectorItem(QWidget):
    def __init__(self, player, med_item, screen_scale):
        super().__init__()
        self.setStyleSheet(f"background-color: #292929")
        self.player = player
        self.med_item = med_item
        self.height = int(54 / self.player.screen_scale)

        # Create vertical box
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create image button
        self.image_button = QPushButton()
        self.image_button.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\{med_item.code}"))
        self.image_button.setStyleSheet(f"border: none;")
        self.image_button.clicked.connect(lambda: player.select_media(med_item.code))
        self.image_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.image_button, alignment=Qt.AlignTop)

        # Create the overlay image label
        self.overlay_label = QLabel(self)

        if not med_item.tags:
            self.overlay_pixmap = QPixmap(fr"C:\Storage\Programming\ContentManager_V3\bin\overlay_notags.png")
            self.overlay_label.setPixmap(self.overlay_pixmap)

        elif int(med_item.favourite):
            self.overlay_pixmap = QPixmap(fr"C:\Storage\Programming\ContentManager_V3\bin\overlay_favourite.png")
            self.overlay_label.setPixmap(self.overlay_pixmap)
        else:
            self.overlay_pixmap = None
            self.overlay_label.setPixmap(QPixmap())

        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setStyleSheet("background: transparent;")
        self.overlay_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.overlay_label.raise_()

        # Create title label
        self.title_label = ClickableLabel(med_item.title)
        self.title_label.setStyleSheet("""
            QLabel {color: #ffffff; background-color: #1d1d1d; padding: 5px;}
            QLabel:hover {color: #ff5555;}
        """)
        self.title_label.clicked.connect(lambda: player.select_media(med_item.code))
        self.title_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.title_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.title_label.setCursor(Qt.PointingHandCursor)

        # Set font, font size and wrapping
        self.text_font = QFont("Bahnschrift Semibold", int(14 / screen_scale))
        self.title_label.setFont(self.text_font)
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label, alignment=Qt.AlignTop)

        self.image_button.enterEvent = self.button_enter
        self.image_button.leaveEvent = self.button_leave

    def button_enter(self, event):
        self.title_label.setStyleSheet("""
            QLabel {color: #ff5555; background-color: #1d1d1d; padding: 5px;}
            QLabel:hover {color: #ff5555;}
        """)
    def button_leave(self, event):
        self.title_label.setStyleSheet("""
            QLabel {color: #ffffff; background-color: #1d1d1d; padding: 5px;}
            QLabel:hover {color: #ff5555;}
        """)

    def set_icon(self, code):
        cached_thumb = [thumb for thumb in self.player.thumb_cache if str(code) in thumb][0]
        self.player.thumb_cache.pop(cached_thumb)
        self.image_button.setIcon(self.player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\{code}"))

    def resizeEvent(self, event):
        self.image_button.setFixedHeight(int(self.image_button.width() * 0.562))

        self.title_label.setFixedWidth(int(self.image_button.width()))
        self.title_label.setFixedHeight(self.height)

        self.setFixedHeight(int(self.image_button.width() * 0.562) + self.height)

        if self.overlay_pixmap:
            self.overlay_label.setFixedSize(self.image_button.size())
            scaled_pixmap = self.overlay_pixmap.scaled(self.image_button.width(), self.image_button.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.overlay_label.setPixmap(scaled_pixmap)


class SelectorPanel(Partition):
    def __init__(self, player, color, screen_scale):
        super().__init__(color)
        self.player = player
        self.icon_cache = {}
        self.screen_scale = screen_scale

        self.num_columns = 3
        self.columns_spacing = {0: 80, 1: 80, 2: 50, 3: 40, 4: 35, 5: 31}

        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignTop)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {border: 1px solid #292929; background: #292929; width: 15px; margin: 0px 0px 0px 0px;}
            QScrollBar::handle:vertical {background: #191919; min-height: 20px; border-radius: 7px;}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: none; height: 0px;}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: #292929;}
        """)

        # Create outer container to allow widgets to top-align
        outer_container = QWidget()
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.setAlignment(Qt.AlignTop)
        outer_container.setLayout(outer_layout)

        # Create inner container for grid layout
        content_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        content_widget.setLayout(self.grid_layout)

        # Add content to outer container, and set container as scroll widget
        outer_layout.addWidget(content_widget)
        self.scroll_area.setWidget(outer_container)

        # For each media item, create a selector item element and add
        self.selector_buttons = []
        self.populate_selector()

        self.layout.addWidget(self.scroll_area)

    def populate_selector(self):
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.selector_buttons = []

        if self.num_columns >= 2:
            for i, med_item in enumerate(self.player.filtered_media):
                button = SelectorItem(self.player, med_item, self.screen_scale)
                self.selector_buttons.append(button)
                self.grid_layout.addWidget(button, i // self.num_columns, i % self.num_columns)

            self.scroll_area.widget().updateGeometry()
            self.updateGeometry()

            self.adjust_buttons_sizes(self.num_columns)

        else:
            for i, med_item in enumerate(self.player.filtered_media):

                if self.num_columns == 1:
                    button = SelectorRow(self.player, med_item, self.screen_scale, create_image=True)
                else:
                    button = SelectorRow(self.player, med_item, self.screen_scale, create_image=False)

                self.selector_buttons.append(button)
                self.grid_layout.addWidget(button, i // 1, i % 1)

            self.scroll_area.widget().updateGeometry()
            self.updateGeometry()

            if self.num_columns == 1:
                self.adjust_buttons_sizes(5)

    def switch_size(self):
        self.num_columns = {3: 4, 4: 5, 5: 1, 1: 0, 0: 2, 2: 3}[self.num_columns]
        self.populate_selector()

    def adjust_buttons_sizes(self, num_columns):
        for button in self.selector_buttons:
            w = int(self.width() / num_columns) - self.columns_spacing[num_columns]
            button.image_button.setIconSize(QSize(w, int(w * 0.562)))
            button.image_button.setMaximumSize(QSize(w, int(w * 0.562)))

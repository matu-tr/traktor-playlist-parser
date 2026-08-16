from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class TrafficLightButton(QPushButton):
    def __init__(self, color: str, hover_color: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            f"""
            QPushButton {{ background-color: {color}; border-radius: 6px; border: none; }}
            QPushButton:hover {{ background-color: {hover_color}; }}
            """
        )


class TitleBar(QWidget):
    """A slim, draggable replacement for the native OS title bar, styled
    after macOS traffic lights. Click-drag anywhere on it to move the
    window; the close (and optional minimize) button work like normal."""

    def __init__(self, title: str = "", show_minimize: bool = False, on_close=None, parent=None):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedHeight(36)
        self._drag_offset = None
        self._on_close = on_close

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(8)

        close_btn = TrafficLightButton("#ff5f56", "#ff8078")
        close_btn.clicked.connect(self._handle_close)
        layout.addWidget(close_btn)

        if show_minimize:
            min_btn = TrafficLightButton("#ffbd2e", "#ffcf5c")
            min_btn.clicked.connect(lambda: self.window().showMinimized())
            layout.addWidget(min_btn)

        layout.addStretch()

        if title:
            label = QLabel(title)
            label.setObjectName("Subtitle")
            layout.addWidget(label)
            layout.addStretch()

    def _handle_close(self):
        if self._on_close:
            self._on_close()
        else:
            self.window().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self.window().pos()

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None and event.buttons() & Qt.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_offset)

    def mouseReleaseEvent(self, event):
        self._drag_offset = None

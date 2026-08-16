from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ..formatters import FormatError, format_output
from ..models import ParseResult
from ..parsers.errors import ParseError, UnsupportedFileError
from ..parsers.html_parser import parse_html_playlist
from ..parsers.nml_parser import list_playlist_names, parse_nml_playlist
from .field_format_dialog import FieldFormatDialog
from .titlebar import TitleBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traktor Playlist Converter")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(560, 400)
        self.setAcceptDrops(True)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        card_layout.addWidget(TitleBar(show_minimize=True))

        content = QWidget()
        content.setObjectName("Content")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 4, 32, 32)
        layout.setSpacing(10)

        title = QLabel("Traktor Playlist Converter")
        title.setObjectName("Title")
        subtitle = QLabel("Drop your playlist, pick your fields, export it.")
        subtitle.setObjectName("Subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        self.drop_label = QLabel("📂  Drop your playlist file here\n(.html or .nml)")
        self.drop_label.setObjectName("DropZone")
        self.drop_label.setProperty("active", False)
        self.drop_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.drop_label, stretch=1)

        card_layout.addWidget(content, stretch=1)
        self.setCentralWidget(card)

    def _set_drop_zone_active(self, active: bool):
        self.drop_label.setProperty("active", active)
        self.drop_label.style().unpolish(self.drop_label)
        self.drop_label.style().polish(self.drop_label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            ext = Path(url.toLocalFile()).suffix.lower()
            if ext in (".html", ".htm", ".nml"):
                event.acceptProposedAction()
                self._set_drop_zone_active(True)
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        self._set_drop_zone_active(False)

    def dropEvent(self, event):
        self._set_drop_zone_active(False)
        path = event.mimeData().urls()[0].toLocalFile()
        try:
            result = self.route_and_parse(path)
        except (ParseError, UnsupportedFileError) as exc:
            QMessageBox.critical(self, "Import Failed", str(exc))
            return
        except Exception as exc:
            QMessageBox.critical(self, "Import Failed", f"Unexpected error: {exc}")
            return

        if result.warnings:
            QMessageBox.warning(self, "Warnings", "\n".join(result.warnings))

        self.handle_parsed(path, result)

    def route_and_parse(self, path: str) -> ParseResult:
        ext = Path(path).suffix.lower()
        if ext in (".html", ".htm"):
            return parse_html_playlist(path)
        elif ext == ".nml":
            names = list_playlist_names(path)
            if len(names) > 1:
                name, ok = QInputDialog.getItem(
                    self,
                    "Choose Playlist",
                    "This NML file contains multiple playlists:",
                    names,
                    editable=False,
                )
                if not ok:
                    raise ParseError("Cancelled.")
                return parse_nml_playlist(path, playlist_name=name)
            return parse_nml_playlist(path)
        else:
            raise UnsupportedFileError(
                f"Unsupported file type: {ext or '(no extension)'}. Drop a .html or .nml file."
            )

    def handle_parsed(self, source_path: str, result: ParseResult):
        dialog = FieldFormatDialog(result, self)
        if dialog.exec() != FieldFormatDialog.Accepted:
            return

        fields = dialog.selected_fields()
        style = dialog.selected_format()
        template = dialog.custom_template()

        default_name = str(Path(source_path).with_suffix(".txt").name)
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save List", default_name, "Text Files (*.txt);;All Files (*)"
        )
        if not save_path:
            return

        try:
            text = format_output(result.tracks, fields, style, template)
        except FormatError as exc:
            QMessageBox.critical(self, "Format Error", str(exc))
            return

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(text)
        except OSError as exc:
            QMessageBox.critical(self, "Save Failed", str(exc))
            return

        QMessageBox.information(
            self, "Done", f"Exported {len(result.tracks)} tracks to {save_path}"
        )

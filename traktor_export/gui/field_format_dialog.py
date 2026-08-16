from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..formatters import DEFAULT_CUSTOM_TEMPLATE, FormatError, format_output
from ..models import Field, FormatStyle, ParseResult
from .titlebar import TitleBar

_FIELD_LABELS = {
    Field.NUM: "Track Number",
    Field.TITLE: "Title",
    Field.ARTIST: "Artist",
    Field.LABEL: "Label",
    Field.BPM: "BPM",
    Field.KEY: "Key",
}

_FIELD_ORDER = [Field.NUM, Field.TITLE, Field.ARTIST, Field.LABEL, Field.BPM, Field.KEY]
_ALWAYS_ON = {Field.TITLE, Field.ARTIST}

_FORMAT_LABELS = {
    FormatStyle.NUMBERED_LIST: "Numbered list",
    FormatStyle.CUE_SHEET: "Cue sheet (00:00 timestamps)",
    FormatStyle.STANZA_BLOCK: "Stanza block",
    FormatStyle.CUSTOM: "Custom format",
}


class FieldFormatDialog(QDialog):
    def __init__(self, parse_result: ParseResult, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fields and Format")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(440)
        self._parse_result = parse_result
        self._checkboxes: dict[Field, QCheckBox] = {}
        self._format_buttons: dict[FormatStyle, QRadioButton] = {}

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        card_layout.addWidget(TitleBar(title="Fields and Format", on_close=self.reject))
        outer.addWidget(card)

        content = QWidget()
        content.setObjectName("Content")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 4, 24, 24)
        layout.setSpacing(14)
        card_layout.addWidget(content)

        summary = QLabel(f"{len(parse_result.tracks)} tracks found · {parse_result.source_kind.name}")
        summary.setObjectName("Summary")
        layout.addWidget(summary)

        fields_box = QGroupBox("Fields to include")
        fields_layout = QHBoxLayout(fields_box)
        for f in _FIELD_ORDER:
            cb = QCheckBox(_FIELD_LABELS[f])
            available = f in parse_result.available_fields
            forced = f in _ALWAYS_ON
            cb.setChecked(available)
            cb.setEnabled(available and not forced)
            cb.stateChanged.connect(self._update_preview)
            self._checkboxes[f] = cb
            fields_layout.addWidget(cb)
        layout.addWidget(fields_box)

        format_box = QGroupBox("Output format")
        format_layout = QVBoxLayout(format_box)
        button_group = QButtonGroup(self)
        for style in FormatStyle:
            rb = QRadioButton(_FORMAT_LABELS[style])
            if style == FormatStyle.NUMBERED_LIST:
                rb.setChecked(True)
            rb.toggled.connect(self._update_preview)
            button_group.addButton(rb)
            self._format_buttons[style] = rb
            format_layout.addWidget(rb)

        self.template_input = QLineEdit(DEFAULT_CUSTOM_TEMPLATE)
        self.template_input.setEnabled(False)
        self.template_input.textChanged.connect(self._update_preview)
        self._format_buttons[FormatStyle.CUSTOM].toggled.connect(self.template_input.setEnabled)
        format_layout.addWidget(self.template_input)

        placeholders = QLabel("Available fields: {track_number} {artist} {title} {label} {bpm} {key}")
        placeholders.setObjectName("Subtitle")
        placeholders.setWordWrap(True)
        format_layout.addWidget(placeholders)

        layout.addWidget(format_box)

        self.preview_label = QLabel()
        self.preview_label.setObjectName("Preview")
        self.preview_label.setWordWrap(True)
        layout.addWidget(self.preview_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._update_preview()

    def _update_preview(self, *_):
        if not self._parse_result.tracks:
            return
        sample = self._parse_result.tracks[:2]
        try:
            text = format_output(
                sample, self.selected_fields(), self.selected_format(), self.custom_template()
            )
        except FormatError as exc:
            self.preview_label.setText(f"⚠ {exc}")
            return
        self.preview_label.setText(text or "(empty output)")

    def _on_accept(self):
        fields = self.selected_fields()
        style = self.selected_format()
        no_core_field = Field.TITLE not in fields and Field.ARTIST not in fields
        if style != FormatStyle.CUSTOM and no_core_field:
            QMessageBox.warning(self, "Invalid Selection", "At least Title or Artist must be selected.")
            return
        if style == FormatStyle.CUSTOM:
            try:
                format_output(self._parse_result.tracks[:1], fields, style, self.custom_template())
            except FormatError as exc:
                QMessageBox.warning(self, "Invalid Format Template", str(exc))
                return
        self.accept()

    def selected_fields(self) -> list[Field]:
        return [f for f, cb in self._checkboxes.items() if cb.isChecked()]

    def selected_format(self) -> FormatStyle:
        for style, rb in self._format_buttons.items():
            if rb.isChecked():
                return style
        return FormatStyle.NUMBERED_LIST

    def custom_template(self) -> str:
        return self.template_input.text()

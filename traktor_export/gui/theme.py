STYLESHEET = """
QWidget {
    background-color: #1b1d23;
    color: #e6e6ea;
    font-family: -apple-system, "Segoe UI", "Helvetica Neue", sans-serif;
    font-size: 13px;
}

QMainWindow, QDialog {
    background: transparent;
}

QWidget#TitleBar, QWidget#Content {
    background: transparent;
}

QFrame#Card {
    background-color: #1b1d23;
    border-radius: 18px;
    border: 1px solid #2c2e37;
}

QLabel#Title {
    font-size: 20px;
    font-weight: 700;
    color: #f2f2f5;
}

QLabel#Subtitle {
    color: #8b8f9c;
    font-size: 13px;
}

QLabel#DropZone {
    border: 2px dashed #3a3d47;
    border-radius: 18px;
    padding: 56px;
    font-size: 15px;
    color: #9a9ea8;
    background-color: #212330;
}

QLabel#DropZone[active="true"] {
    border: 2px dashed #7c6cf0;
    background-color: #262a3d;
    color: #d6d1ff;
}

QLabel#Summary {
    color: #b8bcc8;
    font-size: 13px;
    padding-bottom: 4px;
}

QGroupBox {
    border: 1px solid #33353f;
    border-radius: 12px;
    margin-top: 16px;
    padding: 14px 12px 12px 12px;
    font-weight: 600;
    color: #cfd2db;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #a9adba;
}

QCheckBox, QRadioButton {
    padding: 5px 0;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QLineEdit {
    background-color: #262a34;
    border: 1px solid #3a3d47;
    border-radius: 8px;
    padding: 8px 10px;
    color: #e6e6ea;
    selection-background-color: #7c6cf0;
}

QLineEdit:focus {
    border: 1px solid #7c6cf0;
}

QLineEdit:disabled {
    color: #5c606c;
    background-color: #1f212a;
}

QPushButton {
    background-color: #7c6cf0;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 9px 20px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #8d7ff5;
}

QPushButton:pressed {
    background-color: #6a5add;
}

QPushButton:disabled {
    background-color: #33353f;
    color: #6b6f7c;
}

QLabel#Preview {
    background-color: #14151a;
    border: 1px solid #2c2e37;
    border-radius: 10px;
    padding: 12px;
    font-family: "SF Mono", "Cascadia Code", Consolas, monospace;
    font-size: 12px;
    color: #8be9c1;
}

QMessageBox {
    background-color: #1b1d23;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #3a3d47;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

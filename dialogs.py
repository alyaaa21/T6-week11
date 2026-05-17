# nama: alya dwi pangesti
# nim: f1d02310104
# kelas: pemvis D

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox,
    QLineEdit, QTextEdit, QComboBox, QLabel
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt


class PostDialog(QDialog):
 
    def __init__(self, parent=None, post=None):
        super().__init__(parent)

        is_edit = post is not None
        self.setWindowTitle("✏️  Edit Post" if is_edit else "✨  Tambah Post Baru")
        self.setMinimumWidth(480)
        self.setMinimumHeight(420)

        self.setStyleSheet("""
            QDialog {
                background-color: #FFF0F5;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #8B2252;
                font-weight: 600;
                font-size: 12px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                border: 2px solid #F4A7C3;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
                color: #4A0030;
                selection-background-color: #F48FB1;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #E91E8C;
                background-color: #FFF5F9;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QPushButton {
                background-color: #E91E8C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #C2185B;
            }
            QPushButton:pressed {
                background-color: #AD1457;
            }
            QPushButton[text="Cancel"] {
                background-color: #F8BBD9;
                color: #880E4F;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #F48FB1;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Edit Post" if is_edit else "Tambah Post Baru")
        title_label.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #880E4F; margin-bottom: 4px;"
        )
        layout.addWidget(title_label)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul post...")

        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Isi konten post...")
        self.body_input.setMinimumHeight(100)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Nama penulis...")

        self.slug_input = QLineEdit()
        self.slug_input.setPlaceholderText("url-friendly-slug (contoh: judul-post-saya)")

        self.status_input = QComboBox()
        self.status_input.addItems(["published", "draft"])

        form.addRow("Title *", self.title_input)
        form.addRow("Body *", self.body_input)
        form.addRow("Author *", self.author_input)
        form.addRow("Slug *", self.slug_input)
        form.addRow("Status", self.status_input)

        layout.addLayout(form)

        note = QLabel("* Field wajib diisi. Slug harus unik.")
        note.setStyleSheet("color: #AD1457; font-size: 11px; font-style: italic;")
        layout.addWidget(note)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.button(QDialogButtonBox.Ok).setText("Simpan")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancel")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if is_edit:
            self.title_input.setText(post.get('title', ''))
            self.body_input.setPlainText(post.get('body', ''))
            self.author_input.setText(post.get('author', ''))
            self.slug_input.setText(post.get('slug', ''))
            idx = self.status_input.findText(post.get('status', 'draft'))
            if idx >= 0:
                self.status_input.setCurrentIndex(idx)

    def get_data(self):
        return {
            'title': self.title_input.text().strip(),
            'body': self.body_input.toPlainText().strip(),
            'author': self.author_input.text().strip(),
            'slug': self.slug_input.text().strip(),
            'status': self.status_input.currentText()
        }
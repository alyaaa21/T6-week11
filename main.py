# nama: alya dwi pangesti
# nim: f1d02310104
# kelas: pemvis D

import sys
from PySide6.QtCore import QThread, Qt
from PySide6.QtGui import QFont, QColor, QPalette, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QTextEdit, QSplitter, QHeaderView, QMessageBox, QDialog,
    QFrame, QScrollArea, QSizePolicy
)
from dialogs import PostDialog
from api_worker import ApiWorker


GLOBAL_STYLE = """
* {
    font-family: 'Segoe UI', 'Arial', sans-serif;
}

QMainWindow {
    background-color: #FFF0F5;
}

QWidget#centralWidget {
    background-color: #FFF0F5;
}

/* ── Header Bar ── */
QWidget#headerBar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #E91E8C, stop:0.5 #F06292, stop:1 #F48FB1);
    border-bottom: 2px solid #C2185B;
}

QLabel#appTitle {
    color: #ffffff;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#appSubtitle {
    color: #FCE4EC;
    font-size: 12px;
}

/* ── Status Bar ── */
QLabel#statusLabel {
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
}

/* ── Buttons ── */
QPushButton {
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
    border: none;
    min-width: 90px;
}

QPushButton#btnRefresh {
    background-color: #F8BBD9;
    color: #880E4F;
    border: 2px solid #F48FB1;
}
QPushButton#btnRefresh:hover {
    background-color: #F48FB1;
    color: #4A0030;
}
QPushButton#btnRefresh:disabled {
    background-color: #FCE4EC;
    color: #CE93D8;
    border-color: #F8BBD9;
}

QPushButton#btnTambah {
    background-color: #E91E8C;
    color: white;
}
QPushButton#btnTambah:hover {
    background-color: #C2185B;
}
QPushButton#btnTambah:disabled {
    background-color: #F8BBD9;
    color: #CE93D8;
}

QPushButton#btnEdit {
    background-color: #F06292;
    color: white;
}
QPushButton#btnEdit:hover {
    background-color: #E91E63;
}
QPushButton#btnEdit:disabled {
    background-color: #F8BBD9;
    color: #CE93D8;
}

QPushButton#btnHapus {
    background-color: #AD1457;
    color: white;
}
QPushButton#btnHapus:hover {
    background-color: #880E4F;
}
QPushButton#btnHapus:disabled {
    background-color: #F8BBD9;
    color: #CE93D8;
}

/* ── Table ── */
QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #FFF0F5;
    border: 2px solid #F4A7C3;
    border-radius: 10px;
    gridline-color: #FCE4EC;
    font-size: 13px;
    color: #4A0030;
    selection-background-color: #F48FB1;
    selection-color: #4A0030;
}

QTableWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #FCE4EC;
}

QTableWidget::item:selected {
    background-color: #F8BBD9;
    color: #4A0030;
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #F8BBD9, stop:1 #F4A7C3);
    color: #880E4F;
    font-weight: 700;
    font-size: 12px;
    padding: 8px 6px;
    border: none;
    border-right: 1px solid #F4A7C3;
    border-bottom: 2px solid #E91E8C;
}

/* ── Detail Panel ── */
QTextEdit#detailPanel {
    background-color: #ffffff;
    border: 2px solid #F4A7C3;
    border-radius: 10px;
    padding: 12px;
    font-size: 13px;
    color: #4A0030;
    line-height: 1.6;
}

/* ── Panel Labels ── */
QLabel#panelTitle {
    font-size: 14px;
    font-weight: 700;
    color: #880E4F;
    padding: 4px 0;
}

/* ── Frame Card ── */
QFrame#card {
    background-color: #ffffff;
    border: 2px solid #F4A7C3;
    border-radius: 12px;
}

/* ── Splitter Handle ── */
QSplitter::handle {
    background-color: #F4A7C3;
    width: 3px;
}
"""


class PostManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸  Post Manager — Threading & REST API")
        self.setGeometry(80, 80, 1100, 680)
        self.setMinimumSize(900, 560)

        self.posts_data = []
        self._thread = None
        self._worker = None

        self.setup_ui()
        self.fetch_posts()  # langsung fetch saat aplikasi dibuka


    def setup_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setSpacing(0)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # ── Header Bar ──────────────────────────────────────────────────
        header = QWidget()
        header.setObjectName("headerBar")
        header.setFixedHeight(64)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)

        icon_lbl = QLabel("🌸")
        icon_lbl.setStyleSheet("font-size: 28px;")

        title_col = QVBoxLayout()
        title_col.setSpacing(0)

        app_title = QLabel("Post Manager")
        app_title.setObjectName("appTitle")

        app_subtitle = QLabel("Threading & REST API — PySide6")
        app_subtitle.setObjectName("appSubtitle")

        title_col.addWidget(app_title)
        title_col.addWidget(app_subtitle)

        h_layout.addWidget(icon_lbl)
        h_layout.addSpacing(10)
        h_layout.addLayout(title_col)
        h_layout.addStretch()

        root_layout.addWidget(header)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 12, 16, 12)
        body_layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.status_label = QLabel("Memuat data...")
        self.status_label.setObjectName("statusLabel")

        self.btn_refresh = QPushButton("🔄  Refresh")
        self.btn_refresh.setObjectName("btnRefresh")

        self.btn_tambah = QPushButton("✨  Tambah")
        self.btn_tambah.setObjectName("btnTambah")

        self.btn_edit = QPushButton("✏️  Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setEnabled(False)

        self.btn_hapus = QPushButton("🗑️  Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.setEnabled(False)

        top_row.addWidget(self.status_label)
        top_row.addStretch()
        top_row.addWidget(self.btn_refresh)
        top_row.addWidget(self.btn_tambah)
        top_row.addWidget(self.btn_edit)
        top_row.addWidget(self.btn_hapus)

        body_layout.addLayout(top_row)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)

        left_card = QFrame()
        left_card.setObjectName("card")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        tbl_header = QLabel("  📋  Daftar Posts")
        tbl_header.setObjectName("panelTitle")
        tbl_header.setStyleSheet(
            "background-color: #FFF0F5; padding: 8px 12px;"
            "border-bottom: 1px solid #F4A7C3; color: #880E4F; font-weight: 700;"
        )
        left_layout.addWidget(tbl_header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Title', 'Author', 'Status'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 45)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 90)
        self.table.setStyleSheet("border: none; border-radius: 0;")
        left_layout.addWidget(self.table)

        splitter.addWidget(left_card)

        right_card = QFrame()
        right_card.setObjectName("card")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        detail_header = QLabel("  🔍  Detail Post")
        detail_header.setObjectName("panelTitle")
        detail_header.setStyleSheet(
            "background-color: #FFF0F5; padding: 8px 12px;"
            "border-bottom: 1px solid #F4A7C3; color: #880E4F; font-weight: 700;"
        )
        right_layout.addWidget(detail_header)

        self.detail = QTextEdit()
        self.detail.setObjectName("detailPanel")
        self.detail.setReadOnly(True)
        self.detail.setPlaceholderText("Pilih post dari tabel untuk melihat detail...")
        self.detail.setStyleSheet("border: none; border-radius: 0;")
        right_layout.addWidget(self.detail)

        splitter.addWidget(right_card)
        splitter.setSizes([560, 440])

        body_layout.addWidget(splitter)
        root_layout.addWidget(body)

        self.btn_refresh.clicked.connect(self.fetch_posts)
        self.btn_tambah.clicked.connect(self.add_post)
        self.btn_edit.clicked.connect(self.edit_post)
        self.btn_hapus.clicked.connect(self.delete_post)
        self.table.currentCellChanged.connect(self.on_row_selected)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)


    def run_worker(self, action, on_success, **kwargs):
        self._thread = QThread()
        self._worker = ApiWorker(action, **kwargs)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(on_success)
        self._worker.error.connect(self.on_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(lambda: self.set_loading(False))

        self.set_loading(True)
        self._thread.start()

    def set_loading(self, is_loading):
        self.btn_refresh.setEnabled(not is_loading)
        self.btn_tambah.setEnabled(not is_loading)

        has_selection = self.table.currentRow() >= 0
        self.btn_edit.setEnabled(not is_loading and has_selection)
        self.btn_hapus.setEnabled(not is_loading and has_selection)

        if is_loading:
            self.set_status("loading", "⏳  Memuat data...")

    def set_status(self, state, msg):
        colors = {
            "loading": ("color:#0D47A1; background:#E3F2FD;", msg),
            "success": ("color:#1B5E20; background:#E8F5E9;", msg),
            "error":   ("color:#B71C1C; background:#FFEBEE;", msg),
            "empty":   ("color:#E65100; background:#FFF3E0;", msg),
        }
        style, text = colors.get(state, ("", msg))
        self.status_label.setStyleSheet(
            f"font-weight:600; font-size:12px; padding:6px 12px;"
            f"border-radius:6px; {style}"
        )
        self.status_label.setText(text)


    def fetch_posts(self):
        self.run_worker("get_posts", self.on_posts_loaded)

    def on_posts_loaded(self, posts):
        self.posts_data = posts
        self.table.setRowCount(0)
        self.detail.clear()

        if not posts:
            self.set_status("empty", "ℹ️  Tidak ada data post ditemukan")
            return

        for p in posts:
            row = self.table.rowCount()
            self.table.insertRow(row)

            id_item = QTableWidgetItem(str(p.get('id', '')))
            id_item.setTextAlignment(Qt.AlignCenter)

            status_val = p.get('status', '')
            status_item = QTableWidgetItem(status_val)
            status_item.setTextAlignment(Qt.AlignCenter)
            # Warna badge status
            if status_val == 'published':
                status_item.setForeground(QColor("#1B5E20"))
                status_item.setBackground(QColor("#E8F5E9"))
            else:
                status_item.setForeground(QColor("#E65100"))
                status_item.setBackground(QColor("#FFF3E0"))

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, QTableWidgetItem(p.get('title', '')))
            self.table.setItem(row, 2, QTableWidgetItem(p.get('author', '')))
            self.table.setItem(row, 3, status_item)

        self.set_status("success", f"✅  {len(posts)} posts berhasil dimuat")


    def on_selection_changed(self):
        has_selection = len(self.table.selectedItems()) > 0
        self.btn_edit.setEnabled(has_selection)
        self.btn_hapus.setEnabled(has_selection)

    def on_row_selected(self, row, col, prev_row, prev_col):
        if row < 0 or row >= len(self.posts_data):
            return

        post = self.posts_data[row]
        post_id = post.get('id')

        self.detail.setPlainText(
            f"⏳ Memuat detail post ID {post_id}..."
        )

        self.run_worker("get_post", self.on_detail_loaded, post_id=post_id)

    def on_detail_loaded(self, post):
        comments = post.get('comments', [])

        lines = [
            f"📌  ID          : {post.get('id', '')}",
            f"📝  Title       : {post.get('title', '')}",
            f"👤  Author      : {post.get('author', '')}",
            f"🔗  Slug        : {post.get('slug', '')}",
            f"🏷️  Status      : {post.get('status', '')}",
            f"",
            f"📄  Body:",
            f"{post.get('body', '')}",
            f"",
            f"─────────────────────────────────",
            f"💬  Comments ({len(comments)}):",
        ]

        if comments:
            for i, c in enumerate(comments, 1):
                lines.append(f"  [{i}] {c.get('author', 'Unknown')} — {c.get('body', '')}")
        else:
            lines.append("  (Tidak ada komentar)")

        self.detail.setPlainText("\n".join(lines))


    def add_post(self):
        dialog = PostDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()

            missing = [f for f in ['title', 'body', 'author', 'slug'] if not data.get(f)]
            if missing:
                QMessageBox.warning(
                    self, "⚠️  Validasi",
                    f"Field berikut wajib diisi:\n• " + "\n• ".join(missing)
                )
                return

            self.run_worker(
                "create_post", self.on_post_created,
                title=data['title'],
                body=data['body'],
                author=data['author'],
                slug=data['slug'],
                status=data['status']
            )

    def on_post_created(self, result):
        new_id = result.get('data', {}).get('id', '?')
        QMessageBox.information(
            self, "✅  Sukses",
            f"Post berhasil ditambahkan!\nID yang dikembalikan server: {new_id}"
        )
        self.fetch_posts()


    def edit_post(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "⚠️  Peringatan", "Pilih post terlebih dahulu!")
            return

        post = self.posts_data[row]
        dialog = PostDialog(self, post)

        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()

            missing = [f for f in ['title', 'body', 'author', 'slug'] if not data.get(f)]
            if missing:
                QMessageBox.warning(
                    self, "⚠️  Validasi",
                    f"Field berikut wajib diisi:\n• " + "\n• ".join(missing)
                )
                return

            self.run_worker(
                "update_post", self.on_post_updated,
                post_id=post['id'],
                title=data['title'],
                body=data['body'],
                author=data['author'],
                slug=data['slug'],
                status=data['status']
            )

    def on_post_updated(self, result):
        QMessageBox.information(self, "✅  Sukses", "Post berhasil diupdate!")
        self.fetch_posts()


    def delete_post(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "⚠️  Peringatan", "Pilih post terlebih dahulu!")
            return

        post = self.posts_data[row]
        post_id = post.get('id')
        title = post.get('title', 'post ini')

        reply = QMessageBox.question(
            self,
            "🗑️  Konfirmasi Hapus",
            f"Yakin ingin menghapus post berikut?\n\n"
            f"ID     : {post_id}\n"
            f"Title  : {title}\n\n"
            f"⚠️  Semua komentar juga akan ikut terhapus (cascade delete).",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.run_worker("delete_post", self.on_post_deleted, post_id=post_id)

    def on_post_deleted(self, result):
        QMessageBox.information(self, "✅  Sukses", "Post berhasil dihapus!")
        self.detail.clear()
        self.fetch_posts()


    def on_error(self, message):
        self.set_status("error", f"❌  Error: {message}")
        QMessageBox.critical(
            self, "❌  API Error",
            f"Terjadi kesalahan:\n\n{message}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_STYLE)

    window = PostManagerApp()
    window.show()
    sys.exit(app.exec())
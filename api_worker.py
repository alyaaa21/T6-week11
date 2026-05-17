# nama: alya dwi pangesti
# nim: f1d02310104
# kelas: pemvis D

from PySide6.QtCore import QObject, Signal
from api_service import ApiService


class ApiWorker(QObject):

    finished = Signal()       # selalu dipanggil di akhir (sukses maupun gagal)
    success = Signal(object)  # kirim data hasil (list/dict/bool)
    error = Signal(str)       # kirim pesan error

    def __init__(self, action, post_id=None, title=None, body=None,
                 author=None, slug=None, status=None):
        super().__init__()
        self.action = action
        self.post_id = post_id
        self.title = title
        self.body = body
        self.author = author
        self.slug = slug
        self.status = status
        self.service = ApiService()

    def run(self):
        try:
            if self.action == "get_posts":
                result = self.service.get_posts()

            elif self.action == "get_post":
                result = self.service.get_post(self.post_id)

            elif self.action == "create_post":
                result = self.service.create_post(
                    self.title, self.body, self.author, self.slug, self.status
                )

            elif self.action == "update_post":
                result = self.service.update_post(
                    self.post_id, self.title, self.body,
                    self.author, self.slug, self.status
                )

            elif self.action == "delete_post":
                result = self.service.delete_post(self.post_id)

            else:
                raise ValueError(f"Action tidak dikenali: {self.action}")

            self.success.emit(result)

        except Exception as e:
            self.error.emit(str(e))

        finally:
            self.finished.emit()  # selalu emit agar thread bisa berhenti
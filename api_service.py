# nama: alya dwi pangesti
# nim: f1d02310104
# kelas: pemvis D

import requests

class ApiService:

    BASE_URL = "https://api.pahrul.my.id/api"
    TIMEOUT = 10  


    def get_posts(self):
        response = requests.get(
            f"{self.BASE_URL}/posts",
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return response.json()['data']

    def get_post(self, post_id):
        response = requests.get(
            f"{self.BASE_URL}/posts/{post_id}",
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return response.json()['data']

    def create_post(self, title, body, author, slug, status):
        payload = {
            'title': title,
            'body': body,
            'author': author,
            'slug': slug,
            'status': status
        }
        response = requests.post(
            f"{self.BASE_URL}/posts",
            json=payload,
            timeout=self.TIMEOUT
        )
        if response.status_code == 422:
            errors = response.json().get('errors', {})
            msg_parts = []
            for field, msgs in errors.items():
                if isinstance(msgs, list):
                    msg_parts.append(f"{field}: {msgs[0]}")
                else:
                    msg_parts.append(f"{field}: {msgs}")
            raise ValueError("Validasi gagal:\n" + "\n".join(msg_parts))
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id, title, body, author, slug, status):
        payload = {
            'title': title,
            'body': body,
            'author': author,
            'slug': slug,
            'status': status
        }
        response = requests.put(
            f"{self.BASE_URL}/posts/{post_id}",
            json=payload,
            timeout=self.TIMEOUT
        )
        if response.status_code == 422:
            errors = response.json().get('errors', {})
            msg_parts = []
            for field, msgs in errors.items():
                if isinstance(msgs, list):
                    msg_parts.append(f"{field}: {msgs[0]}")
                else:
                    msg_parts.append(f"{field}: {msgs}")
            raise ValueError("Validasi gagal:\n" + "\n".join(msg_parts))
        response.raise_for_status()
        return response.json()

    def delete_post(self, post_id):
        response = requests.delete(
            f"{self.BASE_URL}/posts/{post_id}",
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return True

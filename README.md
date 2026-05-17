nama: alya dwi pangesti
nim: f1d02310014
kelas: pemvis D

# Post Manager — Tugas 5 PySide6

Aplikasi desktop untuk mengelola data post menggunakan REST API nyata.
Dibangun dengan PySide6 dan menggunakan multi-threading agar UI tidak freeze saat melakukan request ke server.

---

## Struktur File

```
post_manager/
  ├── api_service.py   ← Semua logika HTTP request (GET, POST, PUT, DELETE)
  ├── api_worker.py    ← Menjalankan request di thread terpisah
  ├── dialogs.py       ← Form dialog Tambah & Edit post
  ├── main.py          ← Tampilan utama & entry point
  └── README.md
```

Setiap file punya tanggung jawab sendiri — prinsip ini disebut **Separation of Concerns (SoC)**.
Artinya file HTTP tidak bercampur dengan file tampilan, dan sebaliknya.

---

## API yang Digunakan

**Base URL:** `https://api.pahrul.my.id/api`

| Operasi | Method | Endpoint | Keterangan |
|---|---|---|---|
| Ambil semua post | GET | `/api/posts` | Mengembalikan list semua post |
| Detail satu post | GET | `/api/posts/{id}` | Mengembalikan post + daftar comments |
| Tambah post baru | POST | `/api/posts` | Body: title, body, author, slug, status |
| Edit post | PUT | `/api/posts/{id}` | Body: title, body, author, slug, status |
| Hapus post | DELETE | `/api/posts/{id}` | Comments ikut terhapus (cascade delete) |

> API ini nyata — data yang dibuat, diubah, atau dihapus akan benar-benar tersimpan di server.

---

## Fitur Aplikasi

- **Lihat Daftar Post** — semua post ditampilkan dalam tabel dengan kolom ID, Title, Author, dan Status
- **Lihat Detail Post** — klik baris di tabel untuk melihat isi lengkap post beserta komentar di panel kanan
- **Tambah Post** — klik tombol Tambah, isi form, klik Simpan
- **Edit Post** — pilih post dari tabel, klik Edit, ubah data, klik Simpan
- **Hapus Post** — pilih post dari tabel, klik Hapus, konfirmasi dulu baru dihapus
- **Status Loading** — saat request berjalan, semua tombol nonaktif dan status berubah jadi biru
- **Penanganan Error** — jika koneksi gagal atau server error, pesan error langsung ditampilkan

---

## Mengapa Pakai Threading?

Kalau request ke API dijalankan langsung di main thread (thread yang mengurus tampilan),
maka selama menunggu response dari server, **aplikasi akan freeze** — tidak bisa diklik sama sekali.

Solusinya: jalankan request di **worker thread** terpisah menggunakan `QThread`.
Main thread tetap bebas mengurus tampilan, worker thread yang mengurus koneksi ke server.
Setelah selesai, hasil dikirim balik ke main thread lewat **Signal**.

```
Main Thread  →  tampilan tetap responsif
Worker Thread →  request ke API berjalan di background
Signal        →  cara aman mengirim data dari worker ke main thread
```

---

## Penjelasan Tiap File

### `api_service.py` — Layer Data

Berisi semua kode untuk berkomunikasi dengan API. Setiap method merepresentasikan satu operasi:

- `get_posts()` — ambil semua post
- `get_post(id)` — ambil satu post berdasarkan ID
- `create_post(...)` — kirim post baru
- `update_post(...)` — update post yang sudah ada
- `delete_post(id)` — hapus post

File ini tidak mengandung kode Qt sama sekali — bisa diuji langsung dari terminal tanpa membuka UI.

---

### `api_worker.py` — Layer Threading

Berisi class `ApiWorker` yang mewarisi `QObject`. Worker ini dipindahkan ke `QThread` oleh `main.py`
sehingga method `run()` dieksekusi di thread terpisah, bukan di main thread.

Worker menerima nama aksi (`action`) seperti `"get_posts"` atau `"create_post"`,
lalu memanggil method yang sesuai di `ApiService`.

Hasil dikirim balik ke main thread lewat tiga signal:
- `success` — kalau request berhasil
- `error` — kalau request gagal
- `finished` — selalu dikirim di akhir, baik sukses maupun gagal

---

### `dialogs.py` — Layer Komponen UI

Berisi class `PostDialog` — form popup untuk input data post.

Dialog ini dipakai di dua kondisi:
- **Mode Tambah** — form kosong, dipanggil dengan `PostDialog(self)`
- **Mode Edit** — form terisi data lama, dipanggil dengan `PostDialog(self, post)`

Field yang tersedia: Title, Body, Author, Slug, Status (dropdown: published / draft).

---

### `main.py` — Window Utama

File utama yang menggabungkan semua komponen. Tugasnya:

1. Menampilkan UI (tabel, panel detail, tombol-tombol)
2. Membuat `QThread` dan `ApiWorker` saat tombol diklik
3. Menerima hasil dari worker lewat signal dan menampilkannya ke layar
4. Menangani state loading, sukses, error, dan empty

Method `run_worker()` adalah helper yang mengurangi pengulangan kode —
setiap kali butuh API call, cukup panggil satu method ini.


## Screenshots
<img width="1103" height="709" alt="Screenshot 2026-05-18 at 03 21 34" src="https://github.com/user-attachments/assets/e1e04143-a228-437a-87e8-193ed810af0e" />
<img width="1105" height="709" alt="Screenshot 2026-05-18 at 03 21 52" src="https://github.com/user-attachments/assets/ffa21e89-1bf3-48cb-bab4-96df69324663" />
<img width="1102" height="709" alt="Screenshot 2026-05-18 at 03 22 21" src="https://github.com/user-attachments/assets/f9ae3a97-8c02-49f2-ad11-79eaf1596689" />
<img width="1104" height="709" alt="Screenshot 2026-05-18 at 03 22 47" src="https://github.com/user-attachments/assets/f5bbbb9a-69b8-473d-bdd0-6ca5ede3266a" />
<img width="1103" height="712" alt="Screenshot 2026-05-18 at 03 23 00" src="https://github.com/user-attachments/assets/daac6810-194e-4dc9-82d3-5969c989ea5a" />
<img width="1105" height="706" alt="Screenshot 2026-05-18 at 03 23 11" src="https://github.com/user-attachments/assets/d98fbd70-79b0-44a0-b861-1b845b61bc82" />
<img width="1099" height="709" alt="Screenshot 2026-05-18 at 03 23 19" src="https://github.com/user-attachments/assets/d851c967-14a9-49af-87e0-df729441745b" />

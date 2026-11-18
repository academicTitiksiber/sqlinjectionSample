siberFinance - Local SQLite Authentication Lab

Aplikasi web Flask sederhana untuk lingkungan pelatihan keamanan aplikasi web lokal yang berfokus pada pemahaman mekanisme autentikasi berbasis SQLite dan analisis kerentanan kueri SQL.

Ringkasan Proyek

Proyek ini menyediakan antarmuka login dan dashboard sederhana berbasis Flask yang terhubung ke database SQLite lokal (lab.db). Aplikasi secara otomatis menginisialisasi skema tabel users beserta data akun contoh saat modul pertama kali dimuat, dan membatasi server pengembangan agar hanya berjalan pada antarmuka loopback (127.0.0.1 atau localhost).

Teknologi yang Digunakan

Python 3.10+

Flask (>=3.0,<4.0)

python-dotenv (>=1.0,<2.0)

SQLite3 (pustaka standar Python)

HTML/CSS dan Vanilla JavaScript (templates/index.html)

Struktur Direktori

sqlinjectionsample/
├── app.py                  # Aplikasi utama Flask, inisialisasi SQLite, dan routing
├── requirements.txt        # Daftar dependensi Python
├── templates/
│   └── index.html          # Antarmuka halaman login dan dashboard pengguna
└── .env                    # Konfigurasi variabel lingkungan lokal (opsional)


Prasyarat

Python 3.10 atau versi yang lebih baru

pip dan venv untuk manajemen lingkungan virtual

Instalasi dan Konfigurasi

Clone atau unduh repositori ke direktori lokal Anda, lalu masuk ke folder proyek:

cd sqlinjectionsample


Buat dan aktifkan lingkungan virtual Python:

python3 -m venv .venv
source .venv/bin/activate


Pada Windows (PowerShell):

.venv\Scripts\Activate.ps1


Pasang dependensi yang diperlukan:

pip install -r requirements.txt


(Opsional) Buat file .env di direktori utama untuk menyesuaikan konfigurasi lokal:

SECRET_KEY=ganti-dengan-string-acak-yang-aman
DB_PATH=lab.db
HOST=127.0.0.1
PORT=5000


Jika file .env tidak dibuat, aplikasi akan menggunakan nilai bawaan: DB_PATH=lab.db, HOST=127.0.0.1, dan PORT=5000.

Menjalankan Aplikasi

Jalankan server Flask secara lokal:

python app.py


Setelah berjalan, buka browser dan akses http://127.0.0.1:5000.

Catatan: Aplikasi menerapkan validasi host pada app.py sehingga akan menolak dijalankan apabila HOST diatur ke alamat selain 127.0.0.1 atau localhost.

Ringkasan Endpoint

Metode

Path

Deskripsi

GET

/

Menampilkan halaman login atau mengarahkan ke /dashboard jika sesi aktif

POST

/login

Memproses kredensial pengguna dari form login

GET

/dashboard

Menampilkan halaman akun terautentikasi

POST

/logout

Menghapus sesi aktif dan mengarahkan kembali ke halaman login

Peringatan Keamanan dan Etika Penggunaan

Aplikasi ini dibuat khusus untuk tujuan pembelajaran dan audit kode di lingkungan lokal yang terisolasi.

Jangan men-deploy kode ini ke jaringan publik atau lingkungan produksi.

Untuk standar pengembangan produksi, selalu gunakan parameterized query (? pada sqlite3), terapkan hashing kata sandi menggunakan algoritma standar seperti Argon2 atau bcrypt, simpan SECRET_KEY melalui secret manager, dan aktifkan proteksi CSRF pada seluruh form POST.

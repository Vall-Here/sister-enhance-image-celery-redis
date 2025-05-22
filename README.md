# Image Enhancement System with Celery and Redis

Sistem pemrosesan citra paralel yang dibangun dengan Flask, Celery, dan Redis untuk meningkatkan kualitas gambar dengan metode *denoising* dan peningkatan kontras secara bersamaan.

## 📋 Deskripsi Proyek

Proyek ini merupakan aplikasi web yang memungkinkan pengguna untuk mengunggah gambar dan mendapatkan hasil gambar yang telah ditingkatkan kualitasnya melalui beberapa proses:

1. **Denoising & Enhancement** - Mengurangi noise pada gambar dan meningkatkan kecerahan
2. **Contrast Enhancement** - Meningkatkan kontras gambar secara paralel
3. **Image Combination** - Menggabungkan kedua hasil untuk mendapatkan gambar berkualitas optimal

Arsitektur sistem menggunakan:
- **Flask** sebagai web server
- **Celery** untuk distributed task processing
- **Redis** sebagai broker dan backend penyimpanan hasil

## 🛠️ Teknologi yang Digunakan

- **Backend**: Flask, Flask-CORS
- **Image Processing**: OpenCV, Pillow, NumPy
- **Task Queue**: Celery
- **Message Broker & Backend**: Redis
- **Frontend**: HTML, JavaScript, TailwindCSS

## 📊 Arsitektur Sistem

```
                             ┌────────────────┐
                             │                  │
                             │  Flask Server    │
                             │                  │
                             └────────┬───────┘
                                      │
                                      ▼
                             ┌────────────────┐
                             │                  │
                             │  Redis Broker    │
                             │                  │
                             └────────┬───────┘
                                       │
                 ┌──────────────────┬┴────────────────────────┐
                 │                    │                      │
        ┌────────▼───────────┐ ┌────────▼────────┐ ┌───────▼─────────┐
        │                 │ │                 │ │                 │
        │  Celery Worker  │ │  Celery Worker  │ │  Celery Worker  │
        │  (Denoising)    │ │  (Contrast)     │ │  (Combination)  │
        │                 │ │                 │ │                 │
        └────────┬───────────┘ └────────┬────────┘ └───────┬─────────┘
                 │                   │                   │
                 └───────────────────┬───────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │                 │
                            │  Result Image   │
                            │                 │
                            └─────────────────┘
```

## 🚀 Cara Menjalankan Aplikasi

### Prasyarat

- Python 3.8+ 
- Redis Server

### Instalasi Lingkungan

1. Clone repositori ini
   ```bash
   git clone <url-repositori>
   cd sister-enhance-image-celery-redis
   ```

2. Buat dan aktifkan virtual environment (opsional tapi disarankan)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Menjalankan Aplikasi

1. Pastikan Redis server berjalan
   ```bash
   # Redis biasanya dijalankan dengan perintah:
   redis-server
   ```

2. Jalankan Celery worker
   ```bash
   celery -A tasks worker --loglevel=info
   ```

3. Jalankan Flask server
   ```bash
   python app.py
   ```

4. Buka browser dan akses `http://localhost:5000`

## 🖥️ Fitur Aplikasi

- Unggah beberapa gambar sekaligus
- Pemrosesan paralel untuk meningkatkan kecepatan
- Real-time progress tracking
- Download hasil gambar yang telah diproses

## 🧩 Struktur Proyek

```
│   app.py                 # Flask server utama
│   requirements.txt       # Daftar dependencies
│   tasks.py               # Definisi task Celery
│
├───static
│   ├───css
│   │       styles.css
│   │
│   ├───images
│   │       hasil.jpg
│   │
│   └───js
│           script.js
│
└───templates
        index.html         # Halaman web utama
```

## 👨‍💻 Rincian Komponen

### `app.py`

File utama yang menjalankan server Flask dan menangani routing. Fungsi utama:
- Route untuk menampilkan halaman utama
- Endpoint API untuk memproses gambar
- Endpoint untuk mengambil hasil pemrosesan

### `tasks.py`

Mendefinisikan tugas-tugas Celery yang dijalankan secara paralel:
- `enhance_and_denoise_task`: Mengurangi noise dan meningkatkan kecerahan
- `enhance_contrast_task`: Meningkatkan kontras gambar
- `combine_task`: Menggabungkan hasil dari dua tugas sebelumnya

### Frontend

- Antarmuka pengguna dengan TailwindCSS
- JavaScript untuk mengirim permintaan API dan menampilkan hasil
- Real-time tracking proses dengan polling

## 📝 Catatan Pengembangan

- Pastikan Redis server berjalan sebelum memulai Celery dan Flask
- Sistem menggunakan default Redis port 6379
- Pemrosesan gambar besar mungkin membutuhkan penyesuaian timeout
- Untuk deployment produksi, pertimbangkan menggunakan Gunicorn atau uWSGI

## 🛣️ Pengembangan Selanjutnya

- Implementasi autentikasi pengguna
- Dashboard monitoring untuk Celery
- Opsi pemrosesan gambar tambahan
- Penyimpanan hasil gambar ke cloud storage
- Optimisasi performa untuk gambar resolusi tinggi

---

Dibuat untuk mata kuliah Sistem Terdistribusi

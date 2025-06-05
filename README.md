# DAKEMBAR - Aplikasi Data Keluar Masuk Barang

Aplikasi manajemen stok barang berbasis web untuk sekolah, dibangun dengan Flask dan SQLite. Dirancang khusus untuk memudahkan operator sarpras dalam mencatat transaksi barang masuk/keluar secara digital.

![Image](https://github.com/user-attachments/assets/862c0848-8513-4f6b-9848-0f4acc7140cc)

## Fitur Utama
- **📦 Manajemen Barang Masuk**: Input data barang baru dengan detail lengkap (tanggal, sumber, jumlah, harga).
- **📤 Pengeluaran Barang**: Validasi stok otomatis sebelum barang dikeluarkan.
- **📊 Laporan Real-time**: Pantau stok, riwayat transaksi, dan statistik periode tertentu.
- **🔒 Sistem Login**: Autentikasi admin dengan username/password.
- **⚠️ Notifikasi Stok Minim**: Peringatan ketika stok di bawah batas minimum.

## Teknologi
- **Backend**: Python 3.9 + Flask
- **Database**: SQLite3 (file-based)
- **Frontend**: HTML5, CSS3
- **Deployment**: Vercel (serverless)

## Instalasi Lokal
### Persyaratan:
- Python 3.9+
- Pip

### Langkah:
1. Clone repositori:
   ```bash
   git clone https://github.com/xDzaky/DAKEMBAR.git
   cd DAKEMBAR
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Inisialisasi database:
   ```bash
   python app.py
   ```
   *(File `db/database.db` akan dibuat otomatis)*

4. Jalankan aplikasi:
   ```bash
   flask run
   ```
   Buka http://localhost:5000 di browser.

## Cara Menggunakan
### Login:
- **Username**: `admin`
- **Password**: `admin123`

### 1. Tambah Barang Masuk:
- Buka menu **Barang Masuk** → **Tambah Barang**
- Isi form:
  - Tanggal, sumber barang (contoh: "PT Sumber Jaya")
  - Nomor dokumen (opsional)
  - Uraian barang (contoh: "Kertas A4")
  - Jumlah, satuan, harga satuan
- Total harga akan dihitung otomatis

### 2. Keluarkan Barang:
- Buka menu **Pengeluaran**
- Pilih barang dari dropdown (hanya stok tersedia yang muncul)
- Isi jumlah dan penerima
- Sistem akan validasi stok otomatis

### 3. Pantau Stok:
- Menu **Stok Barang** menampilkan:
  - Daftar barang beserta jumlah tersedia
  - Peringatan stok minim (warna merah)

## Struktur Folder
```
DAKEMBAR/
├── db/                  # Database SQLite
│   └── database.db
├── static/              # CSS dan assets
│   ├── form_barang.css
│   └── ...
├── templates/           # Halaman HTML
│   ├── index.html
│   └── ...
├── app.py               # Main application
├── requirements.txt     # Dependencies
└── vercel.json          # Konfigurasi deploy
```


## Dokumentasi Teknis
### Diagram Alur
![Flowchart](https://github.com/user-attachments/assets/10f998d0-17f7-4d60-ac90-33d16daf11e5)


⚠️ **Catatan Penting**:  
Aplikasi ini menggunakan SQLite untuk penyimpanan lokal. Untuk penggunaan produksi, disarankan migrasi ke database cloud seperti Supabase atau MySQL.

**Dashboard**:  
![Image](https://github.com/user-attachments/assets/862c0848-8513-4f6b-9848-0f4acc7140cc)

**Tambah_Barang**:  
![Image](https://github.com/user-attachments/assets/7d2fafe7-5da5-4ecf-8840-9d99adcf5cba)

**Pengeluaran_Barang**:  
![Image](https://github.com/user-attachments/assets/fb61eab0-d3e0-4c03-8074-ae72cb189bd6)
```

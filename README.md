# DAKEMBAR - Sistem Manajemen Stok Digital untuk Sekolah

🌐 **Live Demo**: [dakembar.vercel.app](https://dakembar.vercel.app)

![Dashboard Preview](https://github.com/user-attachments/assets/862c0848-8513-4f6b-9848-0f4acc7140cc)

Aplikasi manajemen stok berbasis web untuk operator sarpras sekolah dengan fitur lengkap pengelolaan inventaris digital.

## 🔥 Fitur Terbaru (Update)
- **🔄 Sistem Stok Otomatis** - Perhitungan real-time saat barang masuk/keluar
- **🚨 Notifikasi Stok Minim** - Peringatan visual untuk stok yang hampir habis
- **📈 Laporan Bulanan** - Grafik interaktif riwayat transaksi
- **🔒 Keamanan Enhanced** - Proteksi route dan validasi input

## 🛠 Teknologi Terupdate
- **Backend**: Python 3.10 + Flask 2.3
- **Database**: JSON-based (file `db/data.json`) - lebih ringan dari SQLite
- **Frontend**: Jinja2 templates + Chart.js
- **Deployment**: Vercel + Serverless Functions

## 🚀 Panduan Instalasi (Versi Terbaru)

### Prasyarat:
- Python 3.10+
- Pipenv (rekomendasi)

### Langkah:
```bash
git clone https://github.com/xDzaky/DAKEMBAR.git
cd DAKEMBAR

# Gunakan Pipenv untuk virtual environment
pip install pipenv
pipenv install
pipenv shell

# Inisialisasi database
python app.py --init

# Jalankan aplikasi
flask run --debug
```
Buka http://localhost:5000

## 📚 Panduan Pengguna Lengkap

### 1. Manajemen Barang Masuk
- Fitur auto-complete untuk uraian barang
- Perhitungan otomatis: `total = jumlah × harga_satuan`
- Pencatatan nomor dokumen dan keterangan

### 2. Sistem Pengeluaran Cerdas
```python
# Contoh validasi stok dalam code:
if InventoryManager.check_stock(uraian) < jumlah:
    return "Stok tidak mencukupi!"
```

### 3. Fitur Admin:
- Tambah/Edit/Hapus operator
- Setel minimum stok per item
- Backup data otomatis

## 🗂 Struktur Proyek Terupdate
```
DAKEMBAR/
├── db/
│   ├── data.json        # Database JSON utama
│   └── backup/          # Auto-backup harian
├── static/
│   ├── css/
│   │   └── dashboard.css
│   └── js/
│       └── chart.js     # Visualisasi data
├── templates/
│   ├── auth/            # Halaman login/register
│   ├── components/      # Partial templates
│   └── ...              # Halaman utama
├── app.py               # Main app (Flask)
├── requirements.txt     # Dependencies
└── vercel.json          # Konfigurasi deploy
```

## 📊 Dokumentasi API Baru
Endpoint | Method | Deskripsi
---|---|---
`/api/stock` | GET | Daftar stok tersedia
`/api/check-stock` | POST | Validasi ketersediaan stok
`/api/report` | GET | Generate laporan PDF

## 🖼 Screenshot Terupdate
**Dashboard Modern**  
![Dashboard](https://github.com/user-attachments/assets/862c0848-8513-4f6b-9848-0f4acc7140cc)

**Form Cerdas**  
![Form](https://github.com/user-attachments/assets/7d2fafe7-5da5-4ecf-8840-9d99adcf5cba)

## ⚠️ Catatan Migrasi
Untuk pengguna versi lama (SQLite):
1. Backup database SQLite
2. Jalankan migrasi otomatis:
   ```bash
   python migrate.py --from-sqlite --to-json
   ```

## 🤝 Berkontribusi
1. Fork repository
2. Buat branch fitur (`git checkout -b fitur-baru`)
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## 📜 Lisensi
MIT License - Bebas digunakan dan dimodifikasi untuk kebutuhan sekolah

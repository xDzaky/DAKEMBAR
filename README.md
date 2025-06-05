# DAKEMBAR - Aplikasi Data Keluar Masuk Barang

🌐 **Live Demo**: [dakembar.vercel.app](https://dakembar.vercel.app)

![Dashboard Preview](https://github.com/user-attachments/assets/862c0848-8513-4f6b-9848-0f4acc7140cc)

Aplikasi manajemen stok berbasis web untuk operator sarpras sekolah dengan fitur lengkap pengelolaan inventaris digital.

## 🔥 Fitur Terbaru (Update)
- **🔄 Sistem Stok Otomatis** - Perhitungan real-time saat barang masuk/keluar
- **🚨 Notifikasi Stok Minim** - Peringatan visual untuk stok yang hampir habis
- **📈 Laporan Bulanan** - Grafik interaktif riwayat transaksi

## 🔐 Login Default
- **Username**: admin
- **Password**: admin123

## 🛠 Teknologi Terupdate
- **Backend**: Python 3.10 + Flask 2.3
- **Database**: JSON-based (file `db/data.json`)
- **Frontend**: Jinja2 templates + Chart.js

## 🚀 Panduan Instalasi (Versi Terbaru)

### Prasyarat:
- Python 3.10+
- Pipenv (rekomendasi)

### Langkah:
```bash
# Clone repositori
git clone https://github.com/xDzaky/DAKEMBAR.git
cd DAKEMBAR-main

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```
Buka http://localhost:5000

## 📚 Panduan Penggunaan

### 1. Manajemen Barang
- **Tambah Barang**: 
  - Isi form di `/barang/tambah`
  - Sistem otomatis update stok

- **Edit/Hapus**:
  - Akses melalui menu Barang → Daftar Barang

### 2. Pengeluaran Barang
```python
# Contoh validasi stok dalam code:
if InventoryManager.check_stock(uraian) < jumlah:
    return error("Stok tidak mencukupi")
```

### 3. Monitoring Stok
- Peringatan visual untuk stok dibawah minimum
- Filter dan pencarian cepat

## 🗂 Struktur Proyek 
```
DAKEMBAR/
├── db/
│   └── data.json        # Database JSON utama
├── static/
│   ├── form_barang.css
│   ├── form_pengeluaran.css
│   ├── list_barang.css  
│   ├── list_pengeluaran.css
│   ├── stok_barang.css
│   └── style.css        # CSS global
├── templates/
│   ├── auth/
│   │   └── login.html
│   ├── form_barang.html
│   ├── form_pengeluaran.html
│   ├── index.html       # Dashboard utama
│   ├── list_barang.html
│   ├── list_pengeluaran.html
│   └── stok_barang.html
├── app.py               
├── requirements.txt     
├── runtime.txt          
└── vercel.json          
```

## 🖼 Screenshot Terupdate
**Dashboard Modern**  
![Dashboard](https://github.com/user-attachments/assets/862c0848-8513-4f6b-9848-0f4acc7140cc)

**Form Cerdas**  
![Form](https://github.com/user-attachments/assets/7d2fafe7-5da5-4ecf-8840-9d99adcf5cba)



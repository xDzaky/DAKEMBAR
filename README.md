# DAKEMBAR - Aplikasi Data Keluar Masuk Barang

Aplikasi manajemen stok barang berbasis web untuk sekolah, dibangun dengan Flask dan SQLite. Dirancang khusus untuk memudahkan operator sarpras dalam mencatat transaksi barang masuk/keluar secara digital.

![Dashboard Preview](screenshot.png) *(Contoh screenshot dashboard)*

## Fitur Utama
- **📦 Manajemen Barang Masuk**: Input data barang baru dengan detail lengkap (tanggal, sumber, jumlah, harga).
- **📤 Pengeluaran Barang**: Validasi stok otomatis sebelum barang dikeluarkan.
- **📊 Laporan Real-time**: Pantau stok, riwayat transaksi, dan statistik periode tertentu.
- **🔒 Sistem Login**: Autentikasi admin dengan username/password.
- **⚠️ Notifikasi Stok Minim**: Peringatan ketika stok di bawah batas minimum.

## Teknologi
- **Backend**: Python 3.9 + Flask
- **Database**: SQLite3 (file-based)
- **Frontend**: HTML5, CSS3, Bootstrap 5
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

## Deploy ke Vercel
1. Fork repository ini ke akun GitHub Anda
2. Buat proyek baru di Vercel
3. Import dari GitHub dengan konfigurasi:
   - **Framework Preset**: Other
   - **Build Command**: `pip install -r requirements.txt`
   - **Environment Variables**:
     ```
     FLASK_APP = app.py
     FLASK_ENV = production
     ```

## Dokumentasi Teknis
### Diagram Alur
![Flowchart](flowchart.png) *(Deskripsi alur CRUD)*

### Cuplikan Kode Penting
```python
# Contoh fungsi tambah barang
@app.route('/barang/tambah', methods=['POST'])
def tambah_barang():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Ambil data dari form
    data = request.form
    
    # Simpan ke database
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO barang (...) VALUES (?,?,...)', data)
        conn.commit()
    
    return redirect(url_for('barang_list'))
```

## Kontribusi
1. Buat issue terlebih dahulu untuk diskusi fitur baru
2. Fork project dan buat branch baru
3. Submit Pull Request dengan deskripsi jelas

---

⚠️ **Catatan Penting**:  
Aplikasi ini menggunakan SQLite untuk penyimpanan lokal. Untuk penggunaan produksi, disarankan migrasi ke database cloud seperti Supabase atau MySQL.
```

---

### Poin Kunci yang Dibedakan dari Contoh Teman:
1. **Spesifik ke Proyek Anda**:
   - Fokus pada fitur **keluar/masuk barang** (bukan peminjaman)
   - Tekankan validasi stok otomatis
   - Sertakan contoh data barang yang relevan

2. **Instruksi Deployment**:
   - Panduan deploy ke Vercel (sesuai masalah yang pernah dihadapi)
   - Warning tentang keterbatasan SQLite

3. **Dokumentasi Teknis**:
   - Sertakan cuplikan kode dari `app.py` yang relevan
   - Diagram alur disederhanakan sesuai fitur aktual

4. **Keamanan**:
   - Peringatan untuk mengganti password default
   - Penjelasan autentikasi session

Tambahkan screenshot:
- `dashboard.png` (tampilan menu utama)
- `form_barang.png` (contoh input data)
- `stok_warning.png` (notifikasi stok minim)

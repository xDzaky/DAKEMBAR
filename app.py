from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey123'
DATABASE = 'db/database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            dari TEXT,
            nomor TEXT,
            tanggal_bukti TEXT,
            uraian TEXT,
            satuan TEXT,
            jumlah INTEGER,
            harga_satuan INTEGER,
            total_harga INTEGER,
            keterangan TEXT
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            nama_lengkap TEXT,
            role TEXT DEFAULT 'user'
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS stok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT UNIQUE,
            satuan TEXT,
            jumlah INTEGER,
            min_stok INTEGER DEFAULT 0
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS pengeluaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            uraian TEXT,
            satuan TEXT,
            jumlah INTEGER,
            penerima TEXT,
            keterangan TEXT
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS notifikasi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipe TEXT,
            pesan TEXT,
            dibaca INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Cek apakah admin sudah ada
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=?", ('admin',))
        admin = cur.fetchone()
        
        if not admin:
            # Buat akun admin default jika tidak ada
            conn.execute("INSERT INTO admin (username, password) VALUES (?, ?)", 
                        ('admin', 'admin123'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Username atau Password salah'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            try:
                conn.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, password))
                msg = 'Berhasil daftar, silakan login.'
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                msg = 'Username sudah terdaftar.'
    return render_template('register.html', msg=msg)

@app.route('/dashboard')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/api/chart-data')
def chart_data():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        start_date = week_ago
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Data barang masuk
        cur.execute("""
            SELECT strftime('%Y-%m-%d', tanggal) as day, 
                   SUM(jumlah) as total 
            FROM barang 
            WHERE tanggal BETWEEN ? AND ?
            GROUP BY day
            ORDER BY day
        """, (start_date, end_date))
        barang_masuk = [dict(row) for row in cur.fetchall()]
        
        # Data pengeluaran
        cur.execute("""
            SELECT strftime('%Y-%m-%d', tanggal) as day, 
                   SUM(jumlah) as total 
            FROM pengeluaran 
            WHERE tanggal BETWEEN ? AND ?
            GROUP BY day
            ORDER BY day
        """, (start_date, end_date))
        pengeluaran = [dict(row) for row in cur.fetchall()]
        
        # Data stok hampir habis
        cur.execute("SELECT nama, jumlah, min_stok FROM stok WHERE jumlah <= min_stok AND min_stok > 0")
        low_stock = cur.fetchall()
        
        # Total statistik
        cur.execute("SELECT COUNT(*) as total FROM barang")
        total_barang = cur.fetchone()['total']
        
        cur.execute("SELECT COUNT(*) as total FROM pengeluaran")
        total_pengeluaran = cur.fetchone()['total']
        
        cur.execute("SELECT SUM(jumlah) as total FROM stok")
        total_stok = cur.fetchone()['total']
    
    return jsonify({
        'barang_masuk': barang_masuk,
        'pengeluaran': pengeluaran,
        'stats': {
            'total_barang': total_barang,
            'total_pengeluaran': total_pengeluaran,
            'total_stok': total_stok or 0
        },
        'low_stock': [dict(row) for row in low_stock]
    })

@app.route('/barang')
def barang_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM barang")
        rows = cur.fetchall()
    return render_template('list_barang.html', data=rows)

@app.route('/barang/tambah', methods=['GET', 'POST'])
def barang_tambah():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = (
            request.form['tanggal'],
            request.form['dari'],
            request.form['nomor'],
            request.form['tanggal_bukti'],
            request.form['uraian'],
            request.form['satuan'],
            int(request.form['jumlah']),
            int(request.form['harga_satuan']),
            int(request.form['total_harga']),
            request.form['keterangan']
        )
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
                INSERT INTO barang (
                    tanggal, dari, nomor, tanggal_bukti, uraian, satuan, jumlah,
                    harga_satuan, total_harga, keterangan
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

            # Update stok
            cur = conn.cursor()
            cur.execute("SELECT * FROM stok WHERE nama=?", (data[4],))
            existing = cur.fetchone()
            if existing:
                conn.execute("UPDATE stok SET jumlah=jumlah+? WHERE nama=?", (data[6], data[4]))
            else:
                conn.execute("INSERT INTO stok (nama, satuan, jumlah) VALUES (?, ?, ?)", (data[4], data[5], data[6]))

        return redirect(url_for('barang_list'))
    return render_template('form_barang.html', data=None)

@app.route('/barang/edit/<int:id>', methods=['GET', 'POST'])
def barang_edit(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        if request.method == 'POST':
            # Ambil data lama untuk hitung stok
            cur.execute("SELECT uraian, jumlah FROM barang WHERE id=?", (id,))
            old_data = cur.fetchone()
            old_uraian, old_jumlah = old_data if old_data else ("", 0)

            # Data baru
            tanggal = request.form['tanggal']
            dari = request.form['dari']
            nomor = request.form['nomor']
            tanggal_bukti = request.form['tanggal_bukti']
            uraian = request.form['uraian']
            satuan = request.form['satuan']
            jumlah = int(request.form['jumlah'])
            harga_satuan = int(request.form['harga_satuan'])
            total_harga = int(request.form['total_harga'])
            keterangan = request.form['keterangan']

            # Update stok (kurangi yang lama)
            if old_uraian == uraian:
                cur.execute("UPDATE stok SET jumlah = jumlah - ? WHERE nama = ?", (old_jumlah, old_uraian))
                cur.execute("UPDATE stok SET jumlah = jumlah + ? WHERE nama = ?", (jumlah, uraian))
            else:
                cur.execute("UPDATE stok SET jumlah = jumlah - ? WHERE nama = ?", (old_jumlah, old_uraian))
                cur.execute("SELECT * FROM stok WHERE nama=?", (uraian,))
                existing = cur.fetchone()
                if existing:
                    cur.execute("UPDATE stok SET jumlah = jumlah + ? WHERE nama = ?", (jumlah, uraian))
                else:
                    cur.execute("INSERT INTO stok (nama, satuan, jumlah) VALUES (?, ?, ?)", (uraian, satuan, jumlah))

            # Update data barang
            cur.execute('''
                UPDATE barang SET
                    tanggal=?, dari=?, nomor=?, tanggal_bukti=?,
                    uraian=?, satuan=?, jumlah=?, harga_satuan=?,
                    total_harga=?, keterangan=? WHERE id=?
            ''', (tanggal, dari, nomor, tanggal_bukti, uraian, satuan, jumlah, harga_satuan, total_harga, keterangan, id))
            conn.commit()
            return redirect(url_for('barang_list'))
        else:
            cur.execute("SELECT * FROM barang WHERE id=?", (id,))
            row = cur.fetchone()
            return render_template('form_barang.html', data=row)

@app.route('/barang/hapus/<int:id>', methods=['GET'])
def barang_hapus(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT uraian, jumlah FROM barang WHERE id=?", (id,))
        row = cur.fetchone()
        if row:
            uraian, jumlah = row
            cur.execute("UPDATE stok SET jumlah = jumlah - ? WHERE nama = ?", (jumlah, uraian))
        conn.execute("DELETE FROM barang WHERE id=?", (id,))
    return redirect(url_for('barang_list'))

@app.route('/pengeluaran')
def list_pengeluaran():
    if 'username' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM pengeluaran ORDER BY tanggal DESC")
        rows = cur.fetchall()
    return render_template('list_pengeluaran.html', data=rows)

@app.route('/api/get-stock-items')
def get_stock_items():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT nama, satuan, jumlah FROM stok WHERE jumlah > 0 ORDER BY nama")
        items = [dict(row) for row in cur.fetchall()]
    
    return jsonify(items)

@app.route('/pengeluaran/tambah', methods=['GET', 'POST'])
def pengeluaran_tambah():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = ''
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        uraian = request.form['uraian']
        satuan = request.form['satuan']
        jumlah = int(request.form['jumlah'])
        penerima = request.form.get('penerima', '')
        keterangan = request.form.get('keterangan', '')

        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT jumlah FROM stok WHERE nama=?", (uraian,))
            stok = cur.fetchone()

            if stok and stok[0] >= jumlah:
                cur.execute("""
                    INSERT INTO pengeluaran 
                    (tanggal, uraian, satuan, jumlah, penerima, keterangan) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (tanggal, uraian, satuan, jumlah, penerima, keterangan))
                cur.execute("UPDATE stok SET jumlah = jumlah - ? WHERE nama = ?", (jumlah, uraian))
                conn.commit()
                return redirect(url_for('list_pengeluaran'))
            else:
                error = "Stok tidak mencukupi atau barang belum tersedia."

    # Get available items for dropdown
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT nama, satuan, jumlah FROM stok WHERE jumlah > 0 ORDER BY nama")
        stock_items = cur.fetchall()

    return render_template('form_pengeluaran.html', error=error, stock_items=stock_items)

@app.route('/stok')
def stok_barang():
    if 'username' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM stok ORDER BY nama")
        rows = cur.fetchall()
    return render_template('stok_barang.html', data=rows)

if __name__ == '__main__':
    if not os.path.exists('db'):
        os.makedirs('db')
    init_db()
    app.run(debug=True)
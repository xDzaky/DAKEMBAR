from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from datetime import datetime, timedelta
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey123'
DATA_FILE = 'db/data.json'

# Initialize data structure
def init_data():
    if not os.path.exists('db'):
        os.makedirs('db')
    if not os.path.exists(DATA_FILE):
        data = {
            "barang": [],
            "admin": [{"username": "admin", "password": "admin123", "role": "admin"}],
            "stok": [],
            "pengeluaran": [],
            "notifikasi": []
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

def load_data():
    if not os.path.exists(DATA_FILE):
        init_data()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Custom function to generate IDs
def get_next_id(items):
    return max([item['id'] for item in items] + [0]) + 1

# Improved InventoryManager class
class InventoryManager:
    @staticmethod
    def update_stock(nama, satuan, jumlah_change, min_stok=0):
        data = load_data()
        stok_items = data['stok']
        
        # Find existing item
        existing = next((item for item in stok_items if item['nama'] == nama), None)
        
        if existing:
            # Update jumlah stok
            existing['jumlah'] += jumlah_change
            if existing['jumlah'] < 0:
                existing['jumlah'] = 0
            
            # Update satuan jika berubah
            existing['satuan'] = satuan
            
            # Update min_stok jika diberikan
            if min_stok > 0:
                existing['min_stok'] = min_stok
        else:
            # Hanya buat item baru jika jumlah positif
            if jumlah_change > 0:
                new_item = {
                    'id': get_next_id(stok_items),
                    'nama': nama,
                    'satuan': satuan,
                    'jumlah': jumlah_change,
                    'min_stok': min_stok
                }
                stok_items.append(new_item)
        
        save_data(data)
        return existing['jumlah'] if existing else jumlah_change

    @staticmethod
    def check_stock(nama):
        data = load_data()
        item = next((item for item in data['stok'] if item['nama'] == nama), None)
        return item['jumlah'] if item else 0

    @staticmethod
    def recalculate_all_stock():
        """Menghitung ulang semua stok dari barang masuk dan pengeluaran"""
        data = load_data()
        
        # Reset semua stok
        stok_dict = {}
        
        # Hitung semua barang masuk
        for barang in data['barang']:
            if barang['uraian'] not in stok_dict:
                stok_dict[barang['uraian']] = {
                    'satuan': barang['satuan'],
                    'jumlah': 0
                }
            stok_dict[barang['uraian']]['jumlah'] += barang['jumlah']
        
        # Kurangi dengan semua pengeluaran
        for pengeluaran in data['pengeluaran']:
            if pengeluaran['uraian'] in stok_dict:
                stok_dict[pengeluaran['uraian']]['jumlah'] -= pengeluaran['jumlah']
        
        # Simpan ke data stok
        data['stok'] = []
        for nama, item in stok_dict.items():
            if item['jumlah'] > 0:  # Hanya simpan yang jumlahnya positif
                # Pertahankan min_stok dari data lama jika ada
                old_item = next((i for i in data['stok'] if i['nama'] == nama), None)
                min_stok = old_item['min_stok'] if old_item and 'min_stok' in old_item else 0
                
                data['stok'].append({
                    'id': get_next_id(data['stok']),
                    'nama': nama,
                    'satuan': item['satuan'],
                    'jumlah': item['jumlah'],
                    'min_stok': min_stok
                })
        
        save_data(data)

# Panggil ini saat startup untuk memastikan stok akurat
init_data()
InventoryManager.recalculate_all_stock()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data()
        admin = next((user for user in data['admin'] if user['username'] == username), None)
        
        if admin and admin['password'] == password:
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
        
        data = load_data()
        if any(user['username'] == username for user in data['admin']):
            msg = 'Username sudah terdaftar.'
        else:
            new_user = {
                'id': get_next_id(data['admin']),
                'username': username,
                'password': password,
                'role': 'user'
            }
            data['admin'].append(new_user)
            save_data(data)
            msg = 'Berhasil daftar, silakan login.'
            return redirect(url_for('login'))
    
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
    
    data = load_data()
    
    # Process barang masuk
    barang_masuk = []
    temp_data = {}
    for item in data['barang']:
        if start_date <= item['tanggal'] <= end_date:
            day = item['tanggal']
            temp_data[day] = temp_data.get(day, 0) + item['jumlah']
    
    barang_masuk = [{'day': day, 'total': total} for day, total in temp_data.items()]
    
    # Process pengeluaran
    pengeluaran = []
    temp_data = {}
    for item in data['pengeluaran']:
        if start_date <= item['tanggal'] <= end_date:
            day = item['tanggal']
            temp_data[day] = temp_data.get(day, 0) + item['jumlah']
    
    pengeluaran = [{'day': day, 'total': total} for day, total in temp_data.items()]
    
    # Low stock items
    low_stock = [item for item in data['stok'] if item['jumlah'] <= item['min_stok'] and item['min_stok'] > 0]
    
    # Statistics
    stats = {
        'total_barang': len(data['barang']),
        'total_pengeluaran': len(data['pengeluaran']),
        'total_stok': sum(item['jumlah'] for item in data['stok'])
    }
    
    return jsonify({
        'barang_masuk': barang_masuk,
        'pengeluaran': pengeluaran,
        'stats': stats,
        'low_stock': low_stock
    })

@app.route('/barang')
def barang_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    return render_template('list_barang.html', data=data['barang'])

@app.route('/barang/tambah', methods=['GET', 'POST'])
def barang_tambah():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            new_item = {
                'id': get_next_id(load_data()['barang']),
                'tanggal': request.form['tanggal'],
                'dari': request.form['dari'],
                'nomor': request.form['nomor'],
                'tanggal_bukti': request.form['tanggal_bukti'],
                'uraian': request.form['uraian'],
                'satuan': request.form['satuan'],
                'jumlah': int(request.form['jumlah']),
                'harga_satuan': float(request.form['harga_satuan']),
                'total_harga': float(request.form['total_harga']),
                'keterangan': request.form['keterangan']
            }
            
            data = load_data()
            data['barang'].append(new_item)
            save_data(data)
            
            # Update stock
            InventoryManager.update_stock(new_item['uraian'], new_item['satuan'], new_item['jumlah'])
            
            return redirect(url_for('barang_list'))
        except Exception as e:
            print(f"Error: {e}")
            return "Terjadi kesalahan saat menyimpan data", 500
    
    return render_template('form_barang.html', data=None)

@app.route('/barang/edit/<int:id>', methods=['GET', 'POST'])
def barang_edit(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    item_to_edit = next((item for item in data['barang'] if item['id'] == id), None)
    
    if not item_to_edit:
        return redirect(url_for('barang_list'))
    
    if request.method == 'POST':
        old_uraian = item_to_edit['uraian']
        old_jumlah = item_to_edit['jumlah']
        old_satuan = item_to_edit['satuan']
        
        # Update item data
        item_to_edit.update({
            'tanggal': request.form['tanggal'],
            'dari': request.form['dari'],
            'nomor': request.form['nomor'],
            'tanggal_bukti': request.form['tanggal_bukti'],
            'uraian': request.form['uraian'],
            'satuan': request.form['satuan'],
            'jumlah': int(request.form['jumlah']),
            'harga_satuan': float(request.form['harga_satuan']),
            'total_harga': float(request.form['total_harga']),
            'keterangan': request.form['keterangan']
        })
        
        # Recalculate stock if uraian or jumlah changed
        if old_uraian != item_to_edit['uraian'] or old_jumlah != item_to_edit['jumlah'] or old_satuan != item_to_edit['satuan']:
            # First remove the old stock
            InventoryManager.update_stock(old_uraian, old_satuan, -old_jumlah)
            # Then add the new stock
            InventoryManager.update_stock(item_to_edit['uraian'], item_to_edit['satuan'], item_to_edit['jumlah'])
        
        save_data(data)
        return redirect(url_for('barang_list'))
    
    return render_template('form_barang.html', data=item_to_edit)

@app.route('/barang/hapus/<int:id>', methods=['GET'])
def barang_hapus(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    item_to_delete = next((item for item in data['barang'] if item['id'] == id), None)
    
    if item_to_delete:
        # Update stock by removing the deleted item's quantity
        InventoryManager.update_stock(item_to_delete['uraian'], item_to_delete['satuan'], -item_to_delete['jumlah'])
        
        # Remove item
        data['barang'] = [item for item in data['barang'] if item['id'] != id]
        save_data(data)
    
    return redirect(url_for('barang_list'))

@app.route('/pengeluaran')
def list_pengeluaran():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    pengeluaran_data = []
    for item in data['pengeluaran']:
        pengeluaran_data.append({
            'id': item['id'],
            'tanggal': item['tanggal'],
            'uraian': item['uraian'],
            'satuan': item['satuan'],
            'jumlah': item['jumlah'],
            'penerima': item['penerima'],
            'keterangan': item.get('keterangan', '')
        })
    
    return render_template('list_pengeluaran.html', data=pengeluaran_data)

@app.route('/api/get-stock-items')
def get_stock_items():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = load_data()
    items = [{'nama': item['nama'], 'satuan': item['satuan'], 'jumlah': item['jumlah']} 
             for item in data['stok'] if item['jumlah'] > 0]
    return jsonify(items)

@app.route('/pengeluaran/tambah', methods=['GET', 'POST'])
def pengeluaran_tambah():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    error = ''
    data = load_data()
    
    if request.method == 'POST':
        uraian = request.form['uraian']
        jumlah = int(request.form['jumlah'])
        satuan = request.form['satuan']
        
        available_stock = InventoryManager.check_stock(uraian)
        
        if available_stock >= jumlah:
            new_pengeluaran = {
                'id': get_next_id(data['pengeluaran']),
                'tanggal': request.form['tanggal'],
                'uraian': uraian,
                'satuan': satuan,
                'jumlah': jumlah,
                'penerima': request.form.get('penerima', ''),
                'keterangan': request.form.get('keterangan', '')
            }
            
            data['pengeluaran'].append(new_pengeluaran)
            # Update stock by subtracting the quantity
            InventoryManager.update_stock(uraian, satuan, -jumlah)
            save_data(data)
            
            return redirect(url_for('list_pengeluaran'))
        else:
            error = "Stok tidak mencukupi atau barang belum tersedia."
    
    stock_items = [item for item in data['stok'] if item['jumlah'] > 0]
    return render_template('form_pengeluaran.html', error=error, stock_items=stock_items)

@app.route('/pengeluaran/hapus/<int:id>', methods=['GET'])
def pengeluaran_hapus(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    item_to_delete = next((item for item in data['pengeluaran'] if item['id'] == id), None)
    
    if item_to_delete:
        # Update stock by adding back the deleted item's quantity
        InventoryManager.update_stock(item_to_delete['uraian'], item_to_delete['satuan'], item_to_delete['jumlah'])
        
        # Remove item
        data['pengeluaran'] = [item for item in data['pengeluaran'] if item['id'] != id]
        save_data(data)
    
    return redirect(url_for('list_pengeluaran'))

@app.route('/stok')
def stok_barang():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Pastikan stok selalu terupdate
    InventoryManager.recalculate_all_stock()
    
    data = load_data()
    stok_data = []
    for item in data['stok']:
        stok_data.append({
            'id': item['id'],
            'nama': item['nama'],
            'satuan': item['satuan'],
            'jumlah': item['jumlah'],
            'min_stok': item.get('min_stok', 0)
        })
    
    return render_template('stok_barang.html', data=stok_data)

@app.route('/stok/set-min-stok', methods=['POST'])
def set_min_stok():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    nama = request.form.get('nama')
    min_stok = int(request.form.get('min_stok', 0))
    
    data = load_data()
    item = next((item for item in data['stok'] if item['nama'] == nama), None)
    
    if item:
        item['min_stok'] = min_stok
        save_data(data)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
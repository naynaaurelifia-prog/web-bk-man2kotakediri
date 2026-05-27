from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Konfigurasi Database (SQLite)
basedir = os.path.abspath(os.path.dirname(__file__))
# Gunakan database di folder /tmp agar Vercel tidak error saat mencoba membaca/menulis
db_path = os.path.join('/tmp', 'pelanggaran.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Tabel
class Pelanggaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_siswa = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    jenis_pelanggaran = db.Column(db.String(100), nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)
    pelapor = db.Column(db.String(100))

# Buat database otomatis saat dijalankan
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/petugas', methods=['GET', 'POST'])
def petugas():
    if request.method == 'POST':
        nama = request.form.get('nama_siswa')
        kls = request.form.get('kelas')
        pel = request.form.get('pelanggaran')
        
        # Nama guru otomatis (Tanpa NIP sesuai request)
        guru = "Dra. Sri Wahyuningsih"
        
        data_baru = Pelanggaran(nama_siswa=nama, kelas=kls, jenis_pelanggaran=pel, pelapor=guru)
        db.session.add(data_baru)
        db.session.commit()
        return redirect(url_for('guru'))
        
    return render_template('petugas.html')
    


@app.route('/login_siswa', methods=['GET', 'POST'])
def login_siswa():
    if request.method == 'POST':
        nisn = request.form.get('nisn')
        password = request.form.get('password')

        user = Siswa.query.filter_by(nisn=nisn, password=password).first()
        if user:
            return redirect(url_for('dashboard_siswa'))
        else:
            return "Login Gagal, Cek NISN/Password!"
    return render_template('login_siswa.html')

    
@app.route('/siswa', methods=['GET', 'POST'])
def siswa():
    hasil = None
    nama_input = ""
    if request.method == 'POST':
        nama_input = request.form.get('nama')
        hasil = Pelanggaran.query.filter(Pelanggaran.nama_siswa.like(f'%{nama_input}%')).all()
    return render_template('siswa.html', hasil=hasil, nama_dicari=nama_input)

@app.route('/guru')
def guru():
    laporan_semua = Pelanggaran.query.order_by(Pelanggaran.waktu.desc()).all()
    return render_template('guru.html', laporan=laporan_semua)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

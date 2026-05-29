import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. DEFINISIKAN BASEDIR DULU (Biar Python tahu jalan foldernya)
basedir = os.path.abspath(os.path.dirname(__file__))

# 2. KONFIGURASI DATABASE & SECRET KEY
app.config['SECRET_KEY'] = 'berylaurel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database_bk.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. KONEKSIKAN DATABASE KE APP
db = SQLAlchemy(app)

# 2. MODEL DATABASE
class Riwayat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_siswa = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    jenis_pelanggaran = db.Column(db.String(100), nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

# 3. ROUTES (LOGIKA WEB)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/petugas', methods=['GET', 'POST'])
def petugas():
    if request.method == 'POST':
        nama = request.form.get('nama_siswa')
        kelas = request.form.get('kelas')
        pelanggaran = request.form.get('jenis_pelanggaran')
        
        laporan_baru = Riwayat(nama_siswa=nama, kelas=kelas, jenis_pelanggaran=pelanggaran)
        db.session.add(laporan_baru)
        db.session.commit()
        
        flash("Laporan Berhasil Terkirim ke Guru BK!")
        return redirect(url_for('petugas')) 
        
    return render_template('petugas.html')

@app.route('/guru')
def guru():
    nama_bk = request.args.get('nama', 'Guru BK')
    semua_laporan = Riwayat.query.all()
    return render_template('guru.html', riwayat=semua_laporan, nama_guru=nama_bk)

@app.route('/hapus/<int:id>')
def hapus_laporan(id):
    laporan = Riwayat.query.get(id)
    if laporan:
        db.session.delete(laporan)
        db.session.commit()
    return redirect(url_for('guru')) # Diubah ke url_for('guru') agar lebih aman di hosting

if __name__ == "__main__":
    app.run(debug=True)

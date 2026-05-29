import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'berylaurel'
# Gunakan alamat absolut ke /tmp/ agar Vercel tidak bisa menolak
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data_bk_man2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Riwayat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_siswa = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    jenis_pelanggaran = db.Column(db.String(100), nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)

# Fungsi buat mastiin database dibuat tanpa bikin error saat startup
def buat_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/petugas', methods=['GET', 'POST'])
def petugas():
    buat_db() # Buat database saat ada data masuk pertama kali
    if request.method == 'POST':
        nama = request.form.get('nama_siswa')
        kelas = request.form.get('kelas')
        pelanggaran = request.form.get('jenis_pelanggaran')
        
        laporan_baru = Riwayat(nama_siswa=nama, kelas=kelas, jenis_pelanggaran=pelanggaran)
        db.session.add(laporan_baru)
        db.session.commit()
        
        flash("Laporan Berhasil Terkirim!")
        return redirect(url_for('petugas')) 
    return render_template('petugas.html')

@app.route('/guru')
def guru():
    buat_db()
    nama_bk = request.args.get('nama', 'Guru BK')
    try:
        semua_laporan = Riwayat.query.all()
    except:
        semua_laporan = []
    return render_template('guru.html', riwayat=semua_laporan, nama_guru=nama_bk)

@app.route('/hapus/<int:id>')
def hapus_laporan(id):
    laporan = Riwayat.query.get(id)
    if laporan:
        db.session.delete(laporan)
        db.session.commit()
    return redirect(url_for('guru'))

if __name__ == "__main__":
    app.run(debug=True)

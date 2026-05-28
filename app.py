from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Konfigurasi Database - Gunakan V3 biar bener-bener fresh
db_path = os.path.join('/tmp', 'database_v3.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Database
class Pelanggaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_siswa = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    kelas = db.Column(db.String(20), default='10')

# Buat Database dan Isi Nama Teman
with app.app_context():
    db.create_all()
    # Daftar nama temanmu
    teman = {
        'AFRIALDY': 'afrialdy123', 'AHMAD FAIRUZ NADHIR AMRULLOH': 'faiz123',
        'AHMADA DAKA ELJEISA FATIR': 'jesa123', 'ANNISA AZIZAH NUR AQLIS': 'annisa123',
        'ASHFA ALYA': 'ashfa123', 'CINTA TARISA': 'cinta123',
        'DAMAR SATRIO WIBOWO': 'damar123', 'DEVINA AURALIA IMANDA PUTRI': 'devina123',
        'CAKRA PAMBAYUN': 'cakra123', 'GAYATRI NASTITI DWI HAPSARI': 'aya123',
        'HABLY WAFIROTAL IZZAH': 'hably123', 'IQLIMA AINUN HANIFAH': 'hani123',
        'JASMINE PRAMESWARI WAHYUDI': 'jasmine123', 'KALILA SALSABILA': 'kalila123',
        'MALVA ANASIRUL RAHMAH': 'malva123', 'MOH.ANANDA RIZKY FAUZI': 'rizky123',
        'MUHAMMAD DAVIN REZQYANO': 'davin123', 'MUHAMMAD GALVIN SOBIRIN': 'galvin123',
        'MUHAMMAD HAFIDZUL BAYDHOWI': 'owi123', 'MUHAMMAD HAFIDZUS SALAM': 'salam123',
        'NADHIFA AQILAH': 'nadhifa123', 'NAYNA KEISYA AURELIFIA': 'nayna123',
        'NUZULIKHAN LANGIT ALFASANAH': 'zulkha123', 'OBBIE ABRAR RASHEESA': 'obbie123',
        'PRINCESS ANNABELLE RAHMA HUWAIDA': 'abel123', 'PUTRI AYU AURA RAMADHANI': 'ayu123',
        'RADITHYA ALTHAF HUDA RAMADHAN': 'althaf123', 'RAFA WAHYUZAKY ANANDIKA': 'rafa123',
        'RAJA AULIA RIZQY PRIHARTONO': 'raja123', 'SEPTHIA PUTRI WAGITA': 'tia123',
        'STEFANIE QUEEN': 'fani123', 'SYIFA AMELIA ARTANTI': 'syifa123',
        'TANAYA RISWANA MAHARANI': 'naya123', 'VERRINSYANA VHIMALA': 'vivi123',
        'ZIANKA QOLBI UDZMA ISLAMEY': 'zizi123'
    }
    for nama, pw in teman.items():
        if not Pelanggaran.query.filter_by(nama_siswa=nama).first():
            db.session.add(Pelanggaran(nama_siswa=nama, password=pw))
    db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login_siswa', methods=['GET', 'POST'])
def login_siswa():
    if request.method == 'POST':
        nama_input = request.form.get('nama')
        pw_input = request.form.get('password')
        user = Pelanggaran.query.filter_by(nama_siswa=nama_input).first()
        if user and user.password == pw_input:
            return redirect(url_for('siswa'))
        return "Login Gagal! Cek Nama (KAPITAL) & Password."
    return render_template('login_siswa.html')

@app.route('/siswa')
def siswa():
    return "Selamat datang di halaman siswa!"

if __name__ == "__main__":
    app.run(debug=True)

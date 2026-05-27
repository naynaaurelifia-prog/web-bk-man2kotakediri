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
    with app.app_context():
    db.create_all()
    
    data_kelas = {
        'AFRIALDY': 'afrialdy123',
        'AHMAD FAIRUZ NADHIR AMRULLOH': 'faiz123',
        'AHMADA DAKA ELJEISA FATIR': 'jesa123',
        'ANNISA AZIZAH NUR AQLIS': 'annisa123',
        'ASHFA ALYA': 'ashfa123',
        'CINTA TARISA': 'cinta123',
        'DAMAR SATRIO WIBOWO': 'damar123',
        'DEVINA AURALIA IMANDA PUTRI': 'devina123',
        'CAKRA PAMBAYUN': 'cakra123',
        'GAYATRI NASTITI DWI HAPSARI': 'aya123',
        'HABLY WAFIROTAL IZZAH': 'hably123',
        'IQLIMA AINUN HANIFAH': 'hani123',
        'JASMINE PRAMESWARI WAHYUDI': 'jasmine123',
        'KALILA SALSABILA': 'kalila123',
        'MALVA ANASIRUL RAHMAH': 'malva123',
        'MOH.ANANDA RIZKY FAUZI': 'rizky123',
        'MUHAMMAD DAVIN REZQYANO': 'davin123',
        'MUHAMMAD GALVIN SOBIRIN': 'galvin123',
        'MUHAMMAD HAFIDZUL BAYDHOWI': 'owi123',
        'MUHAMMAD HAFIDZUS SALAM': 'salam123',
        'NADHIFA AQILAH': 'nadhifa123',
        'NAYNA KEISYA AURELIFIA': 'nayna123',
        'NUZULIKHAN  LANGIT  ALFASANAH': 'zulkha123',
        'OBBIE ABRAR RASHEESA': 'obbie123',
        'PRINCESS ANNABELLE RAHMA HUWAIDA': 'abel123',
        'PUTRI AYU AURA RAMADHANI': 'ayu123',
        'RADITHYA ALTHAF HUDA RAMADHAN': 'althaf123',
        'RAFA WAHYUZAKY ANANDIKA': 'rafa123',
        'RAJA AULIA RIZQY PRIHARTONO': 'raja123',
        'SEPTHIA PUTRI WAGITA': 'tia123',
        'STEFANIE QUEEN': 'fani123',
        'SYIFA AMELIA ARTANTI': 'syifa123',
        'TANAYA RISWANA MAHARANI': 'naya123',
        'VERRINSYANA VHIMALA': 'vivi123',
        'ZIANKA QOLBI UDZMA ISLAMEY': 'zizi123' 
    }
    
    for nama, pw in data_kelas.items():
        cek_siswa = Pelanggaran.query.filter_by(nama_siswa=nama).first()
        if not cek_siswa:
            siswa_baru = Pelanggaran(nama_siswa=nama, password=pw, kelas='10')
            db.session.add(siswa_baru)
    
    db.session.commit()
    print("Data kelas berhasil disuntikkan!")

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
        Nama_input = request.form.get('Nama')
        password_input = request.form.get('password')

        user = Pelanggaran.query.filter_by(Nama_Siswa=Nama_input).first()
        if user and use.password == password_input:
            return redirect(url_for('Siswa'))
        else:
            return "Login Gagal, Cek Nama/Password!"
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

from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = 'berylaurel3108'
SUPABASE_URL = "https://owxkabzlenxmpoyuyttm.supabase.co"
SUPABASE_KEY = "sb_publishable_7f4QJTIGVa-g1e8gOt5v_w_VsjWdUj2"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# List nama teman-teman kamu (Utuh & Aman!)
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

@app.route('/')
def home():
    return render_template('index.html')

# === RUTE TAMBAH PELANGGARAN ===
@app.route('/tambah_pelanggaran', methods=['GET', 'POST'])
def tambah_pelanggaran():
    if request.method == 'POST':
        nama_dari_form = request.form.get('nama_siswa')
        kelas_dari_form = request.form.get('kelas')
        pelanggaran_dari_form = request.form.get('pelanggaran')
        tanggal_dari_form = request.form.get('tanggal_waktu')
        
        data = {
            "nama_siswa": nama_dari_form,
            "kelas": kelas_dari_form,
            "pelanggaran": pelanggaran_dari_form,
            "tanggal_waktu": tanggal_dari_form
        }
        supabase.table("Pelanggaran").insert(data).execute()
        return "<script>alert('Laporan Telah Terkirim ke Guru BK'); window.location.href='/';</script>"
        
    return redirect(url_for('home'))

# === RUTE LOGIN SISWA (SUDAH ADA!) ===
@app.route('/login_siswa', methods=['GET', 'POST'])
def login_siswa():
    if request.method == 'POST':
        nama_input = request.form.get('nama')
        pw_input = request.form.get('password')
        
        if nama_input in teman and teman[nama_input] == pw_input:
            return redirect(url_for('siswa', nama=nama_input))
        return "Login Gagal! Cek Nama (KAPITAL) & Password."
    return render_template('login_siswa.html')

@app.route('/siswa')
def siswa():
    nama_user = request.args.get('nama', 'SISWA')
    respon = supabase.table("Pelanggaran").select("*").eq("nama_siswa", nama_user).execute()
    riwayat = respon.data
    return render_template('siswa.html', siswa={'nama_siswa': nama_user}, riwayat=riwayat)

@app.route('/petugas')
def petugas():
    return render_template('petugas.html')

# === RUTE LOGIN GURU ===
@app.route('/login_guru', methods=['GET', 'POST'])
def login_guru():
    if request.method == 'POST':
        nama_input = request.form.get('nama_guru')
        pw_input = request.form.get('password')
        if pw_input == 'IECM2KK':
            return redirect(url_for('guru', nama=nama_input))
        return "Login Guru Gagal! Password Admin Salah."
    return render_template('login_guru.html')

@app.route('/guru')
def guru():
    nama_bk = request.args.get('nama', 'Guru BK')
    respon = supabase.table("Pelanggaran").select("*").execute()
    semua_data = respon.data
    return render_template('guru.html', data_pelanggaran=semua_data, nama_guru=nama_bk)

# === RUTE HAPUS ===
@app.route('/hapus_pelanggaran/<int:id_laporan>')
def hapus_pelanggaran(id_laporan):
    supabase.table("Pelanggaran").delete().eq("id", id_laporan).execute()
    return "<script>alert('Data Berhasil Dihapus'); window.location.href='/guru';</script>"

if __name__ == "__main__":
    app.run(debug=True)

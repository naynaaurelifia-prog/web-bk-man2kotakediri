<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lapor Pelanggaran - BK MAN 2 KOTA KEDIRI</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* CSS TETAP PAKAI PUNYAMU YANG KEREN */
        body {
            background: linear-gradient(135deg, rgba(45, 62, 150, 0.9) 0%, rgba(26, 37, 90, 0.95) 100%), 
                        url("{{ url_for('static', filename='1000107070.jpg') }}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .card {
            background: white;
            width: 90%;
            max-width: 400px;
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            animation: fadeIn 0.5s ease;
        }

        .header {
            background-color: #2d3e96;
            color: white;
            padding: 40px 20px;
            border-bottom-left-radius: 50px;
            border-bottom-right-radius: 50px;
            text-align: center;
        }

        .header h2 {
            margin: 0;
            font-size: 1.5em;
            letter-spacing: 1px;
        }

        .form-content {
            padding: 30px 25px;
        }

        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        
        input, select {
            width: 100%;
            padding: 15px 20px;
            border: 1.5px solid #ccc;
            border-radius: 30px; 
            box-sizing: border-box;
            font-size: 0.95em;
            outline: none;
            transition: 0.3s;
        }

        input:focus, select:focus {
            border-color: #2d3e96;
            box-shadow: 0 0 8px rgba(45, 62, 150, 0.2);
        }

        .btn-submit {
            background-color: #2d3e96;
            color: white;
            border: none;
            width: 100%;
            padding: 16px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 1em;
            cursor: pointer;
            margin-top: 10px;
            transition: 0.3s;
        }

        .btn-submit:hover {
            background-color: #1a255a;
            transform: translateY(-2px);
        }

        .btn-back {
            display: inline-block;
            margin-top: 15px;
            text-decoration: none;
            color: #666;
            font-size: 0.85em;
        }

        /* Style tambahan buat pesan sukses agar tidak nabrak */
        .alert-success {
            background-color: #d4edda; 
            color: #155724; 
            padding: 12px; 
            border-radius: 20px; 
            margin: 20px 25px 0 25px; /* Margin biar pas di tengah card */
            text-align: center; 
            font-size: 0.85em; 
            border: 1px solid #c3e6cb;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    
    <div class="card">
        <div class="header">
            <h2>Masuk sebagai petugas</h2>
        </div>

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert-success">
                        <i class="fa fa-check-circle"></i> {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    
        <div class="form-content">
            <form action="/petugas" method="POST">
                
                <div class="form-group">
                    <input type="text" name="nama_siswa" placeholder="Nama Siswa Yang Melanggar" required>
                </div>

                <div class="form-group">
                    <input type="text" name="kelas" placeholder="Kelas Siswa (Contoh: X-10)" required>
                </div>

                <div class="form-group">
                    <select name="jenis_pelanggaran" required>
                        <option value="" disabled selected>Pilih Jenis Pelanggaran</option>
                        <option value="Terlambat">Terlambat</option>
                        <option value="Atribut Tidak Lengkap">Atribut Tidak Lengkap</option>
                        <option value="Bolos">Bolos</option>
                        <option value="Rambut Tidak Rapi">Rambut Tidak Rapi</option>
                        <option value="Lainnya">Lainnya</option>
                    </select>
                </div>

                <button type="submit" class="btn-submit">Kirim Laporan</button>
            </form>
            
            <center>
                <a href="/" class="btn-back">← Kembali ke Menu Utama</a>
            </center>
        </div>
    </div>

</body>
</html>

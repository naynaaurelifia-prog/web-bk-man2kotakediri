import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. KONFIGURASI DATABASE & SECRET KEY
# Kita pakai /tmp/ langsung supaya Vercel tidak menolak (Read-Only Error)
app.config['SECRET_KEY'] = 'berylaurel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database_bk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. KONEKSIKAN DATABASE KE APP
db = SQLAlchemy(app)

# 3. MODEL DATABASE
class Riwayat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_siswa = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    jenis_pelanggaran = db.Column(db.String(100), nullable=False)
    waktu

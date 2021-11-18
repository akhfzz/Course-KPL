from operator import pos
import sys 
sys.path.append('...')
from config import app 
from app.controls import ControlDB
from app.models import db, User, Postingan, Penyimpanan, Penyuka, Komentar, Pertemanan, Resep
from passlib.hash import sha256_crypt
from flask import render_template, request, redirect, flash, url_for, session

#pendaftaran user
@app.route('/registrasi', methods=['GET', 'POST'])
def registrasi_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = sha256_crypt.hash(password)

        check_data_user = User.query.filter_by(email=email).first()
        if check_data_user is not None:
            flash(f'Email {email} telah terdaftar', 'info')
            return render_template('register.html')
        
        try:
            input = User(username=username, email=email, password=password_hash)
            db.session.add(input)
            db.session.commit()
            flash('Pendaftaran mu berhasil', 'success')
            return redirect(url_for('login_user'))
        except:
            flash(f'Data terhalangi dari duplikasi', 'warning')
            return render_template('register.html')
    return render_template('register.html')

#login user
@app.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check_data_user = User.query.filter_by(username=username).first()
        try:
            if sha256_crypt.verify(password, check_data_user.password):
                session['username'] = username
                session['id_user'] = check_data_user.id
                return redirect(url_for('profil_user'))
            else:
                flash('Kata sandi salah', 'info')
                return render_template('login.html')
        except:
            flash('Kamu belum mendaftar', 'warning')
    return render_template('login.html')

#profil user
@app.route('/login/profil', methods=['POST', 'GET'])
def profil_user():
    if request.method == 'POST':
        judul = request.form['judul']
        file = request.form['file'].encode()
        
        session['bahan'] = judul

        postingan_check = Postingan.query.filter_by(judul=judul).first()
        if postingan_check is not None:
            flash('Menu ini sudah ada, ayo berkreasi yang baru :)')
            return render_template('profil.html')
        
        foreign_user = User.query.filter_by(username=session['username']).first()
        input = Postingan(judul=judul, file=file, postingan=foreign_user)
        db.session.add(input)
        db.session.commit()
        return redirect(url_for('bahan_masakan'))
    return render_template('profil.html', username=session['username'])

@app.route('/login/profil/bahan', methods=['POST', 'GET'])
def bahan_masakan():
    if request.method == 'POST':
        jumlah_bahan = request.form['jumlah_bahan']
        bahan_mentah = request.form['bahan']
        satuan = request.form['satuan']
        postingan = Postingan.query.filter_by(judul=session['bahan']).first()
        check_resep = Resep.query.filter_by(bahan=bahan_mentah).filter_by(resep=postingan).first()
        if check_resep is not None:
            flash('Bahan harus bervariasi', 'info')
            return render_template('bahan.html')
        
        postingan = Postingan.query.filter_by(judul=session['bahan']).first()
        input = Resep(jumlah_bahan=jumlah_bahan, bahan=bahan_mentah, resep=postingan, satuan=satuan)
        db.session.add(input)
        db.session.commit()
        # return redirect(url_for('profil_user', username))
        resep_ku = Resep.query.filter_by(resep=postingan).all()
        return render_template('bahan.html', bahan_mentah=resep_ku)
    return render_template('bahan.html', username=session['username'], bahan=session['bahan'])

@app.route('/login/postingan')
def postingan_user():
    data = ControlDB()
    mysql = data.postingan_get(session['username'])
    if mysql is None:
        return render_template('postingan.html', error='Kamu belum memposting apapun')
    return render_template('postingan.html', data=mysql)



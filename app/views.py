from datetime import datetime
from datetime import *
from operator import pos
import sys 
sys.path.append('...')
from config import app 
from app.controls import ControlDB
from app.models import db
from passlib.hash import sha256_crypt
from flask import render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename

#pendaftaran user
@app.route('/registrasi', methods=['GET', 'POST'])
def registrasi_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = sha256_crypt.hash(password)

        data = ControlDB()
        check_data_user = data.select_user_byemail(email)
        if check_data_user is not None:
            flash(f'Email {email} telah terdaftar', 'info')
            return render_template('register.html')
        
        try:
            tipes = (username, password_hash, email)
            data.insert_user(tipes)
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
        data = ControlDB()
        check_data_user = data.select_user(username) 
        try:
            if sha256_crypt.verify(password, check_data_user['password']):
                session['username'] = username
                session['id_user'] = check_data_user['password']
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
    data = ControlDB()
    usr = data.select_user(session['username'])
    follower = data.count_following(usr['id'])

    if request.method == 'POST':
        judul = request.form['judul']
        file = request.files['file']
        
        session['bahan'] = judul

        postingan_check = data.select_postingan_byjudul(judul)

        if postingan_check is not None:
            flash('Menu ini sudah ada, ayo berkreasi yang baru :)', 'info')
            return render_template('profil.html')
        
        foreign_user = data.select_user(session['username'])

        directory = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(file.filename)
        file.save(directory)

        tipes = (foreign_user['id'], judul, secure_filename(file.filename), datetime.now())
        data.insert_postingan(tipes)

        return redirect(url_for('bahan_masakan'))
    return render_template('profil.html', username=session['username'], follower=follower)

@app.route('/login/profil/bahan', methods=['POST', 'GET'])
def bahan_masakan():
    if request.method == 'POST':
        jumlah_bahan = request.form['jumlah_bahan']
        bahan_mentah = request.form['bahan']
        satuan = request.form['satuan']

        data = ControlDB()
        postingan = data.select_postingan_byjudul(session['bahan'])
        check_resep = data.select_resep_bybahanid(bahan_mentah, postingan['id'])

        if check_resep is not None:
            flash('Bahan harus bervariasi', 'info')
            return render_template('bahan.html')

        tipes = (postingan['id'], jumlah_bahan, satuan, bahan_mentah)
        data.insert_resep(tipes)
        
        resepku = data.select_resep_byid(postingan['id'])
        
        return render_template('bahan.html', bahan_mentah=resepku, x=0)
    return render_template('bahan.html', username=session['username'], bahan=session['bahan'])

@app.route('/login/postingan')
def postingan_user():
    data = ControlDB()
    mysql = data.postingan_get(session['username'])
    if mysql is None:
        flash('Kamu belum memposting', 'warning')
        return render_template('postingan.html')
    return render_template('postingan.html', data=mysql)

@app.route('/login/postingan/<id>', methods=['POST', 'GET'])
def hapus_resep(id:int):
    data = ControlDB()
    data.hapus_postingan(id)
    flash("Data berhasil dihapus", "success")
    return redirect(url_for('postingan_user'))

@app.route('/login/postingan/detail/<int:id>')
def detail_postingan(id):
    data = ControlDB()
    mysql = data.postingan_detail(id)
    like = data.count_like(id)
    usr = data.select_user(session['username'])
    comment = data.count_comment(id)
    pict = data.pict(id)
    field_comment = data.select_komentar_byid(id)
    for i in range(len(field_comment)):
        today = datetime.now()
        tanggalan = today.date() - field_comment[i]['tgl_comment']
        follow = data.select_following(field_comment[i]['id'])
        return render_template('detail.html', data=mysql, gambar=pict, count_like=like, count_comment=comment, field=field_comment, day=tanggalan.days, user=usr, follow=follow)
    return render_template('detail.html', data=mysql, gambar=pict, count_like=like, count_comment=comment, field=field_comment, user=usr)

@app.route('/login/global')
def global_page():
    data = ControlDB()
    mysql = data.postingan_global()
    usr_check = data.select_user(session['username'])
    likedislike = data.select_penyuka_oneparams(usr_check['id'])
    for i in range(len(mysql)):
        following = data.select_follows(usr_check['id'])
        return render_template("global.html", data=mysql, penyuka=likedislike, user=usr_check, following=following)
    return render_template("global.html", data=mysql, penyuka=likedislike, user=usr_check)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login_user'))

@app.route("/login/penyuka/<int:usrid>/<int:postid>", methods=['POST', 'GET'])
def penyuka(usrid, postid):
    if request.method == 'POST':
        data = ControlDB()
        tanggal = datetime.now()
        usr = data.select_user(session['username'])
        if data.select_penyuka(usr['id'], postid) is not None:
            data.dislike(usrid)
        else:
            data.menyukai_postingan(usr['id'], postid, tanggal)
        return redirect(url_for("global_page"))

@app.route("/login/komentar/<int:usrid>/<int:postid>", methods=['POST', 'GET'])
def komentar(usrid, postid):
    if request.method == 'POST':
        comment_field = request.form['comment_post']
        data = ControlDB()
        usr = data.select_user(session['username'])
        tanggal = datetime.now()
        tipes = (usr['id'], postid, tanggal, comment_field)
        data.insert_komentar(tipes)
        return redirect(url_for("global_page"))

@app.route("/login/mengikuti/<int:userid>/<int:followid>", methods=['POST', 'GET'])
def mengikuti(userid, followid):
    if request.method == 'POST':
        data = ControlDB()
        check = data.select_following(followid)
        if check is not None:
            data.hapus_pertemanan(userid, followid)
        else:
            tanggal = datetime.now()
            tipes = (userid, followid, tanggal)
            data.follow(tipes)
        return redirect(url_for("global_page"))

import sys
sys.path.append('..')

from config import db 
from datetime import *
from sqlalchemy.dialects.mysql import MEDIUMBLOB

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    #foreign key akses
    f_access2 = db.relationship('Pertemanan', backref='followed', cascade='all, delete', lazy='select')
    like = db.relationship('Penyuka', backref='like', cascade='all, delete', lazy='select')
    save = db.relationship('Penyimpanan', backref='save', cascade='all, delete', lazy='select')
    komentar = db.relationship('Komentar', backref='komentar', cascade='all, delete', lazy='select')
    postingan = db.relationship('Postingan', backref='postingan', cascade='all, delete', lazy='select')

class Pertemanan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follows = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    following = db.Column(db.Integer, nullable=False)
    tanggal = db.Column(db.Date, default=datetime.today())

class Penyuka(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    id_postingan = db.Column(db.Integer, db.ForeignKey('postingan.id', ondelete='CASCADE'))
    tanggal = db.Column(db.Date, default=datetime.today())

class Penyimpanan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    id_postingan = db.Column(db.Integer, db.ForeignKey('postingan.id', ondelete='CASCADE'))
    tanggal = db.Column(db.Date, default=datetime.today())

class Komentar(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    id_postingan = db.Column(db.Integer, db.ForeignKey('postingan.id', ondelete='CASCADE'))
    tgl_comment = db.Column(db.Date, default=datetime.today())
    comment_post = db.Column(db.String(255), nullable=False)

class Postingan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    file = db.Column(MEDIUMBLOB, nullable=False)
    judul = db.Column(db.String(150), nullable=False, unique=True)
    wkt_posting = db.Column(db.Date, default=datetime.today())
    #foreign key akses
    like = db.relationship('Penyuka', backref='likes', cascade='all, delete', lazy='select')
    save = db.relationship('Penyimpanan', backref='saved', cascade='all, delete', lazy='select')
    komentar = db.relationship('Komentar', backref='comments', cascade='all, delete', lazy='select')
    resep = db.relationship('Resep', backref='resep', cascade='all, delete', lazy='select')

class Resep(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_postingan = db.Column(db.Integer, db.ForeignKey('postingan.id', ondelete='CASCADE'))
    jumlah_bahan = db.Column(db.Integer, nullable=False)
    satuan = db.Column(db.String(50), nullable=False)
    bahan = db.Column(db.String(150), nullable=False)
    




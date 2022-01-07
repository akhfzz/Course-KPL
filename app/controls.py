import pymysql

db = cursor = None 

class ControlDB:
    def __init__(self):
        self.host='localhost'
        self.user='root'
        self.password=''
        self.database='kpl'

    def connecting(self):
        global db, cursor
        db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
    def close(self):
        global db, cursor
        db.close()

    def postingan_get(self, username):
        global db, cursor 
        self.connecting()
        cursor.execute(f"""
            SELECT
                p.id, p.judul, p.wkt_posting as waktu, p.file
            FROM 
                postingan p, user u
            WHERE 
                u.id=p.id_user AND u.username = '{username}'
        """)
        fetch = cursor.fetchall()
        return fetch

    def postingan_detail(self, id):
        global db, cursor
        self.connecting()
        cursor.execute(
            f"""
                SELECT
                    p.id_user, p.judul, p.wkt_posting, r.jumlah_bahan, r.satuan, r.bahan
                FROM 
                    postingan p, resep r
                WHERE 
                    p.id = r.id_postingan AND p.id = {id}
            """
        )
        fetch = cursor.fetchall()
        return fetch

    def pict(self, id):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT
                    p.file, p.judul
                FROM 
                    postingan p, resep r
                WHERE 
                    p.id = r.id_postingan AND p.id = {id}
            """
        )
        fetch = cursor.fetchone()
        return fetch

    def postingan_global(self):
        global db, cursor 
        self.connecting()
        cursor.execute(f"""
            SELECT
                p.id as postingan_id, p.judul, p.wkt_posting as waktu, p.file, u.username, u.id as user_id
            FROM 
                postingan p, user u
            WHERE p.id_user = u.id
        """)
        fetch = cursor.fetchall()
        return fetch
    
    def menyukai_postingan(self, userid, postinganid,tanggal):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                INSERT INTO PENYUKA (
                    id_user, id_postingan, tanggal
                ) values (
                    '{userid}', '{postinganid}', '{tanggal}'
                )
            """
        )
        db.commit()
        self.close()
    
    def select_penyuka(self, userid, postid):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM penyuka WHERE id_user={userid} AND id_postingan={postid}
            """
        )
        fetch = cursor.fetchone()
        return fetch
    
    def select_penyuka_oneparams(self, userid):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM penyuka WHERE id_user={userid}
            """
        )
        fetch = cursor.fetchone()
        return fetch

    def dislike(self, userid):
        global db, cursor
        self.connecting()
        cursor.execute(
            f"""
                DELETE FROM penyuka WHERE id_user={userid}
            """
        )
        db.commit()
        self.close()
    
    def select_user(self, username):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM user WHERE username='{username}'
            """
        )
        fetch = cursor.fetchone()
        return fetch

    def select_user_byemail(self, email):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM user WHERE email='{email}'
            """
        )
        fetch = cursor.fetchone()
        return fetch

    def insert_user(self, data):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                INSERT INTO user (
                    username, password, email
                ) VALUES(
                    '{data[0]}', '{data[1]}', '{data[2]}'
                )
            """
        )
        db.commit()
        self.close()
    
    def select_postingan_byjudul(self, judul):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM postingan WHERE judul='{judul}'
            """
        )
        return cursor.fetchone()
    
    def insert_postingan(self, data):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                INSERT INTO postingan (
                    id_user, judul, file, wkt_posting
                ) VALUES(
                    '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}'
                )
            """
        )
        db.commit()
        self.close()
    
    def select_resep_bybahanid(self, bahan, postid):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM resep WHERE bahan='{bahan}' AND id_postingan='{postid}'
            """
        )
        return cursor.fetchone()
    
    def insert_resep(self, data):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                INSERT INTO resep (
                    id_postingan, jumlah_bahan, satuan, bahan
                ) VALUES(
                    '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}'
                )
            """
        )
        db.commit()
        self.close()
    
    def select_resep_byid(self, postid):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM resep WHERE id_postingan='{postid}'
            """
        )
        return cursor.fetchall()
    
    def count_like(self, postid):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT COUNT(id) as penyuka, id_postingan FROM penyuka WHERE id_postingan='{postid}' GROUP BY id_postingan
            """
        )
        return cursor.fetchone()
    
    def count_comment(self, postid):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT COUNT(id) as komentar, id_postingan FROM komentar WHERE id_postingan='{postid}' GROUP BY id_postingan
            """
        )
        return cursor.fetchone()
    
    def insert_komentar(self, data):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                INSERT INTO komentar (
                    id_user, id_postingan, tgl_comment, comment_post
                )VALUES(
                    '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}'
                )
            """
        )
        db.commit()
        self.close()
    
    def select_komentar_byid(self, id):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT
                    u.id, u.username, k.comment_post as komentar, k.tgl_comment
                FROM 
                    user u, komentar k 
                WHERE 
                    u.id=k.id_user AND k.id_postingan='{id}' 
                ORDER BY k.tgl_comment DESC
            """
        )
        return cursor.fetchall()
    
    def hapus_postingan(self, id):
        global db, cursor
        self.connecting()
        cursor.execute(
            f"""
                DELETE FROM postingan WHERE id='{id}'
            """
        )
        db.commit()
        self.close()
    
    def follow(self, data):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                INSERT INTO pertemanan (
                    follows, following, tanggal
                )VALUES(
                    '{data[0]}', '{data[1]}', '{data[2]}'
                )
            """
        )
        db.commit()
        self.close()
    
    def select_following(self, id):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM pertemanan WHERE following='{id}'
            """
        )
        return cursor.fetchone()
    
    def select_follows(self, id):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                SELECT * FROM pertemanan WHERE follows='{id}'
            """
        )
        return cursor.fetchone()
    
    def hapus_pertemanan(self, follows, following):
        global db, cursor 
        self.connecting()
        cursor.execute(
            f"""
                DELETE FROM pertemanan WHERE following='{following}' and follows='{follows}'
            """
        )
        db.commit()
        self.close()
    
    def count_following(self, id):
        global db, cursor
        self.connecting()
        cursor.execute(
            f"""
                SELECT 
                    count(follows) as follower, following
                FROM 
                    pertemanan
                WHERE
                    following='{id}' GROUP BY following
            """
        )
        return cursor.fetchone()
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
                    p.judul, p.wkt_posting, r.jumlah_bahan, r.satuan, r.bahan
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
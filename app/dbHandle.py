import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('app.db')
        self.cursor = self.con.cursor()
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, nama_lengkap TEXT)")
            self.con.commit()
        except:
            pass
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, sdata TEXT)")
        self.con.commit()
    def saveData(self, dt):
        query = f"INSERT INTO data (sdata) VALUES ('{dt}')"
        self.cursor.execute(query)
        self.con.commit()
    def insert(self,nama,nama_lengkap):
        query = f"INSERT INTO user (nama,nama_lengkap) VALUES ('{nama}','{nama_lengkap}')"
        try:
            self.cursor.execute(query)
            self.con.commit()
            print(f"[INFO]:{query}")
            return True
        except:
            print(f"[INFO]:{query}")
            return False
    def getData(self):
        query = "SELECT * FROM data"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def getAllUser(self):
        self.cursor.execute("SELECT id, nama FROM user")
        return self.cursor.fetchall()
    def getByName(self, nama):
        self.cursor.execute(f"SELECT id, nama FROM user WHERE nama='{nama}'")
        return self.toDict(self.cursor.fetchall())
    def getById(self, idd):
        self.cursor.execute(f"SELECT * FROM user WHERE id={idd}")
        return self.cursor.fetchall()
    def toDict(self,arg):
        dic = {}
        for isi in arg:
            dic['id'] = isi[0]
            dic['nama'] = isi[1]
        return dic

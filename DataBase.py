import math, time, sqlite3
class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM posts'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: 
                return res
        except:
            #print ('Ошибка чтения из бд')
            return False
        return []
    
    def addPost(self, title, content):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (tm, title, content, 'черновик'))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))
            return False
        return True
    
    def updateStatus(self, statuss, pk):
        try:
            self.__cur.execute(f"UPDATE posts SET statuss=? WHERE id=?", (statuss, id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД: " + str(e))
            return False
        return True
    
            
    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, content FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            #print("Ошибка получения статьи из БД "+str(e))
            return False
        return (False, False)
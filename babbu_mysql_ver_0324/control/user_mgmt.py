from flask_login import UserMixin
from model.mysql import conn_mysqldb


class User(UserMixin):

    def __init__(self, id, user_id, user_pw):
        self.id = id
        self.user_id = user_id
        self.user_pw = user_pw

    def get_id(self):
        return str(self.user_id)

    def get_pw(self):
        return str(self.user_pw)

    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM members WHERE user_id = '" + str(user_id) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(id=user[0], user_id=user[1], user_pw=user[2])
        return user

    @staticmethod
    def create(user_id, user_pw):
        user = User.get(user_id)
        if user == None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO members (user_id, user_pw) VALUES ('%s', '%s')" % (
                str(user_id), str(user_pw))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.get(user_id)
        else:
            return user

    @staticmethod
    def find(id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM members WHERE id = '" + str(id) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        print(user)
        if not user:
            return None

        user = User(id=user[0], user_id=user[1], user_pw=user[2])
        return user

    @staticmethod
    def delete(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM user_info WHERE USER_ID = %d" % (user_id)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted


class Image(UserMixin):

    def __init__(self, id, user_id, user_im):
        self.id = id
        self.user_id = user_id
        self.user_im = user_im

    def get_id(self):
        return str(self.user_id)

    def get_pw(self):
        return str(self.user_im)

    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        print(user_id)
        sql = "SELECT * FROM images WHERE user_id = '" + str(user_id) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchall()
        if not user:
            return None

        # user = Image(id=user[0], user_id=user[1], user_im=user[2])
        return user

    @staticmethod
    def create(user_id, user_im):
        user = User.find(user_id)
        if user is not None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO images (user_id, image) VALUES ('%s', '%s')" % (
                str(user_id), str(user_im))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_id)
        else:
            return user

    @staticmethod
    def delete(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM user_info WHERE USER_ID = %d" % (user_id)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted


class Info(UserMixin):

    def __init__(self, id, user_id, weight):
        self.id = id
        self.user_id = user_id
        self.user_we = weight

    def get_id(self):
        return str(self.user_id)

    def get_pw(self):
        return str(self.user_we)

    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM info WHERE user_id = '" + str(user_id) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchall()
        if not user:
            return None

        return user

    @staticmethod
    def create(user_id, user_we):
        user = User.find(user_id)
        if user is not None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO info (user_id, weight) VALUES ('%s', '%s')" % (
                str(user_id), str(user_we))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_id)
        else:
            return user

    @staticmethod
    def find(id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT weight, date FROM info WHERE user_id = '" + str(id) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchall()
        print(user)
        if not user:
            return None

        return user

    @staticmethod
    def delete(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM info WHERE USER_ID = %d" % (user_id)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted

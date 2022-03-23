from flask_login import UserMixin
from model.mysql import conn_mysqldb


class User(UserMixin):

    def __init__(self, user_id, user_pw):
        self.id = user_id
        self.pw = user_pw

    def get_id(self):
        return str(self.id)

    def get_pw(self):
        return str(self.pw)

    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + str(user_id) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(user_id=user[0], user_pw=user[1])
        return user

    @staticmethod
    def find(user_pw):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_EMAIL = '" + \
            str(user_pw) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(user_id=user[0], user_pw=user[1])
        return user

    @staticmethod
    def create(user_id):
        user = User.find(user_id)
        if user == None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_info (USER_ID) VALUES ('%s')" % (
                str(user_id))
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

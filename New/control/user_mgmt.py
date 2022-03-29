from flask_login import UserMixin
from model.mysql import conn_mysqldb


class User(UserMixin):

    def __init__(self, Email, name, pw):
        self.Email = Email
        self.name = name
        self.pw = pw

    def get_Email(self):
        return str(self.Email)

    def get_pw(self):
        return str(self.pw)

    @staticmethod
    def get(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM ID WHERE Email = '" + str(Email) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(Email=user[0], name=user[1], pw=user[2])
        return user

    @staticmethod
    def create(Email, name, pw):
        user = User.get(Email)
        if user == None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO ID (Email, name, pw) VALUES ('%s', '%s', '%s')" % (
                str(Email), str(name), str(pw))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.get(Email)
        else:
            return user

    @staticmethod
    def find(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM ID WHERE Email = '" + str(Email) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        print(user)
        if not user:
            return None

        user = User(Email=user[0], name=user[1], pw=user[2])
        return user

    @staticmethod
    def delete(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM ID WHERE Email = %d" % (Email)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted


class Image(UserMixin):

    def __init__(self, Email, name, user_im):
        self.Email = Email
        self.name = name
        self.user_im = user_im

    def get_Email(self):
        return str(self.Email)

    def get_user_im(self):
        return str(self.user_im)

    @staticmethod
    def get(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        print(Email)
        sql = "SELECT * FROM images WHERE Email = '" + str(Email) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchall()
        if not user:
            return None

        user = Image(Email=user[0], name=user[1], user_im=user[2])
        return user

    @staticmethod
    def create(Email, name, user_im):
        user = Image.find(Email)
        if user is not None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO images (Eamil, name, user_im) VALUES ('%s', '%s', '%s')" % (
                str(Email), str(name), str(user_im))
            db_cursor.execute(sql)
            mysql_db.commit()
            return Image.find(Email)
        else:
            return user

    @staticmethod
    def delete(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM images WHERE Email = %d" % (Email)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted


class Info(UserMixin):

    def __init__(self, Email, age, sex, weight, height, exercise, disease, drink, smoke):
        self.Email = Email
        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height
        self.exercise = exercise
        self.disease = disease
        self.drink = drink
        self.smoke = smoke

    def get_Email(self):
        return str(self.Email)
    def get_age(self):
        return str(self.age)
    def get_weight(self):
        return str(self.weight)
    def get_height(self):
        return str(self.height)
    def get_sex(self):
        return str(self.sex)
    def get_exercise(self):
        return str(self.exercise)
    def get_disease(self):
        return str(self.disease)
    def get_drink(self):
        return str(self.drink)
    def get_smoke(self):
        return str(self.smoke)



    @staticmethod
    def get(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM userinfo WHERE Email = '" + str(Email) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchall()
        if not user:
            return None

        return user

    @staticmethod
    def create(Email, age, sex, weight, height, exercise, disease, drink, smoke):
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO userinfo (Email, age, sex, weight, height, exercise, disease, drink, smoke) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                str(Email), str(age), str(sex), str(weight), str(height), str(exercise), str(disease), str(drink), str(smoke))
            db_cursor.execute(sql)
            mysql_db.commit()
            return Info.get(Email)       


    @staticmethod
    def find(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM userinfo WHERE Email = '" + str(Email) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchall()
        print(user)
        if not user:
            return None

        return user

    @staticmethod
    def delete(Email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM userinfo WHERE Email = %d" % (Email)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted

from flask import Flask
from flask_restx import Api, Resource
from users.user_account import user_account
from users.user_info import user_info
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from controll.user_account_model import user_account_db
from controll.user_info_model import user_info_db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://lab05:lab05@localhost:3306/user"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
CORS(app)
user_account_db.init_app(app)
user_account_db.app = app
user_account_db.create_all()
user_info_db.init_app(app)
user_info_db.app = app
user_info_db.create_all()
api.add_namespace(user_account, '/user_account')
api.add_namespace(user_info, '/user_info')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8999')

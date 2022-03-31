from flask_login import UserMixin
import jwt


class User(UserMixin):

    def __init__(self, token):

        self.token = token

    @staticmethod
    def get(token):
        try:
            jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.exceptions.DecodeError:
            return None
        except jwt.ExpiredSignatureError:
            return None

        return token

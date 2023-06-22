from flask_login import UserMixin
from .models import Users

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = Users.query.get(int(user_id))
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

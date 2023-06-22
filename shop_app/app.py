from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from base64 import b64encode


app = Flask(__name__)
# добавляем БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop_base.db'
# ключ шифрования
app.config['SECRET_KEY'] = 'ba939b1b4903094baa3f81c3d55bb891ae476dbb'
# нужен для работы фильтра шаблонизатору Jinja2
app.jinja_env.filters['b64encode'] = b64encode
# объект БД
db = SQLAlchemy(app)
# объект миграции БД
migrate = Migrate(app, db)
# объект авторизации пользователей
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"
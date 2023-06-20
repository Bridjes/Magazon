from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode


app = Flask(__name__)
# добавляем БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop_base.db'
# нужен для работы фильтра шаблонизатору Jinja2
app.jinja_env.filters['b64encode'] = b64encode
# объект БД
db = SQLAlchemy(app)
migrate = Migrate(app, db)
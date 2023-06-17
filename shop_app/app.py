from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# добавляем БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop_base.db'
# объект БД
db = SQLAlchemy(app)
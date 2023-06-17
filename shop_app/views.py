from flask import render_template, request, redirect
from .app import app, db

# стартовая страница
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/item/add')
def admin_item_add():
    return render_template('admin_item_add.html')
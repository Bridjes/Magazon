from flask import render_template, request, redirect
from .app import app, db

# стартовая страница
@app.route('/')
def index():
    return render_template('index.html')
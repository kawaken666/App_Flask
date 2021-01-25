from show_data import app
from flask import request, redirect, url_for, render_template, flash, session

@app.route('/')
def login():
    return render_template('login.html')

from show_data import app
from flask import request, redirect, url_for, render_template, flash, session
from functools import wraps

# ログインしている場合にのみビュー処理を行うデコレータ。
# ログインしてない場合はログイン画面にリダイレクトする。
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return inner

# ルート画面表示（投稿一覧画面）
@app.route('/')
@login_required
def show():
    return render_template('show.html')

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('ユーザ名が異なります')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('パスワードが異なります')
        else:
            # セッションにlogged_in=Trueを格納する
            session['logged_in'] = True
            flash('ログインしました')
            return redirect(url_for('show'))
    return render_template('login.html')

# ログアウト
@app.route('/logout')
def logout():
    # ログアウト時、セッションのlogged_inをNoneに更新する
    session.pop('logged_in', None)
    flash('ログアウトしました')
    return redirect(url_for('show'))

# 存在しないURLへアクセスされた時の処理。ログイン画面にリダイレクト。
@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('login'))
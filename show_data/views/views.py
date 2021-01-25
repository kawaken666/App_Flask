from show_data import app, login_manager
from flask import request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict

#TODO:flask-loginの使い方と詳細を調査
### flask-loginを使うための前処理(begin)
class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

# ログイン用ユーザー作成
users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password")
}

# ユーザーチェックに使用する辞書作成
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))
### flask-loginを使うための前処理(end)


# ルート画面表示（投稿一覧画面）
@app.route('/')
def index():
    return render_template('login.html')

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # ユーザーチェック
        if (request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"]):
            # ユーザーが存在した場合はログイン
            login_user(users.get(user_check[request.form["username"]]["id"]))
            flash('ログインしました')
            return redirect(url_for('show'))
        else:
            #　ユーザーが存在しない場合はflashにエラー文言を格納
            flash('ユーザー名、または、パスワードが違います')
    return render_template('login.html')

# ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for('login'))

# 一覧表示画面
@app.route('/show')
@login_required
def show():
    return render_template('show.html')

# 存在しないURLへアクセスされた時の処理。ログイン画面にリダイレクト。
@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('login'))
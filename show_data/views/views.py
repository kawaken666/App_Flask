from show_data import app, login_manager, db
from flask import request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from show_data.models.users import User
from show_data.models.posts import Post

# ルート画面表示（ログイン画面）
@app.route('/')
def index():
    # ログインしている場合は投稿一覧画面にリダイレクトする
    if current_user.is_authenticated:
        return redirect(url_for('show'))
    # ログインしていない場合はログイン画面をレンダーする
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['GET', 'POST'])
def login():
    # POSTの場合
    if request.method == 'POST':
        # ログインしている場合は投稿一覧画面にリダイレクトする
        if current_user.is_authenticated:
            return redirect(url_for('show'))
        # リクエストフォームのemailをキーにUserテーブルからSELECTする
        user = User.query.filter_by(email=request.form['email']).first()
        # ユーザーが存在しない、またはパスワードが一致しない場合
        if user is None or not user.check_password(request.form['password']):
            flash('ユーザー名、または、パスワードが違います')
            return render_template('login.html')
        # ユーザーが存在してパスワードチェックも通った場合
        else:
            # flask-loginのlogin_userを呼び出してログイン状態にして、投稿一覧画面にリダイレクトする
            # 具体的には、セッションにユーザーIDやセッションIDを格納している
            login_user(user)
            return redirect(url_for('show'))
    # GETの場合
    return render_template('login.html')

# ログアウト処理
@app.route('/logout')
@login_required
def logout():
    # flask-loginのlogout_user()を呼び出してログアウト状態にする
    # 具体的には、セッションの情報を削除している
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for('login'))

# 一覧表示画面表示
@app.route('/show')
@login_required
def show():
    posts = Post.query.all()
    return render_template('show.html', posts=posts)

# 会員登録画面表示
@app.route('/regist')
def regist():
    return render_template('regist.html')

# 会員登録処理
@app.route('/do_regist', methods=['POST'])
def do_regist():
    already_user = User.query.filter_by(email=request.form['email']).first()
    # DBに既に登録されているメールアドレスが入力された場合
    if already_user is not None:
        flash('そのメールアドレスは既に使用されています')
        return redirect(url_for('regist'))
    # 新規登録できるメールアドレスの場合
    else:
        # リクエストフォームのemailをUserインスタンスにセット
        user = User(email=request.form['email'])
        # リクエストフォームのpasswordをハッシュ化してUserインスタンスにセット
        user.set_password(request.form['password'])
        # UserテーブルにINSERTする
        db.session.add(user)
        db.session.commit()
        flash('会員登録が完了しました。ログインしてください。')
        return redirect(url_for('index'))

# 存在しないURLへアクセスされた時の処理。ログイン画面にリダイレクト。
@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('index'))
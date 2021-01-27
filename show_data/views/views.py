from show_data import app, login_manager, db
from flask import request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from show_data.models.users import User
from show_data.models.posts import Post
from datetime import datetime
from sqlalchemy import and_, desc

# ルートアクセス処理
@app.route('/', methods=['GET'])
def index():
    # ログインしている場合は投稿一覧画面にリダイレクトする
    if current_user.is_authenticated:
        return redirect(url_for('show'))
    # ログインしていない場合はログイン画面をレンダリングする
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['GET', 'POST'])
def login():
    # GETの場合
    if request.method == 'GET':
        # ログインしている場合は投稿一覧画面にリダイレクトする
        if current_user.is_authenticated:
            return redirect(url_for('show'))
        # ログインしていない場合はログイン画面をレンダリングする
        else:
            return render_template('login.html')

    # POSTの場合
    if request.method == 'POST':
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

# ログアウト処理
@app.route('/logout', methods=['GET'])
def logout():
    # ログインしていない場合、単にログイン画面にレンダリングする
    if not current_user.is_authenticated:
        return render_template('login.html')
    # ログインしている場合、flask-loginのlogout_user()を呼び出してログアウト状態にする
    # 具体的には、セッションの情報を削除している
    else:
        logout_user()
        flash('ログアウトしました')
        return render_template('login.html')

# 一覧表示画面表示
@app.route('/show', methods=['GET'])
def show():
    # ログインしていない場合、単にログイン画面にレンダリングする
    if not current_user.is_authenticated:
        return render_template('login.html')
    # ログインしている場合、一覧画面表示処理を行う
    else:
        # リクエストで受け取ったURLクエリを再度渡すためにここで定義しておく
        query_startDate = request.args.get('startDate')
        query_endDate = request.args.get('endDate')

        # dateTime変換処理のif文内のローカル変数だと、後続のDB接続処理のif文で変数定義できてなくてエラー吐くのでここで定義しておく
        startDate = None
        endDate = None

        # URLクエリがNoneでない、かつ、''でない場合にのみdateTimeに変換する。
        # datetime.strptime()にNoneまたは''を入れると変換できずエラー吐くので分岐している。
        # 初期遷移時：URLクエリ=None , 日付指定なし日付指定時：URLクエリ=''　となる
        if query_startDate is not None and query_startDate is not '':
            startDate = datetime.strptime(query_startDate, '%Y-%m-%d')
        if query_endDate is not None and query_endDate is not '':
            endDate = datetime.strptime(query_endDate, '%Y-%m-%d')

        # startDateとendDateの有無に応じて流すSQLを分岐させる
        if startDate is not None and endDate is not None:
            posts = Post.query.filter(and_(startDate <= Post.post_date, Post.post_date <= endDate)).order_by(desc(Post.post_date))
        elif endDate is not None:
            posts = Post.query.filter(Post.post_date <= endDate).order_by(desc(Post.post_date))
        elif startDate is not None:
            posts = Post.query.filter(startDate <= Post.post_date).order_by(desc(Post.post_date))
        else:
            posts = Post.query.order_by(desc(Post.post_date)).all()

        # SQLクエリと受け取ったURLクエリを乗せてレンダリングする
        return render_template('show.html', posts=posts, startDate=query_startDate, endDate=query_endDate)

# 会員登録画面表示
@app.route('/regist', methods=['GET'])
def regist():
    return render_template('regist.html')

# 会員登録処理
@app.route('/do_regist', methods=['GET', 'POST'])
def do_regist():
    # GETの場合
    if request.method == 'GET':
        return render_template('regist.html')
    # POSTの場合
    if request.method == 'POST':
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
            return render_template('login.html')

# 存在しないURLへアクセスされた時の処理。ルートアクセス処理にリダイレクト。
@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('index'))
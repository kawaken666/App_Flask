from show_data import app, login_manager, db
from flask import request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from show_data.models.users import User
from show_data.models.posts import Post
from show_data.views.helper_db import insert_into_db, delete_db
from show_data.views.helper import is_allowed_file
from datetime import datetime, timedelta, timezone
from sqlalchemy import and_, desc
import base64, io

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
        # フォーム未入力チェック(フロントのバリデーションを突破された時用)
        if request.form['email'] == '' or request.form['password'] == '':
            flash('メールアドレスとパスワードは必須項目です。')
            return render_template('login.html')

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


# 一覧表示画面遷移
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

        # URLクエリがNoneでない、かつ、''でない場合にのみdateTimeに変換する
        # datetime.strptime()にNoneまたは''を入れると変換できずエラー吐くので分岐している
        # 初期遷移時：URLクエリ=None , 日付指定なし日付指定時：URLクエリ=''　となる
        if query_startDate != None and query_startDate != '':
            startDate = datetime.strptime(query_startDate, '%Y-%m-%d')
        if query_endDate != None and query_endDate != '':
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


# 会員登録画面遷移
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
        # フォーム未入力チェック(フロントのバリデーションを突破された時用)
        if request.form['email'] == '' or request.form['password'] == '':
            flash('メールアドレスとパスワードは必須項目です。')
            return render_template('regist.html')

        already_user = User.query.filter_by(email=request.form['email']).first()
        # DBに既に登録されているメールアドレスが入力された場合
        if already_user is not None:
            flash('そのメールアドレスは既に使用されています')
            return render_template('regist.html')
        # 新規登録できるメールアドレスの場合
        else:
            # リクエストフォームのemailをUserインスタンスにセット
            user = User(email=request.form['email'])
            # リクエストフォームのpasswordをハッシュ化してUserインスタンスにセット
            user.set_password(request.form['password'])
            # usersテーブルにINSERTする
            insert_into_db(user)
            flash('会員登録が完了しました。ログインしてください。')
            return render_template('login.html')


# 新規投稿画面遷移
@app.route('/regist_post', methods=['GET'])
def regist_post():
    # ログインしていない場合、単にログイン画面にレンダリングする
    if not current_user.is_authenticated:
        return render_template('login.html')

    return render_template('regist_post.html')


# 新規投稿登録処理
@app.route('/do_regist_post', methods=['GET', 'POST'])
def do_regist_post():
    # ログインしていない場合、単にログイン画面にレンダリングする
    if not current_user.is_authenticated:
        return render_template('login.html')

    # 画像ファイルをリクエストから取得
    img_file = request.files['img_file']
    # 画像ファイルのファイル名を格納
    img_file_filename = img_file.filename
    # 画像ファイルのストリームを格納
    img_file_stream = img_file.read()

    # 画像ファイルのストリームをバイナリ>base64>utf-8の順に変換した値を格納するための変数を定義している
    img_base64 = None

    # 画像ファイルのBytesをbase64に変換する
    if img_file is not None and is_allowed_file(img_file_filename):
        # base64に変換
        img_base64 = base64.b64encode(img_file_stream).decode("utf-8")

    # postインスタンスにフォームの投稿内容を格納して、postsテーブルにINSERTする
    post = Post(post_text=request.form['post_text'], img_encoded_base64=img_base64,
                post_date=datetime.now(timezone(timedelta(hours=+9), 'JST')))
    insert_into_db(post)
    flash('投稿が完了しました')
    return redirect(url_for('show'))

# 投稿編集画面遷移
@app.route('/edit_post/<int:post_id>', methods=['GET'])
def edit_post(post_id):
    post = Post.query.filter(Post.post_id == post_id).first()
    return render_template("edit_post.html", post=post)

# 投稿編集処理
@app.route('/do_edit_post/<int:post_id>', methods=['GET', 'POST'])
def do_edit_post(post_id):
    post = Post.query.filter(Post.post_id == post_id).first()
    post.post_text = request.form['post_text']
    db.session.commit()
    flash('投稿が更新されました')
    return redirect(url_for('show'))

# 投稿削除処理
@app.route('/do_delete_post/<int:post_id>', methods=['GET', 'POST'])
def do_delete_post(post_id):
    post = Post.query.filter(Post.post_id == post_id).first()
    delete_db(post)
    flash('投稿を削除しました')
    return redirect(url_for('show'))

# 存在しないURLへアクセスされた時の処理
# ルートアクセス処理にリダイレクト
@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('index'))
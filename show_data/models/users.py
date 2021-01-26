from show_data import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(50))

    # セッションからidを取得してDBからユーザー情報を取得するコールバックデコレータ
    # flask-loginを使う際は必ず必要
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 会員登録用メソッド
    # password_hashカラムにパスワードをハッシュ化した値を格納する
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # ログインチェック用メソッド
    # フォームから取得したパスワード(引数2)のハッシュ値が、DB保持のハッシュ値と合致するかチェックする
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
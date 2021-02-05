from show_data import db

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # TODO いいね、コメントを保持するテーブル作成後、post_idを外部キーと定義する
    post_text = db.Column(db.String(128), nullable=False)
    img_url = db.Column(db.String(128))
    post_date = db.Column(db.DateTime, nullable=False)



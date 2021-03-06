# DB操作のスクリプトファイル

from flask_script import Command
from show_data import db
from show_data.models.posts import Post
from datetime import datetime

# 作成したモデルをDBに反映するコマンド
class InitDB(Command):
    # 下記はスクリプト説明のコメント
    "create database"

    def run(self):
        db.create_all()

# テスト完了後用のDB削除コマンド
class DropDB(Command):
    "drop database"

    def run(self):
        db.drop_all()

# ダミーデータ登録用コマンド
# 適宜データは変えるべし
class InsertDummy(Command):
    "insert dummy data into posts-TBL"

    def run(self):
        posts = [Post(post_text='最新ゲーム紹介', post_date=datetime(2020, 12, 1, 17, 30, 23 ,174812)),
                 Post(post_text='最新化粧品紹介', post_date=datetime(2020, 11, 1, 16, 30, 23, 174812)),
                 Post(post_text='最新グルメ紹介', post_date=datetime(2020, 10, 1, 13, 36, 23, 174812)),
                 Post(post_text='流行コーデ紹介', post_date=datetime(2020, 9, 1, 19, 12, 23, 174812))
                 ]
        for post in posts:
            db.session.add(post)
        db.session.commit()

# SQLの取得結果の配列確認のためのコマンド
# 適宜テーブル名や配列インデックスや配列変数を変えて使うべし
class SelectAll(Command):
    "select * from some TBL"

    def run(self):
        posts = Post.query.all()
        print(posts[0].post_date)
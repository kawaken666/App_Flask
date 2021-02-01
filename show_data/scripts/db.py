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
        posts = [Post(1, '最新ゲーム紹介', datetime(2020, 12, 1, 17, 30, 23 ,174812), 23, 7893, 7465, 505, 2, 76, 0),
                 Post(2, '最新化粧品紹介', datetime(2020, 11, 1, 16, 30, 23, 174812), 34, 8675, 7444, 789, 4, 200, 0),
                 Post(3, '最新グルメ紹介', datetime(2020, 10, 1, 13, 36, 23, 174812), 77, 19384, 13483, 1544, 32, 584, 0),
                 Post(4, '流行コーデ紹介', datetime(2020, 9, 1, 19, 12, 23, 174812), 100, 20394, 19837, 1982, 67, 874, 0),
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
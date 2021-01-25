# DB操作のスクリプトファイル

from flask_script import Command
from show_data import db

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
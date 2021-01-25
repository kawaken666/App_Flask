from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('show_data.config')

# LoginManagerインスタンスを作成して初期化
login_manager = LoginManager()
login_manager.init_app(app)
# TODO:要調査：鍵を作成？この鍵をcookieで交換している？
app.config['SECRET_KEY'] = "secret"

# SQLAlchemyインスタンスを作成して初期化
db = SQLAlchemy(app)
db.init_app(app)

# TODO：要調査：Flaskをインスタンス化した後にしか、show_dataは参照(import)できない？
# 以下を本ファイルの上部に移動するとエラー吐く
import show_data.views.views
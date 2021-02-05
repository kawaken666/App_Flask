from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('show_data.config')

# LoginManagerインスタンスを作成して初期化
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret'
UPLOAD_FOLDER = 'https://mighty-shore-18727.herokuapp.com/show_data/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# SQLAlchemyインスタンスを作成して初期化
db = SQLAlchemy(app)
db.init_app(app)

# 以下を本ファイルの上部に移動するとエラー吐く
import show_data.views.views
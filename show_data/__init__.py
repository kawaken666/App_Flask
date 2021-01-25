from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('show_data.config')

db = SQLAlchemy(app)
db.init_app(app)

import show_data.views.views
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
SQLALCHEMY_DATABASE_URI = DATABASE_URL

"""
# ローカル用のDB接続URI
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
    'user': 'kk',
    'password': 'kk',
    'host': '127.0.0.1',
    'name': 'show_data'
})
"""

SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = 'secret'
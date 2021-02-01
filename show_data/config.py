import os
import psycopg2

# 本番環境用設定値クラス(heroku)
class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # herokuでしかos.environ['DATABASE_URL']は処理できないのでローカルだと以下1行をコメントアウトする必要あり
    DATABASE_URI = os.environ['DATABASE_URL']

    def con(self):
        return psycopg2.connect(BaseConfig.DATABASE_URI, sslmode='require')


# 開発環境用設定値クラス
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
    'user': 'kk',
    'password': 'kk',
    'host': '127.0.0.1',
    'name': 'show_data'
})

# テスト環境用設定値クラス
class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
        'user': 'kk',
        'password': 'kk',
        'host': '127.0.0.1',
        'name': 'show_data'
    })


# heroku用のpsycopg2設定(ローカルだと以下1行は動かないのでコメントアウトする必要あり)
conn = BaseConfig.con()


# SQLAlchemyのDBのURI設定(環境によってconfigクラスを切り替える)
SQLALCHEMY_DATABASE_URI = BaseConfig.DATABASE_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

# デバッグモード設定(環境によってconfigクラスを切り替える)
DEBUG = BaseConfig.DEBUG

# テストモード設定(環境によってconfigクラスを切り替える)
TESTING = BaseConfig.TESTING

SECRET_KEY = 'secret'
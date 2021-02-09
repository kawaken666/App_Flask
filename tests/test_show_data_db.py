# db操作周りメソッドのテスト

from show_data.models.users import User
from show_data.models.posts import Post
from datetime import datetime
from show_data.views.helper_db import insert_into_db


# insert用モデルインスタンス
user = User(email='kenta')
user.set_password('kenta')

post = Post(post_text='test', img_encoded_base64='/9j/4AAQSkZJRgABAQEASABIAAD/7SF4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAA',
            post_date=datetime.now())


# 最初のテスト関数の引数にsetup_dbフィクスチャを入れることで、pytest実行時にdbのcreateを行う。pytest実行後にdropする。
def test_setup_db(setup_db):
    pass

# usersのINSERTテスト
def test_insert_users():
    result = insert_into_db(user)
    assert result is True, 'usersへのINSERTに失敗しました'

# postsのINSERTテスト
def test_insert_posts():
    result = insert_into_db(post)
    assert result is True, 'postsへのINSERTに失敗しました'


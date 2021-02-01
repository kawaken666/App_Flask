import pytest
from show_data import app, db
from show_data.models.posts import Post
from datetime import datetime

# テスト用のDBのcreateとdropを行う
# pytestコマンド単位で行う scopeの値によってスコープ範囲を変更可能
@pytest.fixture(scope="session")
def setup_db():
    db.create_all()
    print('dbをcreateしました')
    yield None  # fixtureはyieldで区切ると、yieldより前の処理をテストの前に、yieldより後の処理をテストの後に、実行する
    db.drop_all()
    print('dbをdropしました')

# 投稿ダミーデータをINSERTする
@pytest.fixture(scope="function")
def insert_dummy_data_to_posts():
    posts = [Post(2, '最新ゲーム紹介', datetime(2020, 12, 1, 17, 30, 23, 174812), 23, 7893, 7465, 505, 2, 76, 0),
             Post(3, '最新化粧品紹介', datetime(2020, 11, 1, 16, 30, 23, 174812), 34, 8675, 7444, 789, 4, 200, 0),
             Post(4, '最新グルメ紹介', datetime(2020, 10, 1, 13, 36, 23, 174812), 77, 19384, 13483, 1544, 32, 584, 0),
             Post(5, '流行コーデ紹介', datetime(2020, 9, 1, 19, 12, 23, 174812), 100, 20394, 19837, 1982, 67, 874, 0),
             ]
    for post in posts:
        db.session.add(post)
    db.session.commit()

# テストクライアント作成
@pytest.fixture(scope="function")
def client():
    # withでtest_clientを括ることでテストfunction毎にclientを生成する->ログイン状態を毎回リセット可能
    with app.test_client() as client:
        yield client

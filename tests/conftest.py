import pytest
from show_data import app, db

# テスト用のDBのcreateとdrop
# pytestコマンド単位で行う scopeの値によってスコープ範囲を変更可能
@pytest.fixture(scope="session")
def setup_db():
    db.create_all()
    print('dbをcreateしました')
    yield None  # fixtureはyieldで区切ると、yieldより前の処理をテストの前に、yieldより後の処理をテストの後に、実行する
    db.drop_all()
    print('dbをdropしました')

# テストクライアント作成
@pytest.fixture(scope="function")
def client():
    # withでtest_clientを括ることでテストfunction毎にclientを生成する->ログイン状態を毎回リセット可能
    with app.test_client() as client:
        yield client

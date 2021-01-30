import pytest
from show_data import app, db

# テストクライアント作成
@pytest.fixture
def client():
    return app.test_client()

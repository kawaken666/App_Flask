from show_data.views.views import index, login, login, show, regist, do_regist, non_existant_route
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

def test_views_index(client):
    res = client.get('/')
    assert res.status_code == 200
    # res.get_data(as_text=True)でレスポンスのhtmlの内容をUnicodeテキスト(日本語対応)で取得できる
    # res.dataだとレスポンスのhtmlの取得内容がバイトコードテキストになるので日本語をassertしたいときはエラー吐いてしまう
    assert 'ログインしてください' in res.get_data(as_text=True)

def test_views_non_existant_route(client):
    res = client.get('404')
    assert res.status_code == 302
    assert res.headers['Location'] == 'http://localhost/'

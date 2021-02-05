from werkzeug.datastructures import FileStorage

from tests.helpers import (assert_http_200, assert_http_302, assert_render_do_regist,
                           assert_flash_required_email_and_password, assert_flash_regist_complete,
                           assert_flash_duplicate_email, assert_render_login, assert_redirect_show,
                           assert_redirect_root, assert_flash_failure_login, assert_flash_success_logout,
                           assert_is_exist_should_select, assert_is_exist_should_not_select,
                           assert_render_regist_post, )

# 最初のテスト関数の引数にsetup_dbフィクスチャを入れることで、pytest実行時にdbのcreateを行う。pytest実行後にdropする。
def test_setup_db(setup_db):
    pass

def test_views_do_regist(client):
    # 登録前GET
    res = client.get('/do_regist')
    assert_http_200(res)
    assert_render_do_regist(res)
    # 登録前POST
    # email未入力チェック
    res = client.post('/do_regist', data=dict(email='', password='kenta'))
    assert_render_do_regist(res)
    assert_flash_required_email_and_password(res)
    # password未入力チェック
    res = client.post('/do_regist', data=dict(email='kenta', password=''))
    assert_render_do_regist(res)
    assert_flash_required_email_and_password(res)
    # 会員登録処理正常
    res = client.post('/do_regist', data=dict(email='kenta', password='kenta'))
    assert_flash_regist_complete(res)
    # 登録後チェック
    # 会員登録email重複チェック
    res = client.post('/do_regist', data=dict(email='kenta', password='kenta'))
    assert_render_do_regist(res)
    assert_flash_duplicate_email(res)

def test_views_index(client):
    # ログイン前GET
    res = client.get('/')
    assert_http_200(res)
    # res.get_data(as_text=True)でレスポンスのhtmlの内容をUnicodeテキスト(日本語対応)で取得できる
    # res.dataだとレスポンスのhtmlの取得内容がバイトコードテキストになるので日本語をassertしたいときはエラー吐いてしまう
    assert_render_login(res)
    # ログイン後GET
    res = client.post('/login', data=dict(email='kenta', password='kenta'))
    res = client.get('/')
    assert_http_302(res)
    assert_redirect_show(res)

def test_views_non_existant_route(client):
    res = client.get('404')
    assert_http_302(res)
    assert_redirect_root(res)

def test_views_login(client):
    # ログイン前GET
    res = client.get('/login')
    assert_http_200(res)
    assert_render_login(res)
    # email未入力チェック
    res = client.post('/login', data=dict(email='', password='kenta'))
    assert_http_200(res)
    assert_render_login(res)
    assert_flash_required_email_and_password(res)
    # password未入力チェック
    res = client.post('/login', data=dict(email='kenta', password=''))
    assert_http_200(res)
    assert_render_login(res)
    assert_flash_required_email_and_password(res)
    # ログイン失敗POST
    res = client.post('/login', data=dict(email='kenta', password='kenta2'))
    assert_http_200(res)
    assert_render_login(res)
    assert_flash_failure_login(res)
    # ログイン成功POST
    res = client.post('/login', data=dict(email='kenta', password='kenta'))
    assert_http_302(res)
    assert_redirect_show(res)
    # ログイン後GET
    res = client.get('/login')
    assert_redirect_show(res)

def test_views_logout(client):
    # ログイン前GET
    res = client.get('/logout')
    assert_http_200(res)
    assert_render_login(res)
    # ログイン後GET
    res = client.post('/login', data=dict(email='kenta', password='kenta'))
    res = client.get('/logout')
    assert_http_200(res)
    assert_flash_success_logout(res)

def test_views_regist(client):
    res = client.get('/regist')
    assert_http_200(res)
    assert_render_do_regist(res)

def test_views_show(insert_dummy_data_to_posts, client):
    # ログイン前GET
    res = client.get('/show')
    assert_http_200(res)
    assert_render_login(res)

    # ログイン処理
    res = client.post('/login', data=dict(email='kenta', password='kenta'))

    # 初期遷移時(startDate=None and endDate=None)
    check_query_post_should_exist = ['投稿一覧', '最新ゲーム紹介', '最新化粧品紹介', '最新グルメ紹介', '流行コーデ紹介']
    res = client.get('/show')
    assert_http_200(res)
    for post in check_query_post_should_exist:
        assert_is_exist_should_select(post, res)

    # 日付指定(startDate!='' and endDate!='')
    check_query_post_should_exist = ['投稿一覧', '最新グルメ紹介', '流行コーデ紹介']
    check_query_post_should_not_exist = ['最新ゲーム紹介', '最新化粧品紹介']
    res = client.get('/show?startDate=2020-8-31&endDate=2020-10-2')
    assert_http_200(res)
    for post in check_query_post_should_exist:
        assert_is_exist_should_select(post, res)
    for post in check_query_post_should_not_exist:
        assert_is_exist_should_not_select(post, res)

    # 日付指定(startDate!='' and endDate='')
    # 取得データの期待値を変数に定義している
    check_query_post_should_exist = ['投稿一覧', '最新ゲーム紹介', '最新化粧品紹介', '最新グルメ紹介']
    check_query_post_should_not_exist = ['流行コーデ紹介']
    res = client.get('/show?startDate=2020-9-30&endDate=')
    assert_http_200(res)
    for post in check_query_post_should_exist:
        assert_is_exist_should_select(post, res)
    for post in check_query_post_should_not_exist:
        assert_is_exist_should_not_select(post, res)

    # 日付指定(startDate='' and endDate!='')
    # 取得データの期待値を変数に定義している
    check_query_post_should_exist = ['投稿一覧', '最新化粧品紹介', '最新グルメ紹介', '流行コーデ紹介']
    check_query_post_should_not_exist = ['最新ゲーム紹介']
    res = client.get('/show?startDate=&endDate=2020-11-2')
    assert_http_200(res)
    for post in check_query_post_should_exist:
        assert_is_exist_should_select(post, res)
    for post in check_query_post_should_not_exist:
        assert_is_exist_should_not_select(post, res)

    # 日付指定(startDate='' and endDate!='')
    # 取得データの期待値を変数に定義している
    check_query_post_should_exist = ['投稿一覧', '最新ゲーム紹介', '最新化粧品紹介', '最新グルメ紹介', '流行コーデ紹介']
    res = client.get('/show?startDate=&endDate=')
    assert_http_200(res)
    for post in check_query_post_should_exist:
        assert_is_exist_should_select(post, res)


def test_views_regist_post(client):
    # ログイン前GET
    res = client.get('/regist_post')
    assert_http_200(res)
    assert_render_login(res)

    # ログイン処理
    res = client.post('/login', data=dict(email='kenta', password='kenta'))

    # 新規投稿画面表示
    res = client.get('/regist_post')
    assert_http_200(res)
    assert_render_regist_post(res)


def test_views_do_regist_post(client):
    # ログイン前GET
    res = client.get('/do_regist_post')
    assert_http_200(res)
    assert_render_login(res)

    # ログイン処理
    res = client.post('/login', data=dict(email='kenta', password='kenta'))

    # 投稿登録処理正常
    res = client.post('/do_regist_post', data=dict(post_text='新規投稿テスト',
                                                   img_file=FileStorage(filename='')),
                      content_type="multipart/form-data")
    assert_http_302(res)
    assert_redirect_show(res)

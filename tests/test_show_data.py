# 最初のテスト関数の引数にsetup_dbフィクスチャを入れることで、pytest実行時にdbのcreateを行う。pytest実行後にdropする。
def test_setup_db(setup_db):
    pass

def test_views_do_regist(client):
    # 登録前GET
    res = client.get('/do_regist')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert '会員登録してください' in res.get_data(as_text=True)
    # 登録前POST
    # email未入力チェック
    res = client.post('/do_regist', data=dict(email='', password='kenta'))
    assert '会員登録してください' in res.get_data(as_text=True)
    assert 'メールアドレスとパスワードは必須項目です。' in res.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
    # password未入力チェック
    res = client.post('/do_regist', data=dict(email='kenta', password=''))
    assert '会員登録してください' in res.get_data(as_text=True)
    assert 'メールアドレスとパスワードは必須項目です。' in res.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
    # 会員登録処理正常
    res = client.post('/do_regist', data=dict(email='kenta', password='kenta'))
    assert '会員登録が完了しました。ログインしてください。' in res.get_data(as_text=True), '会員登録処理が異常です'
    # 登録後チェック
    # 会員登録email重複チェック
    res = client.post('/do_regist', data=dict(email='kenta', password='kenta'))
    assert '会員登録してください' in res.get_data(as_text=True)
    assert 'そのメールアドレスは既に使用されています' in res.get_data(as_text=True), 'アラート(flash)が正常に出せてません'

def test_views_index(client):
    # ログイン前GET
    res = client.get('/')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    # res.get_data(as_text=True)でレスポンスのhtmlの内容をUnicodeテキスト(日本語対応)で取得できる
    # res.dataだとレスポンスのhtmlの取得内容がバイトコードテキストになるので日本語をassertしたいときはエラー吐いてしまう
    assert 'ログインしてください' in res.get_data(as_text=True)
    # ログイン後GET
    res = client.post('/login', data=dict(email='kenta', password='kenta'))
    res = client.get('/')
    assert res.status_code == 302, 'リダイレクトレスポンスのステータスコードが異常です'
    assert res.headers['Location'] == 'http://localhost/show', 'リダイレクト先が異常です'

def test_views_non_existant_route(client):
    res = client.get('404')
    assert res.status_code == 302, 'リダイレクトレスポンスのステータスコードが異常です'
    assert res.headers['Location'] == 'http://localhost/', 'リダイレクト先が異常です'

def test_views_login(client):
    # ログイン前GET
    res = client.get('/login')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert 'ログインしてください' in res.get_data(as_text=True)
    # email未入力チェック
    res = client.post('/login', data=dict(email='', password='kenta'))
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert 'ログインしてください' in res.get_data(as_text=True)
    assert 'メールアドレスとパスワードは必須項目です。' in res.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
    # password未入力チェック
    res = client.post('/login', data=dict(email='kenta', password=''))
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert 'ログインしてください' in res.get_data(as_text=True)
    assert 'メールアドレスとパスワードは必須項目です。' in res.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
    # ログイン失敗POST
    res = client.post('/login', data=dict(email='kenta', password='kenta2'))
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert 'ログインしてください' in res.get_data(as_text=True)
    assert 'ユーザー名、または、パスワードが違います' in res.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
    # ログイン成功POST
    res = client.post('/login', data=dict(email='kenta', password='kenta'))
    assert res.status_code == 302, 'リダイレクトレスポンスのステータスコードが異常です'
    assert res.headers['Location'] == 'http://localhost/show', 'リダイレクト先が異常です'
    #ログイン後GET
    res = client.get('/login')
    assert res.headers['Location'] == 'http://localhost/show', 'リダイレクト先が異常です'

def test_views_logout(client):
    # ログイン前GET
    res = client.get('/logout')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert 'ログインしてください' in res.get_data(as_text=True)
    # ログイン後GET
    res = client.post('/login', data=dict(email='kenta', password='kenta'))
    res = client.get('/logout')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert 'ログアウトしました' in res.get_data(as_text=True)

def test_views_regist(client):
    res = client.get('/regist')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert '会員登録してください' in res.get_data(as_text=True)

def test_views_show(ins_post_to_posts, client):
    # ログイン前GET
    res = client.get('/show')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert 'ログインしてください' in res.get_data(as_text=True)

    # ログイン処理
    res = client.post('/login', data=dict(email='kenta', password='kenta'))

    # 初期遷移時(startDate=None and endDate=None)
    check_query_post_should_exist = ['投稿一覧', '最新ゲーム紹介', '最新化粧品紹介', '最新グルメ紹介', '流行コーデ紹介']
    res = client.get('/show')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    for post in check_query_post_should_exist:
        assert post in res.get_data(as_text=True), 'dbから取得したデータが不適切です'

    # 日付指定(startDate!='' and endDate!='')
    check_query_post_should_exist = ['投稿一覧', '最新グルメ紹介', '流行コーデ紹介']
    check_query_post_should_not_exist = ['最新ゲーム紹介', '最新化粧品紹介']
    res = client.get('/show?startDate=2020-8-31&endDate=2020-10-2')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    for post in check_query_post_should_exist:
        assert post in res.get_data(as_text=True), '取得すべきデータをdbから取得していません'
    for post in check_query_post_should_not_exist:
        assert post not in res.get_data(as_text=True), '取得すべきでないデータをdbから取得しています'

    # 日付指定(startDate!='' and endDate='')
    # 取得データの期待値を変数に定義している
    check_query_post_should_exist = ['投稿一覧', '最新ゲーム紹介', '最新化粧品紹介', '最新グルメ紹介']
    check_query_post_should_not_exist = ['流行コーデ紹介']
    res = client.get('/show?startDate=2020-9-30&endDate=')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    for post in check_query_post_should_exist:
        assert post in res.get_data(as_text=True), '取得すべきデータをdbから取得していません'
    for post in check_query_post_should_not_exist:
        assert post not in res.get_data(as_text=True), '取得すべきでないデータをdbから取得しています'

    # 日付指定(startDate='' and endDate!='')
    # 取得データの期待値を変数に定義している
    check_query_post_should_exist = ['投稿一覧', '最新化粧品紹介', '最新グルメ紹介', '流行コーデ紹介']
    check_query_post_should_not_exist = ['最新ゲーム紹介']
    res = client.get('/show?startDate=&endDate=2020-11-2')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    for post in check_query_post_should_exist:
        assert post in res.get_data(as_text=True), '取得すべきデータをdbから取得していません'
    for post in check_query_post_should_not_exist:
        assert post not in res.get_data(as_text=True), '取得すべきでないデータをdbから取得しています'

    # 日付指定(startDate='' and endDate!='')
    # 取得データの期待値を変数に定義している
    check_query_post_should_exist = ['投稿一覧', '最新ゲーム紹介', '最新化粧品紹介', '最新グルメ紹介', '流行コーデ紹介']
    res = client.get('/show?startDate=&endDate=')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    for post in check_query_post_should_exist:
        assert post in res.get_data(as_text=True), '取得すべきデータをdbから取得していません'


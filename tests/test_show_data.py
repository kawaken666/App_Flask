# 最初のテスト関数の引数にsetup_dbフィクスチャを入れることで、pytest実行時にdbのcreateを行う。pytest実行後にdropする。
def test_setup_db(setup_db):
    pass

def test_views_do_regist(client):
    # 登録前GET
    res = client.get('/do_regist')
    assert res.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
    assert '会員登録してください' in res.get_data(as_text=True)
    ## 登録前POST
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
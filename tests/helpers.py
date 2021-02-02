# テストに必要なヘルパー関数を当ファイルに定義する


# HTTPステータスのassert
def assert_http_200(response):
    assert response.status_code == 200, 'HTTPレスポンスのステータスコードが異常です'
def assert_http_302(response):
    assert response.status_code == 302, 'リダイレクトレスポンスのステータスコードが異常です'


# レンダー先テンプレートが合致しているかを確認するassert
# regist.html
def assert_render_do_regist(response):
    assert '会員登録してください' in response.get_data(as_text=True)
# login.html
def assert_render_login(response):
    assert 'ログインしてください' in response.get_data(as_text=True)
# regist_post.html
def assert_render_regist_post(response):
    assert '新規投稿' in response.get_data(as_text=True)


# flashの確認assert このメソッドはレンダリングの時しか使えないので注意（リダイレクトはレスポンスのdataにhtmlテキストは含まれない）
# フォーム未入力
def assert_flash_required_email_and_password(response):
    assert 'メールアドレスとパスワードは必須項目です。' in response.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
# 会員登録完了
def assert_flash_regist_complete(response):
    assert '会員登録が完了しました。ログインしてください。' in response.get_data(as_text=True), '会員登録処理が異常です'
# 会員登録時、メアド重複
def assert_flash_duplicate_email(response):
    assert 'そのメールアドレスは既に使用されています' in response.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
# ログイン失敗時
def assert_flash_failure_login(response):
    assert 'ユーザー名、または、パスワードが違います' in response.get_data(as_text=True), 'アラート(flash)が正常に出せてません'
# ログアウト完了時
def assert_flash_success_logout(response):
    assert 'ログアウトしました' in response.get_data(as_text=True), 'ログアウト処理が異常です'


# リダイレクト先ロケーションが合致しているを確認するassert
# /
def assert_redirect_root(response):
    assert response.headers['Location'] == 'http://localhost/', 'リダイレクト先が異常です'
# /show
def assert_redirect_show(response):
    assert response.headers['Location'] == 'http://localhost/show', 'リダイレクト先が異常です'


# htmlに含まれるDBから取得したデータが、適切であるかを確認するassert
# このメソッドはレンダリングの時しか使えないので注意（リダイレクトはレスポンスのdataにhtmlテキストは含まれない）
# 取得すべきデータがレスポンスhtmlに存在するか
def assert_is_exist_should_select(expect, response):
    assert expect in response.get_data(as_text=True), '取得すべきデータをdbから取得していません'
# 取得すべきでないデータがレスポンスhtmlに存在するか
def assert_is_exist_should_not_select(expect, response):
    assert expect not in response.get_data(as_text=True), '取得すべきでないデータをdbから取得しています'


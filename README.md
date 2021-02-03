## アプリ概要
### -記事投稿型SNSアプリ-

#### ▼実装機能
- 会員登録
- ログイン (flask-loginを用いたPWハッシュ化認証)
- ログアウト
- 投稿一覧表示
- 投稿一覧の日付での絞り込み表示
- 新規投稿

#### ▼使い方　<font color="Crimson">※現状、レスポンシブ対応は未実装のためPCブラウザからアクセスしてください</span></font>
1. 以下herokuのURLにアクセス  
https://mighty-shore-18727.herokuapp.com/  
1. 最初に会員登録を行ってください  
    -未入力チェック以外のバリデーションは実装してないため、入力値はなんでも構いません
1. ログインしてください

#### ▼pipenvを用いた環境構築  (cloneされる方向け)
1. pipenvをインストールしてください　　
```
$ pip install pipenv
```
2. pipenvを任意のpythonのバージョンを指定して初期化してください  
```
$ pipenv --python 3  # python3系を指定する場合
```
3. Pipfileから環境を再現してください(パッケージのインストール)  
```
$ pipenv install
```



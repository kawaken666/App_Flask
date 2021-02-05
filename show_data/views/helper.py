from show_data.__init__ import ALLOWED_EXTENSIONS

# アップロードされたファイル拡張子が適切かどうかチェックするメソッド
def is_allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
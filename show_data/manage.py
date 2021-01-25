# スクリプトモジュールを実行できるようにするためのファイル

from flask_script import Manager
from show_data import app

from show_data.scripts.db import InitDB, DropDB

if __name__ == "__main__":
    manager = Manager(app)
    # init_dbコマンドを実行できるようにする
    manager.add_command('init_db', InitDB())
    # drop_dbコマンドを実行できるようにする
    manager.add_command('drop_db', DropDB())
    manager.run()
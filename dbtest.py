# MySQLdbのインポート
from distutils.command.config import config
import MySQLdb
import config
# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd=config.PASS,
    db='python_db')
cursor = connection.cursor()
 
# ここに実行したいコードを入力します
try:
    cursor.execute("SELECT * FROM PlayerManager")
    for row in cursor:
        print(row)
    if row[1] == 1234567890:
        print("一致")
except MySQLdb._exceptions.OperationalError:
    print("karamuga nai")


# 保存を実行
connection.commit()
 
# 接続を閉じる
connection.close()
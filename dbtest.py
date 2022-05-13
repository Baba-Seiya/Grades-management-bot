# MySQLdbのインポート
from distutils.command.config import config
import MySQLdb
import config
# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='us-cdbr-east-05.cleardb.net',
    user='b8b7dbaf799928',
    passwd="09fe4b17",
    db='heroku_2864c216fe3c408')
cursor = connection.cursor()
table = "PlayerManager"
id = 588371754737729543
# ここに実行したいコードを入力します
try:
    cursor.execute("UPDATE playermanager SET userName = \"🐏パペガメ🐏#4966\" where userID = 424207709043425281;")

except MySQLdb._exceptions.OperationalError:
    print("karamuga nai")


# 保存を実行
connection.commit()
 
# 接続を閉じる
connection.close()
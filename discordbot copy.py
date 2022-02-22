# インストールした discord.py を読み込む
import discord
import pickle
import asyncio
import re
from pyrsistent import b
import config
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
# MySQLdbのインポート
import MySQLdb

guild_ids = [int(config.GUILD_ID1),int(config.GUILD_ID2)] # Put your server ID in this array.
 
# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd=config.PASS,
    db='python_db')
cursor = connection.cursor()

# 自分のBotのアクセストークンに置き換えてください
TOKEN = config.MY_TOKEN

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=discord.Intents.all())
slash_client = SlashCommand(client,sync_commands=True)
#--------------------------------------------定義関数--------------------------------------------
#db関連の関数
def column_ser(chr):
    try:
        cursor.execute(f"SELECT * FROM {table} where {chr}")
        return True
    except MySQLdb._exceptions.OperationalError:
        return False

#win lose dictを空にする関数
def clean(svid):
    global A
    global D
    A = []
    D = []

#選手の登録する際の関数
def regist(name, id, svid):
    #サーバーが登録されているか確認
    if not column_ser(f"{svid}_win"):
        #無かった場合追加する
        cursor.execute(f"ALTER TABLE {table} ADD {svid}_win int NULL, ADD {svid}_match int NULL, ADD {svid}_rate int NULL")
    

    #その人が登録されているか確認
    cursor.execute(f"SELECT * FROM {table} where userID={id}")
    data = cursor
    for i in data:
        #見つかったらその人がこのサーバーに登録されているか確認する
        if i[1] == id:
            cursor.execute(f"SELECT userID, {svid}_win FROM {table} where userID={id}")
            for u in cursor:
                #None（未登録）だったら0を入れて登録する。
                if u[1] == None:
                    cursor.execute(f"update {table} set {svid}_win=0, {svid}_match=0, {svid}_rate=0")
                    return "サーバーを追加登録しました"
            return "登録済みです"
        break
    else:
        #見つからなかったらその人とサーバーを登録する
        cursor.execute(f"insert into {table}(userName,userID,{svid}_win,{svid}_match,{svid}_rate) values(\"{name}\",{id},0,0,0)")
        return "ユーザを登録をしました"

    return "登録済みです"


#--------------------------変数置き場-------------------------
memberID = [["kame"]] #重複登録確認用ID置き場[[user.id,serverid,serverid....],[...]]
member = {} #キー=id,値=インスタンス名のdict  
instanceName = [] #インスタンス名の管理用 (表示名で登録 message.author)
memberNames = {} #キー=表示名, 値=id
A = [] #userIDが入る
D = []
serverList = []#各サーバーに対して[[serverid,[A],[D],…]のリスト  

table = "PlayerManager" #sqlデバック用

# カスタム絵文字
EmojiA = "🅰️"
EmojiD = "\N{Turtle}"
EmojiOK= "🆗"
EmojiW = "✅"
EmojiL = "❌"
EmojiC = "🚫"

#-----------------------discord.py event-----------------
# ---------------------起動時に動作する処理-----------------
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

#-------------------プログラムを終了する時に必要な動作------------------
@slash_client.slash(name="exit", guild_ids=guild_ids)
async def _slash_exit(ctx: SlashContext):
    await ctx.send(content="bye")
    # 保存を実行
    connection.commit()

    # 接続を閉じる
    connection.close()
    print("正常に終了しました")
    exit()

# ------------------スラッシュコマンドにより動作する処理------------
#選手の登録
@slash_client.slash(name="regist", guild_ids=guild_ids)
async def _slash_regist(ctx: SlashContext):
    name = str(ctx.author)
    id = int(ctx.author_id)
    svid =int(ctx.guild_id) 
    ans = regist(name,id,svid)
    connection.commit()
    await ctx.send(content=str(ans))

@slash_client.slash(name="regist_test", guild_ids=guild_ids)
async def _slash_regist_test(ctx: SlashContext):
    name = "testman"
    id = 1234567890
    svid ="serverid" 
    ans = regist(name,id,svid)
    connection.commit()
    await ctx.send(content=str(ans))

#戦績の表示
@slash_client.slash(name="score", guild_ids=guild_ids)
async def _slash_score(ctx: SlashContext):
    svid = int(ctx.guild_id)
    msg = ""
    if column_ser(f"{svid}_win"):
        cursor.execute(f"SELECT userName, userID, {svid}_win, {svid}_match, {svid}_rate FROM {table} where {svid}_win is not null")
        for i in cursor:
            #勝率を更新する
            cursor.execute(f"update {table} set {svid}_rate={svid}_win/{svid}_match where userID={i[1]}")
        
        cursor.execute(f"SELECT userName, userID, {svid}_win, {svid}_match, {svid}_rate FROM {table} where {svid}_win is not null order by{svid}_rate")
        #ソートして表示
        x=1
        for i in cursor:
            msg += f"{x}. {i[0]} 勝率:{i[4]}% 勝ち数:{i[2]} 試合回数:{i[3]}\n"
            x += 1 
    connection.commit()
    await ctx.send(content=msg)
    


@slash_client.slash(name="hello", guild_ids=guild_ids)
async def _slash_hello(ctx: SlashContext):
    await ctx.send(content="Hello!")

@slash_client.slash(name="dbtest", guild_ids=guild_ids)
async def _slash_dbtest(ctx: SlashContext):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    for i in rows:
        await ctx.send(content=str(i))
    

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
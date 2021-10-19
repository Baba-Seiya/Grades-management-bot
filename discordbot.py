# インストールした discord.py を読み込む
import discord
import pickle

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'ODk5NDUyODI4ODgyNDU2NTg2.YWy-uQ.1EBAeA10aEWGDWQh8WVFecsFah4'

# 接続に必要なオブジェクトを生成
client = discord.Client()

#選手を管理するクラス
class PlayerManager:
    #クラス変数
    count = 0   #総選手数
    @classmethod
    def countup(cls):
        cls.count += 1

    #コンストラクタ
    def __init__(self, userID):
        self.win = 0       #勝利数
        self.match = 0     #対戦回数
        self.id = userID   #ユーザーID
        self.winRate = 0   #勝率
        PlayerManager.countup()
        print(self,self.win,self.match,self.winRate,self.id)


    #インスタンスメソッド
    def winMatch(self):    #勝った時の処理
        self.win += 1
        self.match += 1
    
    def loseMatch(self):   #負けた時の処理
        self.match += 1



# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
#選手の登録
member = ["kame"]
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    if message.content == "!regist":
        for i in member:   #重複登録をさせないための処理
            if message.author.id == i:
                content = "登録済みです"
                await message.channel.send(content)
                break
        else:
            member.append(message.author.id)
            kame1 = PlayerManager(message.author.id) #インスタンス名をどうにかする
            content = str(message.author) + "さん登録しました"
            await message.channel.send(content)

        

                


        
    
    if message.content == "!exit":
        

        with open('test.pickle', mode='wb') as f:
            pickle.dump('hello', f)
        exit()




    


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)



"""メッセージ受信時に実行されるイベントハンドラ
@client.event # イベントを受信するための構文（デコレータ）
async def on_message(message): # イベントに対応する関数と受け取る引数
    ... # 処理いろいろ"""

"""Bot起動時に実行されるイベントハンドラ
@client.event
async def on_ready():
    ..."""

"""リアクション追加時に実行されるイベントハンドラ
@client.event
async def on_reaction_add(reaction, user):
    ..."""

"""新規メンバー参加時に実行されるイベントハンドラ
@client.event
async def on_member_join(member):
    ..."""
    
"""メンバーのボイスチャンネル出入り時に実行されるイベントハンドラ
@client.event
async def on_voice_state_update(member, before, after):
    ..."""
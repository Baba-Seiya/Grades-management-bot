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
    def __init__(self, userID, name):
        self.win = 0       #勝利数
        self.match = 0     #対戦回数
        self.id = userID   #ユーザーID
        self.winRate = 0   #勝率
        self.name = name   #表示名
        PlayerManager.countup()
        print(self.name,self.win,self.match,self.winRate,self.id)


    #インスタンスメソッド
    def winMatch(self):    #勝った時の処理
        self.win += 1
        self.match += 1
        #勝率の計算
        self.winRate = self.win / self.match * 100

    
    def loseMatch(self):   #負けた時の処理
        self.match += 1
        #勝率の計算
        self.winRate = self.win / self.match * 100
    
    def score(self):       #表示するときの処理
        m ="名前:"+ str(self.name) +" 勝率:" + str(self.winRate) + "% 勝ち数:" + str(self.win) + " 試合回数:"+str(self.match)
        return m

    def print(self):       #デバック用
        print(self,self.win,self.match,self.winRate,self.id)




# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


#変数置き場
member = ["kame"] #重複登録確認用ID置き場
instanceName = [] #インスタンス名の管理用 (表示名で登録 message.author)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    x = 0  #クラス変数が使えな勝ったので選手の数とする

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    #選手の登録
    if message.content == "!regist":
        for i in member:   #重複登録をさせないための処理
            if message.author.id == i:
                content = "登録済みです"
                await message.channel.send(content)
                break
        else:
            member.append(message.author.id)
            instanceName.append(str(message.author))
            instanceName[x] = PlayerManager(message.author.id,message.author) #インスタンス名をどうにかする
            content = str(message.author) + "さん登録しました"
            await message.channel.send(content)
            x += 1
    
    #戦績の記録
    if message.content == "!match":
        lose = [] #勝ち負けに適応したリストにインスタンス名をぶっこむ
        win = []  
        #動作確認のためboombot、lose win処理割愛
        for i in instanceName:
            i.winMatch()
    
    #戦績の表示
    if message.content == "!score":
        for i in instanceName:
            content = i.score()
            await message.channel.send(content)
        
        


    #botを終了させるコマンド
    if message.content == "!exit": 
        exit()
    
    #デバック用
    if message.content == "!print":
        print(f"member{member}, instanceName{instanceName}, x {x}")
        for i in instanceName:
            print(i.print())

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)


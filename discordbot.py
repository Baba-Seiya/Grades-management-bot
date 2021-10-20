# インストールした discord.py を読み込む
import discord
import pickle
import asyncio

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
        m ="名前:"+ str(self.name) +" 勝率:" + str(round(self.winRate,1)) + "% 勝ち数:" + str(self.win) + " 試合回数:"+str(self.match)
        return m

    def print(self):       #デバック用
        print(self,self.win,self.match,self.winRate,self.id)


# カスタム絵文字
EmojiA = "🅰️"
EmojiD = "\N{Turtle}"
EmojiOK= "🆗"
EmojiW = "✅"
EmojiL = "❌"

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

    



#変数置き場
memberID = ["kame"] #重複登録確認用ID置き場
member = {} #キー=id,値=インスタンス名のdict  
instanceName = [] #インスタンス名の管理用 (表示名で登録 message.author)
lose = [] #勝ち負けに適応したリストにインスタンス名をぶっこむ
win = []
A = []
D = []
#任意のチャンネルIDを記述
ch_id = 899475209214627863


#win lose dictを空にする関数
def reset():
    global win
    global lose
    global A
    global D

    win = []
    lose = []
    A = []
    D = []

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    x = 0  #クラス変数が使えな勝ったので選手の数とする

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    #選手の登録
    if message.content == "!regist":
        for i in memberID:
            #重複登録をさせないための処理
            if message.author.id == i:
                content = "登録済みです"
                await message.channel.send(content)
                break
        else:
            memberID.append(message.author.id)        #下3行クラス、dictへ追加
            instanceName.append(str(message.author))
            instanceName[x] = PlayerManager(message.author.id,message.author)
            member[message.author.id] = instanceName[x]
            content = str(message.author) + "さんを登録しました"
            await message.channel.send(content)
            x += 1
    
    #戦績の記録（手動メンションタイプ）
    if message.content == "!match":
          
        content = f"{EmojiA} = Attacker   {EmojiD} = Defender を選択して、完了したら{EmojiOK}を押してください。"
        msg = await message.channel.send(content)

        await msg.add_reaction(EmojiA)
        await msg.add_reaction(EmojiD)
        await msg.add_reaction(EmojiOK)
        reset()
    
    #戦績の表示
    if message.content == "!score":
        #製品版は勝率順にソートする
        for i in member:
            instancename = member[i]
            await message.channel.send(instancename.score())

    #help
    if message.content == "!help":
        content = "選手の登録　!regist\n戦績の記録　!match\n戦績の表示　!score\nbotの終了   　!exit"
        await message.channel.send(content)

    #botを終了させるコマンド
    if message.content == "!exit": 
        exit()
    
    #デバック用
    if message.content == "!print":
        print(f"memberID{memberID}, instanceName{instanceName}, x {x}")
        for i in instanceName:
            print(i.print())

#リアクションがついた時の動作
@client.event
async def on_reaction_add(reaction, user):
    global ch_id
    channel = client.get_channel(ch_id)
    if user.bot:
        return
    emoji =  reaction.emoji
#選手の振り分け    
    #Attackerへの振り分け
    if emoji == EmojiA:
        A.append(user.id)
        
    #Defenderへの振り分け
    if emoji == EmojiD:
        D.append(user.id)
    #完了した時の処理
    if emoji == EmojiOK:
        content = "どっちが勝ちましたか?\n Attackerが勝った場合✅　負けた場合❌を押してください"
        msg = await channel.send(content)
        await msg.add_reaction(EmojiW)
        await msg.add_reaction(EmojiL)
#勝敗登録  
    if emoji == EmojiW:
        for i in A:
            instance = member[i]
            instance.winMatch()
        for i in D:
            instance = member[i]
            instance.loseMatch()
        await channel.send('Attackerが勝ちとして記録しました。戦績を見る場合は!score')
    
    if emoji == EmojiL:
        for i in D:
            instance = member[i]
            instance.winMatch()
        for i in A:
            instance = member[i]
            instance.loseMatch()
        await channel.send("Defenderが勝ちとして記録しました。戦績を見る場合は!score")
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)


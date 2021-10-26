# インストールした discord.py を読み込む
import discord
import pickle
import asyncio

# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''

# 接続に必要なオブジェクトを生成
client = discord.Client()

#--------------------------class-----------------------
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
        m = str(self.name) +" 勝率:" + str(round(self.winRate,1)) + "% 勝ち数:" + str(self.win) + " 試合回数:"+str(self.match)        
        return m

    def print(self):       #デバック用
        print(self,self.win,self.match,self.winRate,self.id)

    #win 対戦回数の調整用のインスタンス
    def countupWin(self):
        self.win += 1
        self.winRate = self.win / self.match * 100
    def countdownWin(self):
        self.win -= 1
        self.winRate = self.win / self.match * 100
    def countupMatch(self):
        self.match += 1
        self.winRate = self.win / self.match * 100
    def countdownMatch(self):
        self.match -= 1
        self.winRate = self.win / self.match * 100

#-------------------------定義関数--------------------
#変数を別ファイルに保存する関数たち
#新しくファイルを作るとき
def newVariableFile():
    global member
    global memberID
    global instanceName
    with open('variable.pickle', mode='wb') as f:
            pickle.dump(memberID, f)
            pickle.dump(instanceName, f)

#保存用の関数
def saveVariableFile():
    global member
    global memberID
    global instanceName
    global memberNames

    keylist=[]
    vallist=[]
                                #不思議なことが起きたもんだ、なんで動いているのか、なんでエラーが出ないのかが分からないんだ。
                                # マストだと思ってたinstanceNameが引き継げなくてもなぜか動いてるんだ分からないけどうごいてるからいっか
    for key in member:
        val = member[key]
        keylist.append(key)
        vallist.append(val)
    
    #pickeleを使用し別のファイルに変数、リストを保存
    with open('variable.pickle', mode='wb') as f:

        pickle.dump(keylist, f)
        pickle.dump(keylist,f)
        pickle.dump(memberID,f)
        pickle.dump(member,f)
        pickle.dump(memberNames,f)
        


#読み込みの関数
def loadVariableFile():
    global member
    global memberID
    global instanceName
    global memberNames
    keylist = []
    #pickleで保存したデータの読み込み
    with open('variable.pickle', mode='rb') as f:
        try:
            keylist = pickle.load(f)
            memberID = pickle.load(f)
            instanceName =pickle.load(f)
            member = pickle.load(f)
            memberNames = pickle.load(f)
        except EOFError :
            pass
    try:
        for i in range(keylist.length):
            key = keylist[i]
            member[key] = instanceName[i]
    except AttributeError:
        pass

#勝率順にソートする関数
def sort():
    global member
    beforeList = []
    afterList = []
    for key in member:
        val = member[key]
        beforeList.append([val.winRate,val])
    for i in range(len(beforeList)):
        r = beforeList[i]
        if i == 0:
            afterList.append(beforeList[i])
        else:
            k = afterList[0]
            if r[0] >= k[0]:
                afterList.insert(0,beforeList[i]) 
            else:
                afterList.append(beforeList[i])
    return afterList

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

#--------------------------変数置き場-------------------------
memberID = ["kame"] #重複登録確認用ID置き場
member = {} #キー=id,値=インスタンス名のdict  
instanceName = [] #インスタンス名の管理用 (表示名で登録 message.author)
memberNames = {} #キー=表示名, 値=id
lose = [] #勝ち負けに適応したリストにインスタンス名をぶっこむ
win = []
A = []
D = []
#任意のチャンネルIDを記述
ch_id = 899475209214627863


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
    global member
    global memberID
    global instanceName

    #初めてプログラムを動かす場合下のコメントアウトを外す
    #newVariableFile()
    loadVariableFile()
    
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')



# ------------------メッセージ受信時に動作する処理------------
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
            if str(message.author.id) == i:
                content = "登録済みです"
                await message.channel.send(content)
                break
        else:#登録処理
            memberID.append(str(message.author.id))      
            instanceName.append(message.author)
            instanceName[x] = PlayerManager(str(message.author.id),str(message.author))
            member[str(message.author.id)] = instanceName[x]
            memberNames[str(message.author)] = str(message.author.id)
            content = str(message.author) + "さんを登録しました"
            await message.channel.send(content)
            x += 1
    
    #戦績の記録（手動メンションタイプ）
    if message.content == "!match":
          
        content = f"{EmojiA} = Attacker   {EmojiD} = Defender を選択して、完了したら{EmojiOK}を押してください。キャンセルは🚫"
        msg = await message.channel.send(content)

        await msg.add_reaction(EmojiA)
        await msg.add_reaction(EmojiD)
        await msg.add_reaction(EmojiOK)
        await msg.add_reaction(EmojiC)
        reset()
    
    #戦績の表示
    if message.content == "!score":
        #製品版は勝率順にソートする
        list = sort()
        x = 1
        for i in list:
            await message.channel.send(str(x) + "．" + i[1].score())
            x += 1
        
        
        """for i in member:
            instancename = member[i]
            await message.channel.send(instancename.score())"""

    #help
    if message.content == "!help":
        content = "選手の登録　!regist\n戦績の記録　!match\n戦績の表示　!score\nbotの終了   　!exit"
        await message.channel.send(content)

    #botを終了させるコマンド
    if message.content == "!exit":
        saveVariableFile()
        exit()
    
    #デバック用
    if message.content == "!print":
        print(f"memberID{memberID}, instanceName{instanceName}, x {x}")
        for i in instanceName:
            print(i.print())
    
    #class操作用
    if message.content == "!class":
        for i in memberNames:
            g = memberNames[i]
            print(i + " " + g)
        key = input("操作するIDを選んでください：")
        cnt = input("操作内容を打ってください（upmatch, downmachなど）：")
        con = input("操作回数を選んでください：")
        con = int(con)
        val = member[str(key)]
        
        if cnt == "upmatch":
            for i in range(con):
                val.countupMatch()
        if cnt == "downmatch":
            for i in range(con):
                val.countdownMatch()
        if cnt == "upwin":
            for i in range(con):
                val.countupWin()
        if cnt == "downwin":
                val.countdownWin()

#---------------------リアクションがついた時の動作----------------------
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
        for i in A:
                if i  == user.id: 
                    content = "技術不足により一度登録したリアクションをキャンセル出来ません　!matchからやり直してください"
                    reset()
                    await channel.send(content)
                    break

        for i in D:
            if i  == user.id: 
                content = "重複登録を検知し、キャンセルしました　!matchからやり直してください"
                reset()
                await channel.send(content)
                break      

        A.append(user.id)
    #Defenderへの振り分け
    if emoji == EmojiD:
        for i in D:
                if i  == user.id: 
                    content = "技術不足により一度登録したリアクションをキャンセル出来ません　!matchからやり直してください"
                    reset()
                    await channel.send(content)
                    break

        for i in A:
            if i  == user.id: 
                content = "重複登録を検知し、キャンセルしました　!matchからやり直してください"
                reset()
                await channel.send(content)
                break

        D.append(user.id)

    #完了した時の処理
    if emoji == EmojiOK:
        content = "どっちが勝ちましたか?\n Attackerが勝った場合✅　負けた場合❌を押してください キャンセルは🚫"
        msg = await channel.send(content)
        await msg.add_reaction(EmojiW)
        await msg.add_reaction(EmojiL)
        await msg.add_reaction(EmojiC)
        
#勝敗登録  
    if emoji == EmojiW:
        for i in A:
            instance = member[str(i)]
            instance.winMatch()
        for i in D:
            instance = member[str(i)]
            instance.loseMatch()
        await channel.send('Attackerが勝ちとして記録しました。戦績を見る場合は!score')
    
    if emoji == EmojiL:
        for i in D:
            instance = member[str(i)]
            instance.winMatch()
        for i in A:
            instance = member[str(i)]
            instance.loseMatch()
        await channel.send("Defenderが勝ちとして記録しました。戦績を見る場合は!score")

    if emoji == EmojiC:
        content = "キャンセルしました　!matchからやり直してください"
        await channel.send(content)
        reset()

#リアクションを消した時の動作 #わからん動かん
@client.event
async def on_reaction_remove(reaction, user):
    emoji =  reaction.emoji
    if emoji == EmojiA:
        A.remove(user.id)
        print("kamesan")
    if emoji == EmojiD:
        D.remove(user.id)
        print("kamekame")
    
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)


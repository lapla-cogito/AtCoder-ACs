#import
% matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import urllib.request
import time
import datetime
from datetime import datetime
from datetime import timedelta
import seaborn as sns
import tweepy
from bs4 import BeautifulSoup
from flask import Flask,request,render_template
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl

# ユーザーの入力
Users = input().split()
Usercount=0
#ツイート用のユーザーを入れる
Userfortw=[]
#ツイートできるタイミングかどうか(グラフの生成が終わっていればTrue)
readyTotw=False

#グラフの基礎設定
plt.style.use('default')
sns.set()
sns.set_style('whitegrid')

#1個前のACした日
prevACtime=0
#入力された中で1番解いてる人の問題数
highest=0
tod = datetime.date(datetime.today())

#取得後に追記
CK = "Consumer Key を入力"
CS = "Consumer Secret を入力"

def tweet():
        senten='AtCoder AC count battle!\n'
        for i in range(Usercount):
            senten+=Userfortw[i]
            if not i==len(range(Usercount))-1:
               senten+=' vs.'
        senten+='\n#ACbattle'
        return senten
        
#入力されたユーザーが存在するかどうか
def existID(s):
        try:
            ACurl = urllib.request.urlopen("https://beta.atcoder.jp/users/" + s)
            return True
        except:
            return False

for i in range(len(Users)):    
        #ACした時間を入れていく
        time=[]
        #ACした数を入れていく
        ac=[]
        #ACした問題のコンテスト名
        contests=[]
        #ACした問題名を入れていく
        problems=[]
        #AC count for each user
        ACs=0
        if not existID(Users[0]):
                continue
        url = "https://kenkoooo.com/atcoder/atcoder-api/results?user="+Users[0]
        jsonRes = urllib.request.urlopen(url)
        jsonData = json.loads(jsonRes.read().decode("utf-8"))
        jsonData = sorted(jsonData,key=lambda x:(x["result"],x["epoch_second"]))
        Usercount+=1
        #previous
        prevTime = str(jsonData[0]["epoch_second"])
        #ローカルタイムに変換
        prevTime = datetime.fromtimestamp(int(prevTime))
    
        for j in range(len(jsonData)):
            l = int(j)
            breakFlag=False
            subData = jsonData[l]
            #ソートしてあるのでACじゃないステータスが出てきたらそれ以降はACは無い
            if subData["result"] != "AC":
                break
             
            #重複ACの排除
            for k in range(len(problems)):
                m=int(k)
                if subData["contest_id"]==contests[m] and subData["problem_id"]==problems[m]:
                    breakFlag=True
                    break

            if breakFlag:
                continue             
            else:
                #ACを出した時間(UNIX時間)
                ACTime=subData["epoch_second"]
                
                if l==0:
                    mon=ACTime
                
                 #ローカルタイムに変換
                fixedTime = datetime.fromtimestamp(ACTime)
                
                if l==0:
                    prevACtime=fixedTime
                 
                ACs+=1
                time.append(fixedTime)
                ac.append(ACs)
                contests.append(subData["contest_id"])
                problems.append(subData["problem_id"])
                prevTime = fixedTime
                    
        if ACs>highest:
            highest=ACs

        #最終ACから現在の日まで線を引く
        if prevTime.day!=tod.day and prevTime.month!=tod.month and prevTime.year!=tod.year:
          day=datetime.date(prevTime)
          while day<=tod:
            time.append(day)
            ac.append(ACs)
            day+=timedelta(1)
          
        plt.plot(time, ac, label=Users[0])
        Userfortw.append(Users[0])
        del Users[0]
  
# Graph
plt.xlabel("Date")
plt.ylabel("AC counts")
plt.ylim(0, highest*1.1)
plt.xticks(rotation=315)
print(tweet())
plt.legend()
plt.savefig('graph.png')
#全ての工程が終了
readyTotw=True

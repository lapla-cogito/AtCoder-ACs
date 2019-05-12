#import
% matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import urllib.request
import seaborn as sns
import tweepy
import webbrowser as web
import time
import datetime
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from flask import Flask,request,render_template
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl


# ユーザーの入力
Users = input().split()
Usercount=0
#グラフの基礎設定
plt.style.use('default')
sns.set()
sns.set_style('whitegrid')

#1個前のACした日
prevACtime=0
#入力された中で1番解いてる人の問題数
highest=0
tod = datetime.date(datetime.today())

#コンテスト情報の取得(うんらてｄがらてｄかが簡単に分かる)
contestURL="https://kenkoooo.com/atcoder/resources/contests.json"
contestRes = urllib.request.urlopen(contestURL)
contestData = json.loads(contestRes.read().decode("utf-8"))
        
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
        #ACした問題のコンテスト名
        contests=[]
        #ACした問題名を入れていく
        problems=[]
        ac=[]
        #RPS counts
        RPS=0
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
                 
                rate=False
                for ra in range(len(contestData)):
                  ranu=int(ra)
                  data=contestData[ranu]
                  if data["id"]==subData["contest_id"] and data["rate_change"]!="-" and not(data["rate_change"]=="All" and data["start_epoch_second"]<1468670400):
                    rate=True
                    break
                    
                if rate==True: 
                    RPS+=subData["point"]
                    time.append(fixedTime)
                    ac.append(RPS)
                    contests.append(subData["contest_id"])
                    problems.append(subData["problem_id"])
                    prevTime = fixedTime
                    print(subData["problem_id"]+" "+data["rate_change"])
                    
        if RPS>highest:
            highest=RPS
        #最終ACから現在の日までx軸に平行な線を引く
        if prevTime.day!=tod.day and prevTime.month!=tod.month and prevTime.year!=tod.year:
          day=datetime.date(prevTime)
          while day<=tod:
            time.append(day)
            ac.append(RPS)
            day+=timedelta(1)
          
        #tips:7人以上の入力で色がループする
        plt.plot(time, ac, label=Users[0])
        del Users[0]
  
# Graph
print(RPS)
plt.xlabel("Date")
plt.ylabel("RPS counts")
plt.ylim(0, highest*1.1)
plt.xticks(rotation=315)
plt.legend()
#plt.savefig('graph.png')

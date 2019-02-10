#import
% matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import urllib.request
import seaborn as sns
import tweepy
import oauth2
import webbrowser as web
import cgi
import time
import datetime
from datetime import datetime
from datetime import timedelta
from twython import Twython, TwythonError
from bs4 import BeautifulSoup
from flask import Flask,request,render_template
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
from browser import document

def ACs():
  
  # ���[�U�[�̓���
  #Users = input().split()
  Users=float(document["inputusers"].value)
  Usercount=0
  #�c�C�[�g�p�̃��[�U�[������
  Userfortw=[]
  #�c�C�[�g�ł���^�C�~���O���ǂ���(�O���t�̐������I����Ă����True)
  readyTotw=False

  #�O���t�̊�b�ݒ�
  plt.style.use('default')
  sns.set()
  sns.set_style('whitegrid')

  #1�O��AC������
  prevACtime=0
  #���͂��ꂽ����1�ԉ����Ă�l�̖�萔
  highest=0
  tod = datetime.date(datetime.today())


  def tweetsen():
          senten='AtCoder AC count battle!\n'
          for i in range(Usercount):
              senten+=Userfortw[i]
              if not i==len(range(Usercount))-1:
                 senten+=' vs.'
          senten+='\n#ACbattle'
          return senten
      
  def tweet():
    CK=""
    CS=""
    AT=""
    AS=""
    medurl="https://upload.twitter.com/1.1/media/upload.json"
    urltex = "https://api.twitter.com/1.1/statuses/update.json"
    twitter=OAuthSession(CK,CS,AT,AS)
    graprhim={"media":open('graph.png','rb')}
    posmed=twitter.post(medurl,files=files)
  
  #�A�b�v���[�h�Ɏ��s
    if req_media.status_code!=200:
      print("�摜�A�b�v���[�h���s!%s",req_media.text)
      exit()
  
    medid=json.loads(req_media.text)['media_id']
    param={'status':'AC battle',"media_ids":[media_id]}
    req_media=twitter.post(urltex,params=params)
  #�A�b�v���[�h�Ɏ��s
    if req_media.status_code!=200:
      print("�e�L�X�g�A�b�v�f�[�g���s!%s",req_media.text)
      exit()
    print("tweeted")
        
#���͂��ꂽ���[�U�[�����݂��邩�ǂ���
  def existID(s):
          try:
              ACurl = urllib.request.urlopen("https://beta.atcoder.jp/users/" + s)
              return True
          except:
              return False

  for i in range(len(Users)):    
          #AC�������Ԃ����Ă���
          time=[]
          #AC�����������Ă���
          ac=[]
          #AC�������̃R���e�X�g��
          contests=[]
          #AC������薼�����Ă���
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
          #���[�J���^�C���ɕϊ�
          prevTime = datetime.fromtimestamp(int(prevTime))
    
          for j in range(len(jsonData)):
              l = int(j)
              breakFlag=False
              subData = jsonData[l]
              #�\�[�g���Ă���̂�AC����Ȃ��X�e�[�^�X���o�Ă����炻��ȍ~��AC�͖���
              if subData["result"] != "AC":
                  break
             
              #�d��AC�̔r��
              for k in range(len(problems)):
                  m=int(k)
                  if subData["contest_id"]==contests[m] and subData["problem_id"]==problems[m]:
                      breakFlag=True
                      break

              if breakFlag:
                  continue             
              else:
                  #AC���o��������(UNIX����)
                  ACTime=subData["epoch_second"]
                
                  if l==0:
                      mon=ACTime
                
                   #���[�J���^�C���ɕϊ�
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

          #�ŏIAC���猻�݂̓��܂Ő�������
          if prevTime.day!=tod.day and prevTime.month!=tod.month and prevTime.year!=tod.year:
            day=datetime.date(prevTime)
            while day<=tod:
              time.append(day)
              ac.append(ACs)
              day+=timedelta(1)
          
          #tips:7�l�ȏ�̓��͂ŐF�����[�v����
          plt.plot(time, ac, label=Users[0])
          Userfortw.append(Users[0])
          del Users[0]
  
  # Graph
  plt.xlabel("Date")
  plt.ylabel("AC counts")
  plt.ylim(0, highest*1.1)
  plt.xticks(rotation=315)
  #plt.legend()
  res=document["result"]
  
  #���|�I�f�o�b�O�p(Brython��������Ɠ�����)
  res.text=tweet()
  plt.savefig('graph.png')
  #�S�Ă̍H�����I��
  readyTotw=True

 #HTML����send���ꂽ����s
runbu=document["run"]
runbu.bind("click",ACs)
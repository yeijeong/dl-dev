import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
from datetime import datetime
import datetime

import pandas as pd
import time

import pythoncom
import time

import pymysql

conn = pymysql.connect(
    host='34.64.240.96'
    , user='root'
    , password='tndusWkd1.'
    , db='final_project'
    , charset='utf8'
)
cur = conn.cursor()


basic_url = "https://finance.naver.com/sise/" # 코스피
exchange_url = "https://finance.naver.com/marketindex/" # 환율


# 현재 시간을 기록

stoptime = datetime.datetime.now().time()
while True:
    if stoptime.strftime('%p') == 'PM' and stoptime.hour == 3 and stoptime.minute >= 30: # 오후 3시 반 이후인지 확인
        break # 3시 30에 멈추는 코드
    else:
        fp = urllib.request.urlopen(basic_url) # 3시30이 아니면 계속 실행
        source = fp.read()
        fp.close() 

        soup = BeautifulSoup(source, 'html.parser')
        soup = soup.findAll("span",class_="num")
        kospi_value = soup[1].string #코스피 지수
        # now = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        
        #환율 실시간
        exchange_url = "https://finance.naver.com/marketindex/"
        fp = urllib.request.urlopen(exchange_url)
        source = fp.read()
        fp.close()

        soup = BeautifulSoup(source, 'html.parser')
        soup = soup.findAll("span",class_="value")

        # 결과값을 변수에 저장
        exchange = soup[0].string #미국환율 지수
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        re_time = now

        # df = pd.DataFrame([{'re_time': now, 'kospi': kospi_value, 'exchange': exchange}])
        # print(df)
        sql = "INSERT INTO kospi_exchage_real (Ymd_Time, Kospi, Exchange) VALUES (%s, %s, %s)" % ("'"+now+"'", "'"+kospi_value+"'", "'"+exchange+"'")
        cur.execute(sql)
        print(sql)
        conn.commit()

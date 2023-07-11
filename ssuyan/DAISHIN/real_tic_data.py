import sys
from PyQt5.QtWidgets import *
import win32com.client
import pandas as pd
import numpy as np

import pymysql
conn = pymysql.connect(
    host='34.64.240.96'
    , user='root'
    , password='tndusWkd1.'
    , db='final_project'
    , charset='utf8'
)
cur = conn.cursor()

list = []
zero_df = pd.DataFrame(columns=['시분초','시가','대비','체결량','거래량'])
        
class CpEvent:
    instance = None
 
    def OnReceived(self):
        # time = CpEvent.instance.GetHeaderValue(3)  # 시간
        timess = CpEvent.instance.GetHeaderValue(18)  # 초
        exFlag = CpEvent.instance.GetHeaderValue(19)  # 예상체결 플래그
        cprice = CpEvent.instance.GetHeaderValue(13)  # 현재가
        diff = CpEvent.instance.GetHeaderValue(2)  # 대비
        cVol = CpEvent.instance.GetHeaderValue(17)  # 순간체결수량
        vol = CpEvent.instance.GetHeaderValue(9)  # 거래량
 
        if (exFlag == ord('1')):  # 동시호가 시간 (예상체결)
            list.append([timess,cprice,diff,cVol,vol])
            app_df = pd.DataFrame(data=list, columns=['시분초','시가','대비','체결량','거래량'])
            df = pd.concat([zero_df,app_df], ignore_index=True)
            print(df)
            JusikTimess = df['시분초'].to_list()
            JusikCprice = df['시가'].to_list()
            JusikDiff = df['대비'].to_list()
            JusikCVol = df['체결량'].to_list()
            JusikVol = df['거래량'].to_list()
            print(JusikTimess)
            for timess, cprice, diff, cvol, vol in zip(JusikTimess, JusikCprice, JusikDiff, JusikCVol, JusikVol):
                sql = "INSERT INTO jusik_tic_chart (JusikTimess, JusikCprice, JusikDiff, JusikCVol, JusikVol) VALUES (%s, %s, %s, %s, %s)" % ("'"+str(timess)+"'", "'"+str(cprice)+"'", "'"+str(diff)+"'", "'"+str(cvol)+"'","'"+str(vol)+"'")
                print(sql)
                cur.execute(sql)
            conn.commit()
           
            
        elif (exFlag == ord('2')):  # 장중(체결)
            list.append([timess,cprice,diff,cVol,vol])
            app_df = pd.DataFrame(data=list, columns=['시분초','시가','대비','체결량','거래량'])
            df = pd.concat([zero_df,app_df], ignore_index=True)
            print(df)
            JusikTimess = df['시분초'].to_list()
            JusikCprice = df['시가'].to_list()
            JusikDiff = df['대비'].to_list()
            JusikCVol = df['체결량'].to_list()
            JusikVol = df['거래량'].to_list()
            print(JusikTimess)
            for timess, cprice, diff, cvol, vol in zip(JusikTimess, JusikCprice, JusikDiff, JusikCVol, JusikVol):
                sql = "INSERT INTO jusik_tic_chart (JusikTimess, JusikCprice, JusikDiff, JusikCVol, JusikVol) VALUES (%s, %s, %s, %s, %s)" % ("'"+str(timess)+"'", "'"+str(cprice)+"'", "'"+str(diff)+"'", "'"+str(cvol)+"'","'"+str(vol)+"'")
                print(sql)
                cur.execute(sql)
            conn.commit()

class CpStockCur:
    def Subscribe(self, code):
        self.objStockCur = win32com.client.Dispatch("DsCbo1.StockCur")
        win32com.client.WithEvents(self.objStockCur, CpEvent)
        self.objStockCur.SetInputValue(0, code)
        CpEvent.instance = self.objStockCur
        self.objStockCur.Subscribe()
 
    def Unsubscribe(self):
        self.objStockCur.Unsubscribe()
 
 
 
class CpStockMst:
    def Request(self, code):
        # 연결 여부 체크
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False
 
        objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        objStockMst.SetInputValue(0, code)  # 종목 코드 - 한화에어로스페이스
        objStockMst.BlockRequest()
 
        rqStatus = objStockMst.GetDibStatus()
        rqRet = objStockMst.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            return False
 
        # 현재가 정보 조회
        code = objStockMst.GetHeaderValue(0)  # 종목코드
        name = objStockMst.GetHeaderValue(1)  # 종목명
        time = objStockMst.GetHeaderValue(4)  # 시간
        cprice = objStockMst.GetHeaderValue(11)  # 종가
        diff = objStockMst.GetHeaderValue(12)  # 대비
        open = objStockMst.GetHeaderValue(13)  # 시가
        high = objStockMst.GetHeaderValue(14)  # 고가
        low = objStockMst.GetHeaderValue(15)  # 저가
        offer = objStockMst.GetHeaderValue(16)  # 매도호가
        bid = objStockMst.GetHeaderValue(17)  # 매수호가
        vol = objStockMst.GetHeaderValue(18)  # 거래량
        vol_value = objStockMst.GetHeaderValue(19)  # 거래대금
 
        print("코드 이름 시간 현재가 대비 시가 고가 저가 매도호가 매수호가 거래량 거래대금")
        print(code, name, time, cprice, diff, open, high, low, offer, bid, vol, vol_value)
        
        return True
 
 
class MyWindow(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLUS API TEST")
        self.setGeometry(300, 300, 300, 150)
        self.isRq = False
        self.objStockMst = CpStockMst()
        self.objStockCur = CpStockCur()
 
        btn1 = QPushButton("요청 시작", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)
 
        btn2 = QPushButton("요청 종료", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)
 
        btn3 = QPushButton("종료", self)
        btn3.move(20, 120)
        btn3.clicked.connect(self.btn3_clicked)

 
    def StopSubscribe(self):
        if self.isRq:
            self.objStockCur.Unsubscribe()
        self.isRq = False
 
    def btn1_clicked(self):
        testCode = "A012450"
        if (self.objStockMst.Request(testCode) == False):
            exit()
 
        self.objStockCur.Subscribe(testCode)

    
        print("빼기빼기=====================================")
        print("실시간 현재가 요청 시작")
        self.isRq = True 


    def btn2_clicked(self):
        self.StopSubscribe()
 
 
    def btn3_clicked(self):
        self.StopSubscribe()
        exit()
        
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


conn.close()
import pythoncom
import win32com.client as winAPI
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

STAND_BY = 0
RECEIVED = 1


class XASessionEvents:
    login_state = STAND_BY

    def OnLogin(self, code, msg):
        XASessionEvents.login_state = RECEIVED
        print(msg)

    def OnDisconnect(self, code, msg):
        pass


class XAQueryEvents:
    query_state = STAND_BY

    def OnReceiveData(self, code):
        XAQueryEvents.query_state = RECEIVED

    def OnReceiveMessage(self, error, nMessageCode, szMessage):
        print(szMessage)



import datetime
import time

SERVER_PORT = 20001
SHOW_CERTIFICATE_ERROR_DIALOG = False
REPEATED_DATA_QUERY = 1
TRANSACTION_REQUEST_EXCESS = -21
TODAY = datetime.datetime.now().strftime('%Y%m%d')

if __name__ == "__main__":
    id = "ssuyan"
    password = "tndus1!!"
    certificate_password = "qkrtndus1!!"
    xa_session = winAPI.DispatchWithEvents("XA_Session.XASession", XASessionEvents)

    # demo.ebestsec.co.kr => 모의투자 
    # hts.ebestsec.co.kr => 실투자
    xa_session.ConnectServer("hts.ebestsec.co.kr", SERVER_PORT)
    xa_session.Login(id, password, certificate_password, SERVER_PORT, SHOW_CERTIFICATE_ERROR_DIALOG)

    while XASessionEvents.login_state is STAND_BY:
        pythoncom.PumpWaitingMessages()
    XASessionEvents.login_state = STAND_BY


TR = "t1310"
xa_query = winAPI.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
xa_query.ResFileName = "C:\\eBEST\\xingAPI\\Res\\" + TR + ".res"

xa_query.SetFieldData("t1310InBlock", "timegb", 0, 1)

while True:
    ret = xa_query.Request(False)
    """ Receiving error message, keep requesting until accepted """
    if ret is TRANSACTION_REQUEST_EXCESS:  # -34
        time.sleep(0.8)
    else:
        break
""" Wait window's event message """
while XAQueryEvents.query_state is STAND_BY:
    pythoncom.PumpWaitingMessages()
XAQueryEvents.query_state = STAND_BY


import win32com.client
import pythoncom
import time
import pandas as pd
import numpy as np
import time
import threading

list = []
ebset_df = pd.DataFrame(columns=['종목코드', '시간', '현재가', '체결수량', '거래량', '매도체결수량', '매수체결수량'])
shcode_list = ['064350', '017670', '005490', '014680', '012450', '051900', '009150', '066570', '108320', '047810', '000660', '010140', '035420', '005380', '009830', '052690', '034020', '005070', '005420', '042700', '028050', '068270', '137310', '005930', '017960', '075580', '003490']

class XReal_S3_:
    def __init__(self):
        super().__init__()
        self.count = 0

    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        stockcode = self.GetFieldData("OutBlock", "shcode")
        chetime = self.GetFieldData("OutBlock", "chetime")
        price = self.GetFieldData("OutBlock", "price")
        cvolume = self.GetFieldData("OutBlock", "cvolume")
        volume = self.GetFieldData("OutBlock", "volume")
        mdvolume = self.GetFieldData("OutBlock", "mdvolume")
        msvolume = self.GetFieldData("OutBlock", "msvolume")
        # print("종목코드;{0}, 시간;{1}, 현재가;{2}, 체결수량;{3}, 거래량;{4}, 매도체결수량;{5}, 매수체결수량;{6}".format(stockcode, chetime, price, cvolume, volume, mdvolume, msvolume))
        # print(self.count, stockcode, chetime, price, cvolume, volume, mdvolume, msvolume)
        
        
        list.append([stockcode, chetime, price, cvolume, volume, mdvolume, msvolume])
        app_df = pd.DataFrame(data=list, columns=['종목코드', '시간', '현재가', '체결수량', '거래량', '매도체결수량', '매수체결수량'])
        df = pd.concat([ebset_df,app_df], ignore_index=True)
        # print(df)
        

        tablename = 'jusik_real_A'+stockcode

        sql = f"INSERT INTO %s (StockCode, CheTime, Price, CVolume, Volume, MdVolume, MsVolume) VALUES (%s, %s, %s, %s, %s, %s, %s)" % (tablename,"'"+str(stockcode)+"'", "'"+str(chetime)+"'", "'"+str(price)+"'", "'"+str(cvolume)+"'","'"+str(volume)+"'","'"+str(mdvolume)+"'","'"+str(msvolume)+"'")
        cur.execute(sql)
        conn.commit()

    def start(self):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\S3_.res"  # RES 파일 등록
        
        for shcode in shcode_list:
            self.SetFieldData("InBlock", "shcode", shcode)
            self.AdviseRealData() 

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xreal
    
    def multithreading_xing(i):

        threads=[]

        for shcode in shcode_list:
            t = threading.Thread(target=OnReceiveRealData(shcode,i))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    def get_real_data():
        xreal = XReal_S3_.get_instance()
        xreal.start()

        while True:
            pythoncom.PumpWaitingMessages()
            if datetime.datetime.now().strftime('%H:%M') == '15:30':
                break
            
    get_real_data()




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

list = []
ebset_df = pd.DataFrame(columns=['종목코드', '시간', '현재가', '체결수량', '거래량', '매도체결수량', '매수체결수량'])

class XQuery_t1310:
    def __init__(self):
        super().__init__()
        self.is_data_received = False

    def OnReceiveData(self, tr_code):
        """
        이베스트 서버에서 ReceiveData 이벤트 받으면 실행되는 event handler
        """
        self.is_data_received = True
        stockcode = self.GetFieldData("t1310OutBlock1", "shcode", 0)
        chetime = self.GetFieldData("t1310OutBlock1", "chetime", 0)
        price = self.GetFieldData("t1310OutBlock1", "price", 0)
        cvolume = self.GetFieldData("t1310OutBlock1", "cvolume", 0)
        volume = self.GetFieldData("t1310OutBlock1", "volume", 0)
        mdvolume = self.GetFieldData("t1310OutBlock1", "mdvolume", 0)
        msvolume = self.GetFieldData("t1310OutBlock1", "msvolume", 0)
        print("종목코드;{0}, 시간;{1}, 현재가;{2}, 체결수량;{3}, 거래량;{4}, 매도체결수량;{5}, 매수체결수량;{6}".format(stockcode, chetime, price, cvolume, volume, mdvolume, msvolume))

        print("TR code => {0}".format(tr_code))

        list.append([stockcode, chetime, price, cvolume, volume, mdvolume, msvolume])
        app_df = pd.DataFrame(data=list, columns=['종목코드', '시간', '현재가', '체결수량', '거래량', '매도체결수량', '매수체결수량'])
        df = pd.concat([ebset_df,app_df], ignore_index=True)
        print(df)

        StockCode = df['종목코드'].to_list()
        CheTime = df['시간'].to_list()
        Price = df['현재가'].to_list()
        CVolume = df['체결수량'].to_list()
        Volume = df['거래량'].to_list()
        MdVolume = df['매도체결수량'].to_list()
        MsVolume = df['매수체결수량'].to_list()
        print(StockCode)
        for stockcode, chetime, price, cvolume, volume, mdvolume, msvolume in zip(StockCode, CheTime, Price, CVolume, Volume, MdVolume, MsVolume):
            sql = "INSERT INTO ebest_real_tic (StockCode, CheTime, Price, CVolume, Volume, MdVolume, MsVolume) VALUES (%s, %s, %s, %s, %s, %s, %s)" % ("'"+str(stockcode)+"'", "'"+str(chetime)+"'", "'"+str(price)+"'", "'"+str(cvolume)+"'","'"+str(volume)+"'","'"+str(mdvolume)+"'","'"+str(msvolume)+"'")
            print(sql)
            cur.execute(sql)
        conn.commit()

    def request(self):
    # 매수 매도 체결 수량 컬럼추가

        """
        이베스트 서버에 일회성 TR data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1310.res"  # RES 파일 등록
        self.SetFieldData("t1310InBlock", "shcode", 0, "012450")  # 한화에어로스페이스
        err_code = self.Request(False)  # data 요청하기 --  연속조회인경우만 True

        if err_code < 0:
            print("error... {0}".format(err_code)) # data 요청하기 --  연속조회인경우만 True

    @classmethod
    def get_instance(cls):
        xq_t1310 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq_t1310

list = []
ebset_df = pd.DataFrame(columns=['종목코드', '시간', '현재가', '체결수량', '거래량', '매도체결수량', '매수체결수량'])

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
        print("종목코드;{0}, 시간;{1}, 현재가;{2}, 체결수량;{3}, 거래량;{4}, 매도체결수량;{5}, 매수체결수량;{6}".format(stockcode, chetime, price, cvolume, volume, mdvolume, msvolume))
        print(self.count, stockcode, chetime, price, cvolume, volume, mdvolume, msvolume)
        
        list.append([stockcode, chetime, price, cvolume, volume, mdvolume, msvolume])
        app_df = pd.DataFrame(data=list, columns=['종목코드', '시간', '현재가', '체결수량', '거래량', '매도체결수량', '매수체결수량'])
        df = pd.concat([ebset_df,app_df], ignore_index=True)
        print(df)

        StockCode = df['종목코드'].to_list()
        CheTime = df['시간'].to_list()
        Price = df['현재가'].to_list()
        CVolume = df['체결수량'].to_list()
        Volume = df['거래량'].to_list()
        MdVolume = df['매도체결수량'].to_list()
        MsVolume = df['매수체결수량'].to_list()
        print(StockCode)
        
        for stockcode, chetime, price, cvolume, volume, mdvolume, msvolume in zip(StockCode, CheTime, Price, CVolume, Volume, MdVolume, MsVolume):
            sql = "INSERT INTO ebest_real_tic (StockCode, CheTime, Price, CVolume, Volume, MdVolume, MsVolume) VALUES (%s, %s, %s, %s, %s, %s, %s)" % ("'"+str(stockcode)+"'", "'"+str(chetime)+"'", "'"+str(price)+"'", "'"+str(cvolume)+"'","'"+str(volume)+"'","'"+str(mdvolume)+"'","'"+str(msvolume)+"'")
            print(sql)
            cur.execute(sql)
        conn.commit()

    def start(self):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\S3_.res"  # RES 파일 등록
        self.SetFieldData("InBlock", "shcode", "012450")
        self.AdviseRealData()   # 실시간데이터 요청

    def add_item(self, stockcode):
        # 실시간데이터 요청 종목 추가
        self.SetFieldData("InBlock", "shcode", stockcode)
        self.AdviseRealData()

    def remove_item(self, stockcode):
        # stockcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(stockcode)

    def end(self):
        self.UnadviseRealData()  # 실시간데이터 요청 모두 취소

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xreal



if __name__ == "__main__":
    def get_single_data():
        xq_t1310 = XQuery_t1310.get_instance()
        xq_t1310.request()

        while xq_t1310.is_data_received == False:
            pythoncom.PumpWaitingMessages()


    def get_real_data():
        xreal = XReal_S3_.get_instance()
        xreal.start()

        while True:
            pythoncom.PumpWaitingMessages()
            xreal.add_item("012450")  # 한화에어로스페이스 주식

    # get_single_data()
    get_real_data()
    
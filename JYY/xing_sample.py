# -*- coding: utf-8 -*-

# date : 2020/07/14
# xing api sample
#  - login
#  - 잔고조회 : T0424
#  - 주문조회 : T0425
#  - Q검색리스트 : T1826
#  - Q검색 : T1825
#  - 분 시세조회 : T8412
#  - 일 시세조회 : T8413
#
# 보다 자세한 내용을 아래 tistory 참고
# https://money-expert.tistory.com/14
# https://money-expert.tistory.com/17
# https://money-expert.tistory.com/18
# https://money-expert.tistory.com/18 : T8401

import win32com.client
import pythoncom
import sys
import time
import json
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

# ======================================================
# 위치가 틀리다면 수정하여야 하는 부분
# ======================================================
XING_PATH = "C:\\eBEST\\xingAPI\\"
# 위치가 틀리다면 수정하여야 하는 부분 끝
# ======================================================

# ======================================================
# 수정하여야 하는 부분
# ======================================================
server_add = "hts.ebestsec.co.kr"
id = "ebest id"
passwd = "로그인 암호"
cert_passwd = "공인인증서 암호"
account_number = "주식 계좌번호" 
account_pwd = "주식계좌 암호"   
if 0 : #모의투자
    server_add = "demo.ebestsec.co.kr"
    passwd = "모의투자 사이트 로그인암호"
    account_number = '모의주식 계좌번호'
    account_pwd = "모의 주식계좌 암호"           
# ======================================================
# 수정하여야 하는 부분 끝
# ======================================================


def read_csv(fname) :
    data = []
    with open(fname, 'r', encoding='UTF8') as FILE :
        csv_reader = csv.reader(FILE, delimiter=',', quotechar='"')
        for row in csv_reader :
            data.append(row)
    return data


#def read_data_from_file(fname) :
def save_to_file_csv(file_name, data) :
    with open(file_name,'w',encoding="cp949") as make_file: 
        # title 저장
        vals = data[0].keys()
        ss = ''
        for val in vals:
            val = val.replace(',','')
            ss += (val + ',')
        ss += '\n'
        make_file.write(ss)

        for dt in data:
            vals = dt.values()
            ss = ''
            for val in vals:
                sval = str(val) 
                sval = sval.replace(',','')
                ss += (sval + ',')
            ss += '\n'
            make_file.write(ss)
    make_file.close()

def save_to_file_json(file_name, data) :
    with open(file_name,'w',encoding="cp949") as make_file: 
       json.dump(data, make_file, ensure_ascii=False, indent="\t") 
    make_file.close()

def load_json_from_file(file_name, err_msg=1) :
    try :
        with open(file_name,'r',encoding="cp949") as make_file: 
           data=json.load(make_file) 
        make_file.close()
    except  Exception as e : # 또는 except : 
        data = {}
        if err_msg :
            print(e, file_name)
    return data

TODAY = time.strftime("%Y%m%d")
TODAY_TIME = time.strftime("%H%M%S")
TODAY_S = time.strftime("%Y-%m-%d")

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("xing_sample_ui.ui", self)
        #init
        self.query_list = []

    def clear_message(self) :
        self.ui.listWidget_msg.clear()
    def show_message(self, pr) :
        self.ui.listWidget_msg.addItem(pr)
        self.ui.listWidget_msg.scrollToBottom()

    # T0424 잔고 받기
    def Balance_0424(self) :
        ret, bals = get_balance('all')  # 모든 종목 정보를 얻는다. 특정 종목을 원하면 해당하는 코드입력
        if ret >= 0 :
            pr = '=== 잔고 ==='
            self.show_message(pr)
            pr = ' code  balance '
            self.show_message(pr)
            pr = '--------------'
            self.show_message(pr)

            for bal in bals[0] :        
                pr = bal['code'] + ' ' + str(bal['total'])
                self.show_message(pr)

    # T0424 잔고 받기
    def OrderResults_0425(self) :
        self.clear_message()
        ordered = order_status_tr(kind='0', code='all') # kind = '0'(전체), '1'(체결), '2'(미체결)
        if 'error' in ordered[0] : # 오류
            self.show_message("0425 : error returned")
            return

        # orders[1] : 주문 내역
        order_num = ordered[2][0]['total']
        if order_num > 0 :
            pr = '  주문결과 '
            self.show_message(pr)
            pr = '--------------------------'
            self.show_message(pr)
            pr = '총 주문수: ' +  str(order_num)
            self.show_message(pr)

            # 취소 주문 : price == 0
            # 미체결 : 'executed_volume' == 0
            # 체결 :  'executed_volume' == volume
            for order in ordered[0] :
                if order['price'] == 0 : #취소주문
                    pr = '취소  : ' + order['market']
                    self.show_message(pr)
                elif order['executed_volume'] == 0 : #미체결
                    pr = '미체결: ' + order['market']
                    self.show_message(pr)
                elif order['executed_volume'] ==  order['volume']: #미체결
                    pr = '체결  : ' + order['side'] + ' ' + order['market'] + ' 가격: ' + str(order['price']) + ' 수량: ' +str(order['volume'])
                    self.show_message(pr)
                else :
                    pr = 'unknown'
                    self.show_message(pr)
                print(order)

            # orders[1] : 체결에 대한 총괄 정보
            # {'ord_total':ord_total, 'ord_fee':ord_fee, 'ord_tax':ord_tax})
            pr = '--------------------------'
            self.show_message(pr)            
            ord_summary = ordered[1][0]
            pr = '주문총수량 : ' + str(ord_summary['ord_total'])
            self.show_message(pr)
            pr = '주문수수료 : ' + str(ord_summary['ord_fee'])
            self.show_message(pr)
            pr = '주문세금   : ' + str(ord_summary['ord_tax'])
            self.show_message(pr)
            pr = '--------------------------'
            self.show_message(pr)

    # t1825 Q 검색 리스트 받기
    def Q_Query_1825(self) :
        if self.query_list == [] :
            self.show_message('press 1826 first')
            return

        for lst in self.query_list :
            time.sleep(1)
            pr = "\n=== " + lst[1] +  " ==="
            self.show_message(pr)
            res = get_q_query(lst[0])
            if 'error' in res[0] :
                self.show_message (res[0]['error']['message'])
            else :
                if len(res) > 1 :
                    pr = "total : " + str(res[0][0]['total'])                    
                    self.show_message (pr)
                    cnt = 0
                    for itm in res[1] :
                        pr = itm['code'] + ' ' + itm['name'] +' ' + str(itm['price']) + ' ' + str(itm['gubun'])
                        self.show_message(pr)
                        if cnt > 10 :
                            break
                        cnt+=1
                else :
                    self.show_message ("total : 0")

    # t18256 Q 검색 결과 받기
    def Q_List_1826(self) :
        rest = get_q_query_list('0')
        if 'error' in rest[0] :
            self.show_message(rest[0]['error']['message'])
        self.query_list = rest[0] 

        for query in self.query_list :
            pr = query[0] + ' ' + query[1]
            self.show_message(pr)
    
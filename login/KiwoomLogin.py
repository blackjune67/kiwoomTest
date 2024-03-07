from platform import python_compiler
import sys 
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
import pythoncom
import queue

class KiwoomLogin:
    def __init__(self) -> None:
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)
        self.tr_queue = queue.Queue()
        self.login = False
        self.tr = False
        self.tr_data={}

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        while self.login is False:
            pythoncom.PumpWaitingMessages()

    def OnEventConnect(self, code):
        self.login = True
        print("로그인 성공!!", code)
        print("==============================================")

    def SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def CommRqData(self, rqname, trcode, next, screen):
        self.tr = False
        # 서버로부터 값이 올 때까지 대기하도록 추가
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", trcode, rqname, next, screen)
        while self.tr is False:
            pythoncom.PumpWaitingMessages()

    # * 행에 대한 데이터 가져오기
    def GetCommData(self, trcode, rqname, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
        return data.strip()
    
    def OnReceiveTrData(self, screen, rqname, trcode, record, next):
        self.tr = True

        # rows = self.GetRepeatCnt(trcode, record)
        # if rows == 0:
        #     rows = 1

        # data = []
        # for row in range(rows):
        #     date = self.GetCommData(trcode, rqname, row, "일자")
        #     open = self.GetCommData(trcode, rqname, row, "시가")
        #     high = self.GetCommData(trcode, rqname, row, "고가")
        #     low  = self.GetCommData(trcode, rqname, row, "저가")
        #     close= self.GetCommData(trcode, rqname, row, "현재가")
        #     data.append([date, open, high, low, close])

        # self.tr_queue.put((data, next))
        name = self.GetCommData(trcode, rqname, 0, "종목명")
        
        data = (name)
        self.tr_data[trcode] = data
        print("==> name : ", data)
        print("==============================================")
        
        # name = self.GetCommData(trcode, rqname, 0, "종목명")
        # print("==> 종목명 : ", name)

    def GetRepeatCnt(self, trcode, record):
        data = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, record)
        return data
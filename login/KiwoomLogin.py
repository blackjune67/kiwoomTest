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
    
    # ! 요청 데이터
    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        self.tr = True
        print("TR MSG : ", sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg)

        # self.sPre

        # self.SetInputValue("종목코드", code)
        # self.SetInputValue("틱범위", 1)
        # self.SetInputValue("수정주가구분", 0)
        # self.CommRqData("myrequest", "opt10081", 0, "0101")

    def tickChart(self, code):
        self.SetInputValue("종목코드", code)
        self.SetInputValue("틱범위", 1)
        self.SetInputValue("수정주가구분", 0)
        self.CommRqData('opt10079_req', "opt10079", "0", "0101")
        

    def GetRepeatCnt(self, trcode, record):
        data = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, record)
        return data
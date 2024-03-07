from platform import python_compiler
import sys 
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
import pythoncom
from KiwoomLogin import KiwoomLogin

if __name__ == "__main__":
    app = QApplication(sys.argv)

    kiwoom = KiwoomLogin()
    kiwoom.CommConnect()

    # TODO 주식틱차트조회요청 [opt10079]
    # kiwoom.SetInputValue("종목코드", "005930")
    # kiwoom.SetInputValue("틱범위", "1:1");

    # kiwoom.SetInputValue("종목코드", "005930")
    # kiwoom.SetInputValue("기준일자", "20240306")
    # kiwoom.SetInputValue("수정주가구분", "1")
    # kiwoom.CommRqData("myrequest", "opt10081", 0, "0101")
    # tr_data = kiwoom.tr_queue.get()
    # print("==> ", tr_data[0])

    kiwoom.tickChart("005930")

    while True:
        pythoncom.PumpWaitingMessages()
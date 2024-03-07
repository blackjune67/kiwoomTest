from platform import python_compiler
import sys 
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
import pythoncom
from KiwoomLogin import KiwoomLogin

if __name__ == "__main__":
    app = QApplication(sys.argv)

    kiwoom = KiwoomLogin()

    kiwoom.SetInputValue("종목코드", "005930")
    kiwoom.SetInputValue("틱범위", "1:1")
    # CommRqData("RQName", "OPT10001", "0","화면번호");
    kiwoom.CommRqData("opt10001", "opt10001", 0, "0101")

    # KiwoomLogin.SetInputValue("수정주가구분", "1", "")
    # KiwoomLogin.CommRqData( "RQName"	,  "OPT10079"	,  "0"	,  "화면번호")

    #  2. Open API 조회 함수를 호출해서 전문을 서버로 전송합니다.
	# CommRqData( "RQName"	,  "OPT10079"	,  "0"	,  "화면번호")
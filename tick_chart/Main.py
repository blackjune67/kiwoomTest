import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import pandas as pd
from datetime import *
import time
from ItemList import ItemList
import pprint
import asyncio

# 초당 조회 횟수를 회피하기 위한 대기시간 지정
# TIME_TERM = 0.5

class Main(QAxWidget):
    def __init__(self):
        super().__init__()
        self.scrno = '1000'
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.login_event_loop = None
        self.tr_event_loop = None
        self.sPrevNext = None
        self.end_date = None
        self.start_time = None
        self.tr = False
        self.dataframes = []

    def gen_scrno(self):
        self.scrno = str(int(self.scrno) + 1)
        return self.scrno

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, nErrCode):
        # if nErrCode == 0:
            # print('로그인 성공!')
            # print('=' * 50)
        self.login_event_loop.exit()

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        # self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        # self.tr_event_loop = QEventLoop()
        # self.tr_event_loop.exec_()
        future = asyncio.Future()
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
        return future

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()
    
    def _comm_get_big_data(self, sTrCode, sRQName):
        ret = self.dynamicCall(
                "GetCommDataEx(QString, QString)", sTrCode, sRQName)
        return ret
        
    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        # print('TR_Message:', sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
        future = asyncio.Future()
        self.sPrevNext = sPrevNext

        if sRQName == "opt10079_req":
            data = self._opt10080(sRQName, sTrCode)
            future.set_result(data)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def req_tick_chart(self, code):
        # 최초조회
        time.sleep(0.5)
        # self.tr = True
        self.set_input_value("종목코드", code)
        self.set_input_value("틱범위", "1")
        self.set_input_value("수정주가구분", "0")
        self.start_time = time.time()  # 시작 시간 기록
        future = self.comm_rq_data(f'opt10079_req', "opt10079", '0', self.gen_scrno())
        return future

        
    def _opt10080(self, rqname, trcode):
        # 조회된 데이터에서 종목코드를 가져옴 (싱글데이터)
        code = self._comm_get_data(trcode, "", rqname, 0, "종목코드")

        # 전체 데이터 개수 조회
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        # data_cnt = min(self._get_repeat_cnt(trcode, rqname), 100)
        # print('전체 데이터 갯수 : ', data_cnt)
        # print('-' * 50)

        # 조회된 데이터 갯수 만큼 반복해서 데이터를 가져온 후 딕셔너리에 저장 (멀티데이터)
        total_ret = []
        for i in range(data_cnt):
                ret = {key: self._comm_get_data(trcode, "", rqname, i, key) for key in ['현재가', '거래량', '체결시간']}
                total_ret.append(ret)
        return total_ret
                       
        # pprint.pprint(total_ret)

        # 딕셔너리를 DataFrame으로 변환 / 컬럼명 변경 / datetime 컬럼 생성
        # df = pd.DataFrame(total_ret)
        # df.columns = ['현재가', '거래량', '체결시간']
        
        # df['체결시간'] = pd.to_datetime(df['체결시간'], format="%Y%m%d%H%M%S")

        # # 최종 조회일자 : 해당 일자이전 기간이 조회데이터에 포함되면 조회를 멈춤
        # if df['체결시간'].iat[-1] < self.end_date:
        #     df = df[df['체결시간'] >= self.end_date]
        #     self.sPrevNext = None   
       
        # df['code'] = code
        # df = df.reset_index(drop=True)
        # self.dataframes.append(df)
        
        # print(df)
        # self.getTime()  # 데이터 가져오는 데 걸린 시간 출력
        
    # def getTime(self):
    #     end_time = time.time()
    #     elapsed_time = end_time - self.start_time
    #     result = timedelta(seconds=elapsed_time)
    #     print('-' * 50)
    #     print('데이터 조회 시간 : ', result)
    #     print('-' * 50)

    # 데이터 파일로 저장
    # def save_data(self):
    #     combined_df = pd.concat(self.dataframes, ignore_index=True)
    #     combined_df.to_csv('C:/Users/최하준/Documents/all_data.csv', index=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.comm_connect()
    main.end_date = datetime(2024, 3, 11)  # 현재부터 해당 날짜까지 조회

    start_time_total = time.perf_counter()

    code_list = (item.value for item in ItemList)

    # for code in code_list:
    #     main.req_tick_chart(code)
    for code in code_list:
        future = main.req_tick_chart(code)

    # for code in code_list:
    #     future = main.req_tick_chart(code)
    #     future.add_done_callback(lambda future: print(f"Result: {future.result()}"))  # 결과를 처리하는 콜백 함수 추가    

    # async def fetch_all():
    #     await asyncio.gather(*[main.req_tick_chart(code) for code in code_list])
    # asyncio.run(fetch_all())
    
    end_time_total = time.perf_counter()

    elapsed_time_total = end_time_total - start_time_total
    result_total = timedelta(seconds=elapsed_time_total)
    print("전체 데이터 조회 시간 : ", result_total)

    # main.save_data()
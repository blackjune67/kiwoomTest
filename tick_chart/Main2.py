from db.database import Database # 하위.py파일 import 클래스명 or Funtion
from datetime import *
import pandas as pd
import pprint
import time


class Main2:
    def __init__(self):
        self.mysql_data = Database.get_data_from_mysql()
        self.dataframes = []


    def data_to_dataframe(self, data):
        df = pd.DataFrame(data, columns=['code', '이름', '날짜'])
        if not df.empty:
            df['날짜'] = pd.to_datetime(df['날짜'], format="%Y-%m-%d")
            df = df.reset_index(drop=True)
            self.dataframes.append(df)

        pprint.pprint(df)


if __name__ == "__main__":
    main = Main2()

    start_time_total = time.perf_counter()

    main.data_to_dataframe(main.mysql_data)

    end_time_total = time.perf_counter()
    elapsed_time_total = end_time_total - start_time_total
    result_total = timedelta(seconds=elapsed_time_total)
    print('데이터 조회 시간 : ', result_total) 
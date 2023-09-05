import gevent.monkey

gevent.monkey.patch_all()

import json
import pandas as pd
from ssi.data.DataStream import MarketDataStream
from tabulate import tabulate

columns = None
df = None

count_attempts = 0

# ======== Biến số ======== #
MAX_ATTEMPTS = 10  # Số lần lấy dữ liệu trước khi lưu vào file
file_name = "data.xlsx"  # Tên file lưu dữ liệu
channel = "X-TRADE:ALL"  # Kênh lấy dữ liệu (X-TRADE:ALL để lấy tất cả các cổ phiếu, X-TRADE:VN30F2309 để lấy cổ phiếu VN30F2309, tương tự với các mã khác)
# ========================= #


def on_message(message):
    global columns, df, count_attempts, MAX_ATTEMPTS

    message = json.loads(message)
    content = json.loads(message["Content"])
    if content["Exchange"] == "DERIVATIVES":
        count_attempts += 1
        if columns is None:
            columns = content.keys()
            df = pd.DataFrame(columns=columns)

        # add content to data frame
        df.loc[len(df)] = content.values()

        if count_attempts == MAX_ATTEMPTS and MAX_ATTEMPTS != 0:
            df.to_excel(file_name, index=False)
            count_attempts = 0

        # Clear terminal before printing new data
        print("\033[H\033[J")  # ANSI escape codes to clear terminal

        # Print the updated table using tabulate
        print(tabulate(df, headers="keys", tablefmt="fancy_grid"))


if __name__ == "__main__":
    market_data_stream = MarketDataStream(
        on_message=on_message,
        on_error=lambda x: print(x),
    )
    market_data_stream.start(channel)

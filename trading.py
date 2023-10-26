import gevent.monkey

gevent.monkey.patch_all()

import json
import os
import time
from datetime import datetime, timedelta
from decimal import Decimal

import pandas as pd
import questionary
from ssi_fctrading import FCTradingClient

from ssi import config
from ssi.data.DataStream import MarketDataStream
from ssi.trading import fc_der_new_order, fc_get_otp, fc_verity_code

# # Check current GMT, if not GMT+7, then change it to GMT+7
# if datetime.now().strftime("%z") != "+0700":
#     os.environ["TZ"] = "Asia/Ho_Chi_Minh"
#     time.tzset()

# ======== Biến số ======== #
MARKET = "VNFE"  # Thị trường ('VN' hoặc 'VNFE')
ORDER_TYPE = "MTL"  # Loại lệnh (LO, ATO, ATC, MTL, MOK, MAK)
PRICE = 0  # Giá. Với lệnh LO, giá phải lớn hơn 0; với các lệnh khác price = 0
ACCOUNT = "0000000000"  # Tài khoản
STOP_ORDER = False  # Chỉ áp dụng cho thị trường VNFE. True nếu là lệnh điều kiện, False nếu là lệnh thường
STOP_PRICE = 0  # Nếu stopOrder là True, thì stopPrice phải lớn hơn 0
STOP_TYPE = ""  # Nếu stopOrder là True, thì stopType phải là mot trong (D: Down, U: Up, V: Trailing Up, E: Trailing Down, O: OCO)
STOP_STEP = 0  # Nếu stopOrder là True, thì stopStep phải lớn hơn 0
LOSS_STEP = 0  # Nếu stopOrder là True và stopType là B, thì lossStep phải lớn hơn 0
PROFIT_STEP = 0  # Nếu stopOrder là True và stopType là B, thì profitStep phải lớn hơn 0
# ========================= #

# ======== Biến số ======== #
STOCK = "VN30F2311"  # Mã cổ phiếu (ví dụ: VN30F2309)
FILE_NAME = "data_trade.txt"  # Tên file lưu dữ liệu giao dịch
STEP_POINT_BACK = 2  # Số tickers để tính delta
MORNING_DELTA_TICK_POINT = 0.4  # Delta tick point buổi sáng
AFTERNOON_DELTA_TICK_POINT = 0.2  # Delta tick point buổi chiều
USE_CUSTOM_PERIOD = False  # True thì sử dụng khoảng thời gian tùy chỉnh, nếu False thì sẽ chạy chương trình ngay lập tức và chạy trong 15 phút
start_datetime = "2023-09-11 00:00:00"  # Ngày giờ bắt đầu chạy chương trình (định dạng: yyyy-mm-dd hh:mm:ss)
end_datetime = "2023-09-20 23:59:59"  # Ngày giờ kết thúc chạy chương trình (định dạng: yyyy-mm-dd hh:mm:ss)
# ========================= #

# Convert datetime string to datetime object
if not USE_CUSTOM_PERIOD:
    start_datetime = datetime.now()  # current time
    end_datetime = start_datetime + timedelta(minutes=15)  # current time + 15 minutes
else:
    start_datetime = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")

# Initialize global variables
df_transactions = None
df_trades = (
    pd.DataFrame(columns=["stock", "timestamp", "position", "price", "delta"])
    if not os.path.exists(FILE_NAME)
    else pd.read_csv(FILE_NAME, sep=";")
)

market_data_stream = None
trading_client = FCTradingClient(
    config.url_trading,
    config.consumer_id,
    config.consumer_secret,
    config.private_key,
    config.two_fa_type,
)


def main():
    global market_data_stream

    # Check Number of step back is greater than 1
    assert STEP_POINT_BACK > 1, "Number of step back must be greater than 1, please check again"

    # Check if end_datetime is greater than start_datetime
    assert end_datetime > start_datetime, "End datetime must be greater than from datetime, please check again"

    # # Get and verify OTP for authentication
    # get_and_verify_otp()

    # Wait for the time to start
    notified = False
    while datetime.now() < start_datetime:
        if not notified:
            print("Waiting for the time to start...")
            print("Current time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("Start time:", start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
            notified = True
            time.sleep(1)

    # Start the market data stream processing
    print("Starting the market data stream...")
    market_data_stream = MarketDataStream(
        on_message=on_message,
        on_error=print,
    )
    market_data_stream.start(f"X-TRADE:{STOCK}")


def on_message(message):
    # If the current time is greater than the end time, then stop the program
    if datetime.now() > end_datetime:
        print("End time reached, stopping the program...")
        market_data_stream.stop()
        return

    # Parse incoming message and extract content
    message = json.loads(message)
    content = json.loads(message["Content"])

    # Append content to the DataFrame
    append_to_df(content)

    # Calculate and place derivative order
    delta_calculation()


def append_to_df(content: dict):
    global df_transactions

    # Initialize DataFrame if it's not created yet
    if df_transactions is None:
        columns = content.keys()
        df_transactions = pd.DataFrame(columns=columns)

    # Append content as a new row in the DataFrame
    df_transactions.loc[len(df_transactions)] = content.values()

    # Only keep the last num_step_back rows
    df_transactions = df_transactions.tail(STEP_POINT_BACK)


# ========= Xử lý logic ======== #
def delta_calculation():
    """
    Columns:
        RType
        TradingDate
        Time
        Isin
        Symbol
        Ceiling
        Floor
        RefPrice
        AvgPrice
        PriorVal
        LastPrice
        LastVol
        TotalVal
        TotalVol
        MarketId
        Exchange
        TradingSession
        TradingStatus
        Change
        RatioChange
        EstMatchedPrice
        Highest
        Lowest
    """
    try:
        # Giá hiện tại
        last_price = df_transactions.loc[df_transactions.index[-1], "LastPrice"]
        # Giá STEP_POINT_BACK tickers trước
        price_at_step_back = df_transactions.loc[df_transactions.index[-STEP_POINT_BACK], "LastPrice"]
        # Độ chênh lệch giá hiện tại và giá STEP_POINT_BACK tickers trước
        delta = Decimal(last_price - price_at_step_back).quantize(Decimal("0.1"))

        # Nếu là buổi sáng thì delta_tick_point = MORNING_DELTA_TICK_POINT, nếu là buổi chiều thì delta_tick_point = AFTERNOON_DELTA_TICK_POINT
        if datetime.now().hour < 12:
            delta_tick_point = MORNING_DELTA_TICK_POINT
        else:
            delta_tick_point = AFTERNOON_DELTA_TICK_POINT

        # Nếu delta >= delta_tick_point thì đặt lệnh Short, ngược lại đặt lệnh Long
        if delta >= delta_tick_point:
            is_place_order = questionary.confirm(
                f"Delta hiện tại ({delta}) lớn hơn {delta_tick_point}, dự báo uptrend. Bạn có muốn đặt lệnh long không?"
            ).ask()
            if is_place_order:
                place_derivative_order(delta, last_price, "B")  # Đặt lệnh long (buy)
        else:
            is_place_order = questionary.confirm(
                f"Delta hiện tại ({delta}) nhỏ hơn {delta_tick_point}, dự báo downtrend. Bạn có muốn đặt lệnh short không?"
            ).ask()
            if is_place_order:
                place_derivative_order(delta, last_price, "S")  # Đặt lệnh short (sell)

    except (IndexError, KeyError):
        pass


# ============================== #


def place_derivative_order(delta, _price, position):
    # Place the derivative order
    print("Placing derivative order...")
    print(
        f"Datetime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, \
            Stock: {STOCK}, Position: {position}, Price: {_price}, Delta: {delta}"
    )

    # Append to df_trade
    df_trades.loc[len(df_trades)] = [
        STOCK,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        position,
        _price,
        delta,
    ]

    # Save to file
    df_trades.to_csv(
        FILE_NAME,
        index=False,
        sep=";",
        index_label=False,
    )

    # res = fc_der_new_order(
    #     client=client,
    #     instrumentID=stock,
    #     market=market,
    #     buySell=position,
    #     orderType=order_type,
    #     price=price,
    #     quantity=volume,
    #     account=account,
    #     stopOrder=stop_order,
    #     stopPrice=stop_price,
    #     stopType=stop_type,
    #     stopStep=stop_step,
    #     lossStep=loss_step,
    #     profitStep=profit_step,
    # )
    # if res.status == 200:
    #     print("Đặt lệnh thành công")
    #     print(res.message)
    #     data = json.loads(res.data["data"])
    #     df_trade.loc[len(df_trade)] = data.values()
    # else:
    #     print("Đặt lệnh thất bại")
    #     print(res.message)
    #     data = json.loads(res.data["data"])
    #     df_trade.loc[len(df_trade)] = data.values()


def get_and_verify_otp():
    fc_get_otp(trading_client)
    print("Mã OTP đã được gửi đến số điện thoại hoặc email của bạn.")
    otp = input("Nhập mã OTP: ")
    fc_verity_code(trading_client, otp)
    return otp


if __name__ == "__main__":
    main()

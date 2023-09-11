import gevent.monkey

gevent.monkey.patch_all()

import json
import os
import time
from datetime import datetime
from decimal import Decimal

import pandas as pd
from ssi_fctrading import FCTradingClient

from ssi import config
from ssi.data.DataStream import MarketDataStream
from ssi.trading import fc_der_new_order, fc_get_otp, fc_verity_code

# Check current GMT, if not GMT+7, then change it to GMT+7
if datetime.now().strftime("%z") != "+0700":
    os.environ["TZ"] = "Asia/Ho_Chi_Minh"
    time.tzset()

# ======== Biến số ======== #
stock = "VN30F2309"  # Mã cổ phiếu (ví dụ: VN30F2309)
market = "VNFE"  # Thị trường ('VN' hoặc 'VNFE')
order_type = "MTL"  # Loại lệnh (LO, ATO, ATC, MTL, MOK, MAK)
price = 0  # Giá. Với lệnh LO, giá phải lớn hơn 0; với các lệnh khác price = 0
account = "0000000000"  # Tài khoản
stop_order = False  # Chỉ áp dụng cho thị trường VNFE. True nếu là lệnh điều kiện, False nếu là lệnh thường
stop_price = 0  # Nếu stopOrder là True, thì stopPrice phải lớn hơn 0
stop_type = ""  # Nu stopOrder là True, thì stopType phải là mot trong (D: Down, U: Up, V: Trailing Up, E: Trailing Down, O: OCO)
stop_step = 0  # Nếu stopOrder là True, thì stopStep phải lớn hơn 0
loss_step = 0  # Nếu stopOrder là True và stopType là B, thì lossStep phải lớn hơn 0
profit_step = 0  # Nếu stopOrder là True và stopType là B, thì profitStep phải lớn hơn 0
file_name = "data_trade.txt"  # Tên file lưu dữ liệu giao dịch
num_step_back = 5  # Số ngày để tính delta
from_datetime = "2023-09-11 00:00:00"  # Ngày giờ bắt đầu chạy chương trình (định dạng: yyyy-mm-dd hh:mm:ss)
end_datetime = "2023-09-18 23:59:59"  # Ngày giờ kết thúc chạy chương trình (định dạng: yyyy-mm-dd hh:mm:ss)
# ========================= #

# Convert datetime string to datetime object
from_datetime = datetime.strptime(from_datetime, "%Y-%m-%d %H:%M:%S")
end_datetime = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")

# Initialize global variables
df_transactions = None
df_trades = (
    pd.DataFrame(columns=["stock", "timestamp", "position", "price", "delta"])
    if not os.path.exists(file_name)
    else pd.read_csv(file_name, sep=";")
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
    assert num_step_back > 1, "Number of step back must be greater than 1, please check again"

    # Check if end_datetime is greater than from_datetime
    assert end_datetime > from_datetime, "End datetime must be greater than from datetime, please check again"

    # # Get and verify OTP for authentication
    # get_and_verify_otp()

    # Wait for the time to start
    notified = False
    while datetime.now() < from_datetime:
        if not notified:
            print("Waiting for the time to start...")
            print("Current time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("Start time:", from_datetime.strftime("%Y-%m-%d %H:%M:%S"))
            notified = True
        pass

    # Start the market data stream processing
    print("Starting the market data stream...")
    market_data_stream = MarketDataStream(
        on_message=on_message,
        on_error=lambda x: print(x),
    )
    market_data_stream.start(f"X-TRADE:{stock}")


def on_message(message):
    global df_transactions

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

    # Calculate the volume delta
    delta = get_delta()

    # Skip in case not enough transactions to calculate delta
    if delta is None:
        return

    # Print current delta
    print("Current delta:", delta)

    # Place orders based on the calculated delta
    if delta >= 0.5:
        place_derivative_order(delta, content["LastPrice"], "S")  # Place a short order (SELL)
    elif delta <= -0.3:
        place_derivative_order(delta, content["LastPrice"], "B")  # Place a long order (BUY)


def append_to_df(content: dict):
    global df_transactions

    # Initialize DataFrame if it's not created yet
    if df_transactions is None:
        columns = content.keys()
        df_transactions = pd.DataFrame(columns=columns)

    # Append content as a new row in the DataFrame
    df_transactions.loc[len(df_transactions)] = content.values()

    # Only keep the last num_step_back rows
    df_transactions = df_transactions.tail(num_step_back)


# ========= Xử lý logic ======== #
def get_delta():
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
        last_price = df_transactions.loc[df_transactions.index[-1], "LastPrice"]
        price_at_step_back = df_transactions.loc[df_transactions.index[-num_step_back], "LastPrice"]
        return Decimal(last_price - price_at_step_back).quantize(Decimal("0.1"))
    except (IndexError, KeyError):
        return None


# ============================== #


def place_derivative_order(delta, price, position):
    # Place the derivative order
    print("Placing derivative order...")
    print(
        f"Datetime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Stock: {stock}, Position: {position}, Price: {price}, Delta: {delta}"
    )

    # Append to df_trade
    df_trades.loc[len(df_trades)] = [
        stock,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        position,
        price,
        delta,
    ]

    # Save to file
    df_trades.to_csv(
        file_name,
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

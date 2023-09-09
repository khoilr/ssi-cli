import gevent.monkey

gevent.monkey.patch_all()

import json
from datetime import datetime

import pandas as pd
from ssi_fctrading import FCTradingClient
from tabulate import tabulate

from ssi import config
from ssi.data.DataStream import MarketDataStream
from ssi.trading import fc_der_new_order, fc_get_otp, fc_verity_code

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
my_steps = 5  # Số ngày để tính delta
# ========================= #

# Initialize global variables
df = None
df_trade = pd.DataFrame(columns=["stock", "timestamp", "position", "price", "delta"])
count = 0
client = FCTradingClient(
    config.url_trading,
    config.consumer_id,
    config.consumer_secret,
    config.private_key,
    config.two_fa_type,
)


def main():
    # # Get and verify OTP for authentication
    # get_and_verify_otp()

    # Start the market data stream processing
    market_data_stream = MarketDataStream(
        on_message=on_message,
        on_error=lambda x: print(x),
    )
    market_data_stream.start(f"X-TRADE:{stock}")


def on_message(message):
    global df, count

    # Parse incoming message and extract content
    message = json.loads(message)
    content = json.loads(message["Content"])

    # Append content to the DataFrame
    append_to_df(content)

    # Calculate the volume delta
    delta = get_delta()

    # Place orders based on the calculated delta
    if delta > 0.5:
        place_derivative_order(-delta, content["LastPrice"], "B")  # Place a long order
    else:
        place_derivative_order(delta, content["LastPrice"], "S")  # Place a short order

    # Increment attempts counter and save data if needed
    count += 1
    if count == 10:
        count = 0


def append_to_df(content: dict):
    global df

    # Initialize DataFrame if it's not created yet
    if df is None:
        columns = content.keys()
        df = pd.DataFrame(columns=columns)

    # Append content as a new row in the DataFrame
    df.loc[len(df)] = content.values()

    # Clear terminal before printing new data
    print("\033[H\033[J")  # ANSI escape codes to clear terminal

    # Print the updated table using tabulate
    print(tabulate(df, headers="keys", tablefmt="fancy_grid"))


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
        return df["LastPrice"][-1] - df["LastPrice"][-my_steps]
    except (IndexError, KeyError):
        return 0


# ============================== #


def place_derivative_order(delta, price, position):
    # Place the derivative order
    # append to df_trade
    df_trade.loc[len(df_trade)] = [
        stock,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        position,
        price,
        delta,
    ]
    df_trade.to_csv(
        "data_trade.txt",
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
    fc_get_otp(client)
    print("Mã OTP đã được gửi đến số điện thoại hoặc email của bạn.")
    otp = input("Nhập mã OTP: ")
    fc_verity_code(client, otp)
    return otp


if __name__ == "__main__":
    main()

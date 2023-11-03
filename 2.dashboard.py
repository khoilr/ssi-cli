import gevent.monkey

gevent.monkey.patch_all()

import json
import os

import pandas as pd
from tabulate import tabulate

from ssi.data.DataStream import MarketDataStream

# ======== Biến số ======== #
stock = "VN30F2311"  # Mã cổ phiếu (ví dụ: VN30F2309)
# ========================= #

# Initialize global variables
df_transactions = None


def main():
    # Start the market data stream processing
    market_data_stream = MarketDataStream(
        on_message=on_message,
        on_error=print,
    )
    market_data_stream.start(f"X-TRADE:{stock}")


def on_message(message):
    # Parse incoming message and extract content
    message = json.loads(message)
    content = json.loads(message["Content"])

    # Append content to the DataFrame
    append_to_df(content)

    # Display dashboard
    display_dashboard()


def append_to_df(content: dict):
    global df_transactions

    # Initialize DataFrame if it's not created yet
    if df_transactions is None:
        columns = content.keys()
        df_transactions = pd.DataFrame(columns=columns)

    # Append content as a new row in the DataFrame
    df_transactions.loc[len(df_transactions)] = content.values()


def display_dashboard():
    # Clear terminal before printing new data
    os.system("cls" if os.name == "nt" else "clear")

    # Print the updated table using tabulate
    print(tabulate(df_transactions.tail(20), headers="keys", tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()

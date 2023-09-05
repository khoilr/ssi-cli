# This is a property
# of SSI company
from gevent import monkey

monkey.patch_all()

import warnings

warnings.filterwarnings("ignore")


from . import md_client_main, md_stream_main

name = "ssi_fc_data"
version = "2.0.0"


# Trading API Client
def access_token(config):
    """Getting token to access api query"""

    config = config

    try:

        return md_client_main.access_token(config)

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def generate_token(config, clientId: str, privateKey: str):
    """Getting two factor token to access api query"""

    config = config
    clientId = clientId
    privateKey = privateKey

    try:

        return md_client_main.generate_token(config, clientId, privateKey)

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def securities(config, market: str, pageIndex: int, pageSize: int):
    """Place new order"""

    market = market
    pageIndex = pageIndex
    pageSize = pageSize
    config = config

    try:

        return md_client_main.securities(config, market, pageIndex, pageSize)

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def securities_details(config, market: str, symbol: str, pageIndex: int, pageSize: int):
    """Modify existing order"""

    market = market
    symbol = symbol
    pageIndex = pageIndex
    pageSize = pageSize
    config = config

    try:

        return md_client_main.securities_details(
            config,
            market,
            symbol,
            pageIndex,
            pageSize,
        )

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def index_components(config, indexCode: str, pageIndex: int, pageSize: int):
    """Cancel existing order"""

    indexCode = indexCode
    pageIndex = pageIndex
    pageSize = pageSize
    config = config

    try:
        return md_client_main.index_components(config, indexCode, pageIndex, pageSize)
    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def index_list(config, exchange: str, pageIndex: int, pageSize: int):
    """Checking balance of a cash account"""

    exchange = exchange
    pageIndex = pageIndex
    pageSize = pageSize
    config = config

    try:

        return md_client_main.index_list(config, exchange, pageIndex, pageSize)

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def daily_ohlc(
    config,
    symbol: str,
    fromDate: str,
    toDate: str,
    pageIndex: int,
    pageSize: int,
    ascending: bool,
):
    """Checking balance of a derivative account"""

    config = config
    symbol = symbol
    fromDate = fromDate
    toDate = toDate
    pageIndex = pageIndex
    pageSize = pageSize
    ascending = ascending

    try:

        return md_client_main.daily_ohlc(
            config,
            symbol,
            fromDate,
            toDate,
            pageIndex,
            pageSize,
            ascending,
        )

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def intraday_ohlc(
    config,
    symbol: str,
    fromDate: str,
    toDate: str,
    pageIndex: int,
    pageSize: int,
    ascending: bool,
    resolution: int,
):
    """Checking the purchasing power of margin account"""

    config = config
    symbol = symbol
    fromDate = fromDate
    toDate = toDate
    pageIndex = pageIndex
    pageSize = pageSize
    ascending = ascending
    resolution = resolution

    try:

        return md_client_main.intraday_ohlc(
            config,
            symbol,
            fromDate,
            toDate,
            pageIndex,
            pageSize,
            ascending,
            resolution,
        )

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def daily_index(
    config,
    requestId: str,
    indexId: str,
    fromDate: str,
    toDate: str,
    pageIndex: int,
    pageSize: int,
    orderBy: str,
    order: str,
):
    """Checking stock position"""

    config = config
    requestId = requestId
    indexId = indexId
    fromDate = fromDate
    toDate = toDate
    pageIndex = pageIndex
    pageSize = pageSize
    orderBy = orderBy
    order = order

    try:
        return md_client_main.daily_index(
            config,
            requestId,
            indexId,
            fromDate,
            toDate,
            pageIndex,
            pageSize,
            orderBy,
            order,
        )
    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def daily_stock_price(
    config,
    symbol: str,
    fromDate: str,
    toDate: str,
    pageIndex: int,
    pageSize: int,
    market: str,
):
    """Checking derivative position"""

    config = config
    symbol = symbol
    fromDate = fromDate
    toDate = toDate
    pageIndex = pageIndex
    pageSize = pageSize
    market = market

    try:
        return md_client_main.daily_stock_price(
            config,
            symbol,
            fromDate,
            toDate,
            pageIndex,
            pageSize,
            market,
        )
    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


def backtest(config, selectedDate: str, symbol: str):
    """Checking max quantity an account can buy"""

    config = config
    selectedDate = selectedDate
    symbol = symbol

    try:
        return md_client_main.backtest(config, selectedDate, symbol)

    except TypeError as te:
        print("Missing required arguments!")
    except IndexError as ie:
        print(
            "No data received! Please check your request or contact vendor for more information!",
        )
    except ValueError as ve:
        print("Please check your input data type!")


# Streaming part


def Market_Data_Stream(config, on_message, on_error, selected_channel):
    """Live stream trading API data"""
    print("Streaming market data...")
    md_stream_main.data_streaming(config, on_message, on_error, selected_channel)

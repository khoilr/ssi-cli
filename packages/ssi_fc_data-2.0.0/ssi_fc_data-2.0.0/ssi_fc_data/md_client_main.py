# from fc_md_client import MarketDataClient
# from model import constants
# from model import model

from .fc_md_client import MarketDataClient
from .model import constants, model

# def generate_token(config, consumerID: str, consumerSecret: str):

# 	req = model.gen_token

# 	req['consumerID'] = consumerID
# 	req['consumerSecret'] = consumerSecret

# 	client = MarketDataClient(config, constants.NONE)
# 	res = client.generate_token(req, constants.NONE)
# 	return res


def access_token(config):

    req = model.accessToken

    req["consumerID"] = config.consumerID
    req["consumerSecret"] = config.consumerSecret

    client = MarketDataClient(config)
    res = client.access_token(req, constants.NONE)
    return res


def securities(config, market: str, pageIndex: int, pageSize: int):

    req = model.securities

    req["market"] = market
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.securities(constants.NONE, req)
    return res


def securities_details(config, market: str, symbol: str, pageIndex: int, pageSize: int):

    req = model.securities_details

    req["market"] = market
    req["symbol"] = symbol
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.securities_details(constants.NONE, req)
    return res


def index_components(config, indexCode: str, pageIndex: int, pageSize: int):

    req = model.index_components

    req["indexCode"] = indexCode
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.index_components(constants.NONE, req)
    return res


def index_list(config, exchange: str, pageIndex: int, pageSize: int):

    req = model.index_list

    req["exchange"] = exchange
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.index_list(constants.NONE, req)
    return res


def daily_ohlc(
    config,
    symbol: str,
    fromDate: str,
    toDate: str,
    pageIndex: int,
    pageSize: int,
    ascending: bool,
):

    req = model.daily_ohlc

    req["symbol"] = symbol
    req["fromDate"] = fromDate
    req["toDate"] = toDate
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize
    req["ascending"] = ascending

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.daily_ohlc(constants.NONE, req)
    return res


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

    req = model.intraday_ohlc

    req["symbol"] = symbol
    req["fromDate"] = fromDate
    req["toDate"] = toDate
    req["resolution"] = resolution
    req["ascending"] = ascending
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.intraday_ohlc(constants.NONE, req)
    return res


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

    req = model.daily_index

    req["requestId"] = requestId
    req["indexId"] = indexId
    req["fromDate"] = fromDate
    req["toDate"] = toDate
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize
    req["orderBy"] = orderBy
    req["order"] = order

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.daily_index(constants.NONE, req)
    return res


def daily_stock_price(
    config,
    symbol: str,
    fromDate: str,
    toDate: str,
    pageIndex: int,
    pageSize: int,
    market: str,
):

    req = model.daily_stock_price

    req["symbol"] = symbol
    req["fromDate"] = fromDate
    req["toDate"] = toDate
    req["pageIndex"] = pageIndex
    req["pageSize"] = pageSize
    req["market"] = market

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.daily_stock_price(constants.NONE, req)
    return res


def backtest(config, selectedDate: str, symbol: str):

    req = model.backtest

    req["selectedDate"] = selectedDate
    req["symbol"] = symbol

    # client = MarketDataClient(config, constants.OTHER)
    client = MarketDataClient(config)
    res = client.backtest(constants.NONE, req)
    return res

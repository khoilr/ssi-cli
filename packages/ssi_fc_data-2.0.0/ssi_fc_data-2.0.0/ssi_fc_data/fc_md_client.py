import json

import requests

from .model import api, constants

# from model import constants
# from model import api


class MarketDataClient(object):

    # def __init__(self, _config, _type_jwt):
    def __init__(self, _config):

        self._config = _config

        # if _type_jwt == constants.AUTH_TOKEN:
        # 	self._type_jwt = self._config.auth_jwt
        # else:
        # 	self._type_jwt = self._config.access_jwt

        self._type_jwt = self._config.access_jwt

        self._header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self._config.auth_type
            + constants.ONE_WHITE_SPACE
            + self._type_jwt,
        }

    def _make_post_request(self, _url, _req_body=None, _object=None):

        _header = self._header

        _req_body = json.dumps(_req_body)

        _api_url = self._config.url + _url

        _response_obj = requests.post(
            _api_url,
            params=_object,
            headers=_header,
            data=_req_body,
        )

        _response = json.loads(_response_obj.content)

        return _response

    def _make_get_request(self, _url, _req_body=None, _object=None):

        _header = self._header

        _req_body = json.dumps(_req_body)

        _api_url = self._config.url + _url

        _response_obj = requests.get(
            _api_url,
            params=_object,
            headers=_header,
            data=_req_body,
        )

        _response = json.loads(_response_obj.content)

        return _response

    # def generate_token(self, _input_data, _object):
    # 	return self._make_post_request(api.MD_GEN_TOKEN, _req_body = _input_data, _object = _object)

    def access_token(self, _input_data, _object):
        return self._make_post_request(
            api.MD_ACCESS_TOKEN,
            _req_body=_input_data,
            _object=_object,
        )

    def securities(self, _input_data, _object):
        return self._make_get_request(
            api.MD_SECURITIES,
            _req_body=_input_data,
            _object=_object,
        )

    def securities_details(self, _input_data, _object):
        return self._make_get_request(
            api.MD_SECURITIES_DETAILS,
            _req_body=_input_data,
            _object=_object,
        )

    def index_components(self, _input_data, _object):
        return self._make_get_request(
            api.MD_INDEX_COMPONENTS,
            _req_body=_input_data,
            _object=_object,
        )

    def index_list(self, _input_data, _object):
        return self._make_get_request(
            api.MD_INDEX_LIST,
            _req_body=_input_data,
            _object=_object,
        )

    def daily_ohlc(self, _input_data, _object):
        return self._make_get_request(
            api.MD_DAILY_OHLC,
            _req_body=_input_data,
            _object=_object,
        )

    def intraday_ohlc(self, _input_data, _object):
        return self._make_get_request(
            api.MD_INTRADAY_OHLC,
            _req_body=_input_data,
            _object=_object,
        )

    def daily_index(self, _input_data, _object):
        return self._make_get_request(
            api.MD_DAILY_INDEX,
            _req_body=_input_data,
            _object=_object,
        )

    def daily_stock_price(self, _input_data, _object):
        return self._make_get_request(
            api.MD_DAILY_STOCK_PRICE,
            _req_body=_input_data,
            _object=_object,
        )

    def backtest(self, _input_data, _object):
        return self._make_get_request(
            api.MD_BACKTEST,
            _req_body=_input_data,
            _object=_object,
        )

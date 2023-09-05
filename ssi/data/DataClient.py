from datetime import datetime, timedelta
from pprint import pprint
from typing import Union

from ssi.data import SSI, constants


class DataClient(SSI):
    def __init__(self, config_file_path: Union[str, None] = None):
        super().__init__(config_file_path)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.config.auth_type} {self.config.access_jwt}",
        }

    def this_request(
        self,
        url: str,
        method: str,
        body=None,
        params=None,
    ):
        return super().request(
            url=url,
            method=method,
            body=body,
            params=params,
            headers=self.headers,
        )

    def stocks(self, market: str, page_index: int, page_size: int):
        """
        Get stocks data from SSI

        Args:
            market (str): HOSE, HNX, UPCOM
            page_index (int): index of page
            page_size (int): size of page

        Returns:
            dict: response from SSI
        """
        params = {
            "market": market,
            "pageIndex": page_index,
            "pageSize": page_size,
        }

        return self.this_request(
            url=constants.STOCKS,
            method="get",
            params=params,
        )

    # def securities_details(self, _input_data, _object):
    #     return self._get(const.MD_SECURITIES_DETAILS, body=_input_data, params=_object)

    # def index_components(self, _input_data, _object):
    #     return self._get(const.MD_INDEX_COMPONENTS, body=_input_data, params=_object)

    # def index_list(self, _input_data, _object):
    #     return self._get(const.MD_INDEX_LIST, body=_input_data, params=_object)

    def daily_ohlc(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        ascending: bool = True,
    ) -> Union[dict, None]:
        """
        Get daily OHLC data from SSI

        Args:
            symbol (str): symbol of stock
            from_date (str): from date in format dd/mm/yyyy
            to_date (str): to date in format dd/mm/yyyy
            ascending (bool, optional): sort by ascending. Defaults to True.

        Returns:
            _type_: _description_
        """

        # convert from_date to_date to datetime object
        from_date_datetime = datetime.strptime(from_date, "%d/%m/%Y")
        to_date_datetime = datetime.strptime(to_date, "%d/%m/%Y")

        # break down from_date_datetime and to_date_datetime into smaller chunks in 30 days
        response = None
        while from_date_datetime < to_date_datetime:
            # Get min to_date_datetime
            current_to_date_datetime = min(
                from_date_datetime + timedelta(days=30),
                to_date_datetime,
            )

            # Call API
            params = {
                "symbol": symbol,
                "fromDate": from_date_datetime.strftime("%d/%m/%Y"),
                "toDate": current_to_date_datetime.strftime("%d/%m/%Y"),
                "pageIndex": 1,
                "pageSize": 100,
                "ascending": ascending,
            }
            current_response = self.this_request(
                constants.MD_DAILY_OHLC,
                method="get",
                params=params,
            )

            # Merge response
            if response is None:
                response = current_response
            else:
                response["data"] += current_response["data"]
                response["totalRecord"] += current_response["totalRecord"]

            # Update from_date_datetime
            from_date_datetime = current_to_date_datetime + timedelta(days=1)

        # Return response
        return response

    def intraday_ohlc(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        page_index: int,
        page_size: int,
        ascending: bool = True,
    ):
        """
        Get intraday OHLC data from SSI

        Args:
            symbol (str): symbol of stock
            from_date (str): from date in format dd/mm/yyyy
            to_date (str): to date in format dd/mm/yyyy
            page_index (int): index of page
            page_size (int): size of page
            ascending (bool): sort by ascending. Defaults to True.

        Returns:
            dict: response from SSI
        """
        # convert from_date to_date to datetime object
        from_date_datetime = datetime.strptime(from_date, "%d/%m/%Y")
        to_date_datetime = datetime.strptime(to_date, "%d/%m/%Y")

        # break down from_date_datetime and to_date_datetime into smaller chunks in 30 days
        response = None
        while from_date_datetime < to_date_datetime:
            # Get min to_date_datetime
            current_to_date_datetime = min(
                from_date_datetime + timedelta(days=30),
                to_date_datetime,
            )

            # Call API
            params = {
                "symbol": symbol,
                "fromDate": from_date_datetime.strftime("%d/%m/%Y"),
                "toDate": current_to_date_datetime.strftime("%d/%m/%Y"),
                "pageIndex": 1,
                "pageSize": 9999,
                "ascending": ascending,
            }
            current_response = self.this_request(
                constants.MD_INTRADAY_OHLC,
                method="get",
                params=params,
            )

            # Merge response
            if response is None or response['data'] is None:
                response = current_response
            else:
                response["data"] += current_response["data"]
                response["totalRecord"] += current_response["totalRecord"]

            # Update from_date_datetime
            from_date_datetime = current_to_date_datetime + timedelta(days=1)

        # Return response
        return response

    # def daily_index(self, _input_data, _object):
    #     return self._get(const.MD_DAILY_INDEX, body=_input_data, params=_object)

    # def daily_stock_price(self, _input_data, _object):
    #     return self._get(const.MD_DAILY_STOCK_PRICE, body=_input_data, params=_object)

    # def backtest(self, _input_data, _object):
    #     return self._get(const.MD_BACKTEST, body=_input_data, params=_object)


if __name__ == "__main__":
    market_data_client = DataClient()
    data = market_data_client.intraday_ohlc(
        symbol="fpt",
        from_date="01/01/2021",
        to_date="31/3/2023",
        page_index=1,
        page_size=100,
    )
    if data is not None:
        pprint(data)
        print(data["totalRecord"])

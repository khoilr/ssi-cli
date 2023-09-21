import json
from datetime import datetime
from typing import Union

import requests
from ssi import config

from ssi.data import constants


class SSI(object):
    def __init__(self, config_file_path: Union[str, None] = None) -> None:
        if config_file_path is None:
            self.config_file_path = "ssi/data/config.py"

        self.config = config
        self.headers = {
            "Authorization": f"{self.config.auth_type} {self.config.access_jwt}",
        }

        self.refresh_token(config_file_path)

    def _get(
        self,
        url: str,
        body=None,
        params=None,
        headers=None,
    ) -> dict:
        res = requests.get(
            self.config.url_data + url,
            params=params,
            headers=headers,
            data=body,
        )
        return json.loads(res.content)

    def _post(
        self,
        url: str,
        body=None,
        params=None,
        headers=None,
    ) -> dict:
        res = requests.post(
            self.config.url_data + url,
            params=params,
            headers=headers,
            data=body,
        )
        return json.loads(res.content)

    def request(
        self,
        url: str,
        method: str,
        body=None,
        params=None,
        headers=None,
    ) -> dict:
        body = json.dumps(body)

        if headers is None:
            headers = self.headers

        if method.upper() == "POST":
            return self._post(url, body, params, headers)
        elif method.upper() == "GET":
            return self._get(url, body, params, headers)
        else:
            return {"error": "Invalid method"}

    def get_token(self):
        body = {
            "consumerID": self.config.consumer_id,
            "consumerSecret": self.config.consumer_secret,
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.config.auth_type} {self.config.access_jwt}",
        }
        return self.request(
            url=constants.ACCESS_TOKEN,
            method="post",
            body=body,
            headers=headers,
        )

    def refresh_token(self, config_file_path: Union[str, None] = None):
        """
        Get new JWT token, reassigned to config and write to file

        Args:
            file_path (str): file to write new config to

        Raises:
            Exception:
        """
        token = self.get_token()["data"]["accessToken"]
        if token is not None:
            # Set the access token in the config
            self.config.access_jwt = token

            if config_file_path is None:
                config_file_path = self.config_file_path

            # Write the config to file
            with open(config_file_path, "w") as f:
                [
                    f.write(f'{key} = "{value}"\n')
                    for key, value in self.config.__dict__.items()
                    if not key.startswith("__")
                ]
                # if not key.startswith("__"):
                #     f.write(f'{key} = "{value}"\n')

            print("Access token set successfully", datetime.now())
        else:
            raise Exception("Failed to get access token", datetime.now())

    # selected_channel = "B:ALL"
    # market_data_stream = MarketDataStream(on_message=lambda x: print(json.loads(x)), on_error=lambda x: print(x))
    # market_data_stream.start(selected_channel)

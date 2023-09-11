import json
import time
from pprint import pprint
from typing import Callable, Union

import signalr
from requests import Session

from ssi.data import SSI


class MarketDataStream(SSI):
    def __init__(
        self,
        on_message: Callable,
        on_error: Callable,
        config_file_path: Union[str, None] = None,
    ):
        super().__init__(config_file_path)

        self.on_message = on_message
        self.on_error = on_error
        self.headers = {
            "Authorization": f"{self.config.auth_type} {self.config.access_jwt}",
        }

        self.connection = None  # Initialize the connection attribute

    def start(self, channel: str):
        with Session() as session:
            session.headers.update(self.headers)

            self.connection = signalr.Connection(
                # url=f"{self.config.stream_url}v2.0/signalr",
                url=f"https://fc-data.ssi.com.vn/v2.0/signalr",
                session=session,
            )
            hub = self.connection.register_hub("FcMarketDataV2Hub")

            hub.client.on("Broadcast", handler=self.on_message)
            hub.client.on("Error", handler=self.on_error)

            self.connection.start()
            hub.server.invoke("SwitchChannels", channel)

            while True:
                try:
                    self.connection.wait()
                except:
                    print("Connection lost: Try to reconnect to server!")
                    time.sleep(5)

    def stop(self):
        if self.connection:
            self.connection.close()


def on_message(message):
    message = json.loads(message)
    content = json.loads(message["Content"])
    pprint(content)


if __name__ == "__main__":
    selected_channel = "X-TRADE:VN30F2309"
    market_data_stream = MarketDataStream(
        on_message=on_message,
        on_error=lambda x: print(x),
    )
    market_data_stream.start(selected_channel)

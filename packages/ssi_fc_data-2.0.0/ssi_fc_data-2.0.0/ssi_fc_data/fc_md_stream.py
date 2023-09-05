import json
import time

from requests import Session

from .model import api, constants
from .signalr import Connection


class MarketDataStream(object):
    def __init__(self, _config):

        self._config = _config
        self._handlers = []
        self._error_handlers = []

    def _on_message(self, _message):

        _message = json.loads(_message)

        try:

            for _handler in self._handlers:

                _handler(_message)

        except:

            raise Exception(constants.RECEIVE_ERROR_MESSAGE)

    def _on_error(self, _error):

        _error = _error

        for _error_handler in self._error_handlers:

            _error_handler(_error)

    def start(self, _on_message, _on_error, _selected_channel, *argv):

        self._handlers.append(_on_message)

        self._error_handlers.append(_on_error)

        with Session() as session:

            using_jwt = self._config.access_jwt

            session.headers["Authorization"] = (
                self._config.auth_type + constants.ONE_WHITE_SPACE + using_jwt
            )

            connection = Connection(self._config.stream_url + api.SIGNALR, session)

            chat = connection.register_hub(api.SIGNALR_HUB_MD)

            chat.client.on(api.SIGNALR_METHOD, self._on_message)

            chat.client.on(api.SIGNALR_ERROR_METHOD, self._on_error)

            connection.error += _on_error

            with connection:

                chat.server.invoke("SwitchChannels", _selected_channel)

                while True:

                    if connection.is_reset_connection:

                        print(constants.CONNECTION_LOST_ERROR_MESSAGE)

                        connection.reset_session(session)
                        connection.start()

                        chat.server.invoke("SwitchChannels", _selected_channel)

                        time.sleep(6)

                        connection.is_reset_connection = False

                    else:

                        time.sleep(9)

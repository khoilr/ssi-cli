import json
import time

import gevent
from signalr.events import EventHook
from signalr.hubs import Hub
from signalr.transports import AutoTransport


class Connection:
    protocol_version = "1.5"

    def __init__(self, url, session):
        self.url = url
        self.__hubs = {}
        self.qs = {}
        self.__send_counter = -1
        self.token = None
        self.data = None
        self.received = EventHook()
        self.error = EventHook()
        self.starting = EventHook()
        self.stopping = EventHook()
        self.__transport = AutoTransport(session, self)
        self.__greenlet = None
        self.started = False
        self.is_reset_connection = False

        def handle_error(**kwargs):
            error = kwargs["E"] if "E" in kwargs else None
            if error is None:
                return

            self.error.fire(error)

        self.received += handle_error

        self.starting += self.__set_data

    def __set_data(self):
        self.data = json.dumps([{"name": hub_name} for hub_name in self.__hubs])

    def increment_send_counter(self):
        self.__send_counter += 1
        return self.__send_counter

    def reset_session(self, new_session):
        self.__transport = AutoTransport(new_session, self)

    def start(self):
        self.starting.fire()

        negotiate_data = self.__transport.negotiate()
        self.token = negotiate_data["ConnectionToken"]

        listener = self.__transport.start()

        def wrapped_listener(i=0):
            try:
                listener()
                gevent.sleep()
                self.is_reset_connection = False
            except Exception as e:
                if "10054" in str(e):
                    # traceback.print_exc()
                    print(
                        "Exception: ",
                        e,
                        "will cause connection break => try to reconnect",
                    )
                    print("This process can make application lose some data and time")
                    time.sleep(1)
                    if i < 5:
                        wrapped_listener(i + 1)
                    else:
                        print(e)
                        self.is_reset_connection = True
                        # raise OSError('Error:10054,WSAECONNRESET => Retry to reconnect excess the maximum number')
                else:
                    print(e)
                    self.is_reset_connection = True

        self.__greenlet = gevent.spawn(wrapped_listener)
        self.started = True

    def wait(self, timeout=30):
        # self.__greenlet.join()
        gevent.joinall([self.__greenlet], timeout)

    def send(self, data):
        self.__transport.send(data)

    def close(self):
        gevent.kill(self.__greenlet)
        # self.__greenlet._stop()
        self.__transport.close()

    def register_hub(self, name):
        if name not in self.__hubs:
            if self.started:
                raise RuntimeError(
                    "Cannot create new hub because connection is already started.",
                )

            self.__hubs[name] = Hub(name, self)
        return self.__hubs[name]

    def hub(self, name):
        return self.__hubs[name]

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

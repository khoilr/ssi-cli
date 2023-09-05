# from fc_md_stream import MarketDataStream

from .fc_md_stream import MarketDataStream


def data_streaming(config, _on_message, _on_error, _selected_channel):
    stream = MarketDataStream(config)
    stream.start(_on_message, _on_error, _selected_channel)


# main function
if __name__ == "__main__":
    from gevent import monkey

    monkey.patch_all()
    main()

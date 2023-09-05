from gevent import monkey

monkey.patch_socket()
monkey.patch_ssl()


__version__ = "0.0.7"

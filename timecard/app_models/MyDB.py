# -*- coding: utf-8 -*-

__author__ = 'DZmitriy Marozau'

from humbledb import Mongo


class MyDB(Mongo):
    # config_host = 'dm-morozov'
    # config_host = 'dmorozov'

    config_host = 'localhost'  # On Ubuntu 14
    config_port = 27017




# -*- coding: utf-8 -*-
from flask import Flask
from DelogX import config
from DelogX.api import DelogXAPI

app = Flask(__name__)
api = DelogXAPI(config.site_info)

from DelogX import route
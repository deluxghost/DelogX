#!/usr/bin/env python
# -*- coding: utf-8 -*-
from DelogX import app
from DelogX.config import DelogXConfig as config

app.run(host=config.app_info['HOST'], port=config.app_info['PORT'])

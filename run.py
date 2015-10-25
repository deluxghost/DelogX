#!/usr/bin/env python
# -*- coding: utf-8 -*-
from DelogX import app
from DelogX import config

app.run(host=config.app_info['HOST'], port=config.app_info['PORT'])

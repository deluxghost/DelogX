# -*- coding: utf-8 -*-
from watchdog.events import PatternMatchingEventHandler

class BlogHandler(PatternMatchingEventHandler):

    def on_any_event(self, event):
        from DelogX import api
        api.update_list()

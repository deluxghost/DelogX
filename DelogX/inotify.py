# -*- coding: utf-8 -*-
import pyinotify

class FileEventHandler(pyinotify.ProcessEvent):
    
    def process_default(self, event):
        from DelogX import api
        mask = pyinotify.IN_MODIFY | pyinotify.IN_ATTRIB \
            | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_FROM \
            | pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE \
            | pyinotify.IN_DELETE | pyinotify.IN_DELETE_SELF \
            | pyinotify.IN_MOVE_SELF
        if event.mask & mask:
            api.update_list()
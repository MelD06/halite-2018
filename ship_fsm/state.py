#!/usr/bin/env python3
# Python 3.6
""" Defining basic state machine structure """
import logging 


class State():

    def __init__(self):
        logging.info('incoming state:' + str(self))

    def on_event(self, event):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

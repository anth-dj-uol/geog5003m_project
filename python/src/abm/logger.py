#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging module

Provides classes used for logging.

@author: Anthony Jarrett
"""

from datetime import datetime

_enabled = False

def log(message, *args):
    if _enabled:
        print("{} - {}".format(datetime.now().isoformat(), message.format(*args)))

def configure(enabled=False):
    global _enabled
    _enabled = enabled
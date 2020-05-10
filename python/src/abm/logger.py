#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging module

Provides classes used for logging.

@author: Anthony Jarrett
"""

from datetime import datetime

def log(message, *args):
    print("{} - {}".format(datetime.now().isoformat(), message.format(*args)))

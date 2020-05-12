#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging module

Provides utility functions for logging text output.

@author: Anthony Jarrett
"""

from datetime import datetime


_enabled = False    # Track the logging enabled flag

def log(message, *args):

    # Check if logging is enabled
    if _enabled:

        # Print the log message with any provided format arguments
        print("{} - {}".format(datetime.now().isoformat(), message.format(*args)))

def configure(enabled=False):

    # Set the logging enabled flag
    global _enabled
    _enabled = enabled
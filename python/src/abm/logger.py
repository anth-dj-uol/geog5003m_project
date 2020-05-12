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
    """
    Log a message.
    
    If logging is enabled, the message will be printed to standard output.

    Parameters
    ----------
    message : str
        Log message.
    *args : any
        Optional string format parameters.

    Returns
    -------
    None.

    """

    # Check if logging is enabled
    if _enabled:

        # Print the log message with any provided format arguments
        print("{} - {}".format(datetime.now().isoformat(), message.format(*args)))


def configure(enabled=False):
    """
    Configure the logger utility.

    Parameters
    ----------
    enabled : bool, optional
        True if logging should be enabled. The default is False.

    Returns
    -------
    None.

    """
    # Set the logging enabled flag
    global _enabled
    _enabled = enabled
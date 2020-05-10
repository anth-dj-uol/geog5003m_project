#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bacterial Bomb Agent-Based Model

A project for the University of Leeds GEOG5003M course.

@author: Anthony Jarrett
"""

from datetime import datetime
from abm import model

def log(message):
    print("{} - {}".format(datetime.now().isoformat(), message))

def main():
    log("Starting Bacterial Bomb Agent-Based Model...")

    model.Model()

# Run the main function when invoked as a script
if __name__ == '__main__':
    main()
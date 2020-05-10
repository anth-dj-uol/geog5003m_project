#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bacterial Bomb Agent-Based Model

A project for the University of Leeds GEOG5003M course.

@author: Anthony Jarrett
"""

from abm import model, logger

def main():
    logger.log("Starting Bacterial Bomb Agent-Based Model...")

    # Create initial model
    initial_model = model.Model()
    logger.log("Created initial model:\n{}", initial_model)


# Run the main function when invoked as a script
if __name__ == '__main__':
    main()
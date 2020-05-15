#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Position unit tests

@author: Anthony Jarrett
"""

import unittest

from python.src.simulation import particleframework

class PositionTestCase(unittest.TestCase):

    def test_init(self):

        # Initialize position parameters
        x_pos = 1
        y_pos = 2

        # Create position
        position = particleframework.Position(x_pos, y_pos)

        # Verfiy position coordinates
        self.assertIsNotNone(position)
        self.assertEqual(position.x, x_pos)
        self.assertEqual(position.y, y_pos)


    def test_create_from(self):

        # Initialize position parameters
        x_pos = 3
        y_pos = 4

        # Create position
        position_a = particleframework.Position(x_pos, y_pos)
        position_b = particleframework.Position.create_from(position_a)

        # Verfiy position coordinates
        self.assertIsNotNone(position_a)
        self.assertEqual(position_a.x, x_pos)
        self.assertEqual(position_a.y, y_pos)
        self.assertEqual(position_a.x, position_b.x)
        self.assertEqual(position_a.y, position_b.y)

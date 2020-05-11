#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BombEnvironment unit tests

@author: Anthony Jarrett
"""

import unittest

from python.src.abm import agentframework

class BombEnvironmentTestCase(unittest.TestCase):

    def test_init(self):

        # Initialize parameters
        plane = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        bomb_position = agentframework.Position(1, 1)

        # Create the environment
        environment = agentframework.BombEnvironment(plane, bomb_position)

        # Verify the resulting environment
        self.assertIsNotNone(environment)
        self.assertEqual(environment.plane, plane)
        self.assertEqual(environment.width, 3)
        self.assertEqual(environment.height, 2)
        self.assertTrue(environment.bomb_position.equals(bomb_position))

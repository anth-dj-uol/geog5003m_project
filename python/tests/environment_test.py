#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Environment unit tests

@author: Anthony Jarrett
"""

import unittest

from python.src.abm import agentframework

class EnvironmentTestCase(unittest.TestCase):

    def test_init(self):

        # Initialize parameters
        plane = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        # Create the environment
        environment = agentframework.Environment(plane)

        # Verify the resulting environment
        self.assertIsNotNone(environment)
        self.assertEqual(environment.plane, plane)
        self.assertEqual(environment.width, 3)
        self.assertEqual(environment.height, 2)

    def test_invalid(self):

        # Initialize invalid plane
        plane = [1, 2, 3]

        try:
            # Create the environment
            environment = agentframework.Environment(plane)
            self.fail()
        except Exception as e:
            self.assertIsNotNone(e)


    def test_contains_positive(self):

        # Initialize plane
        plane = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        # Create the environment
        environment = agentframework.Environment(plane)

        # Verify the contains query
        self.assertTrue(environment.contains(agentframework.Position(1,1)))


    def test_contains_negative(self):

        # Initialize plane
        plane = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        # Create the environment
        environment = agentframework.Environment(plane)
        
        # Verify the contains query
        self.assertFalse(environment.contains(agentframework.Position(10,1)))

    def test_create_from_size(self):

        # Initialize parameters
        width = 50
        height = 80
        initial_value = 42

        # Create the environment
        environment = agentframework.Environment.create_from_size(width, height, initial_value)

        # Verify the resulting environment
        self.assertIsNotNone(environment)
        self.assertEqual(environment.width, width)
        self.assertEqual(environment.height, height)
        self.assertEqual(environment.plane[0][0], initial_value)
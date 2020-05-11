#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wind Settings unit tests

@author: Anthony Jarrett
"""

import unittest

from python.src.abm import agentframework

class WindSettingsTestCase(unittest.TestCase):

    def test_init(self):

        # Initialize parameters
        north_percentage = 5
        east_percentage = 10
        south_percentage = 20
        west_percentage = 65

        # Create wind settings
        wind_settings = agentframework.WindSettings(
            north_percentage,
            east_percentage,
            south_percentage,
            west_percentage
        )

        # Verify the wind settings
        self.assertIsNotNone(wind_settings)
        self.assertEqual(wind_settings.north_percentage, north_percentage)
        self.assertEqual(wind_settings.east_percentage, east_percentage)
        self.assertEqual(wind_settings.south_percentage, south_percentage)
        self.assertEqual(wind_settings.west_percentage, west_percentage)

    def test_sum_too_large(self):

        # Initialize parameters
        north_percentage = 5
        east_percentage = 10
        south_percentage = 20
        west_percentage = 75

        try:
            # Create wind settings
            agentframework.WindSettings(
                north_percentage,
                east_percentage,
                south_percentage,
                west_percentage
            )
            self.fail()
        except Exception as e:
            self.assertIsNotNone(e)

    def test_sum_too_small(self):

        # Initialize parameters
        north_percentage = 5
        east_percentage = 10
        south_percentage = 20
        west_percentage = 15

        try:
            # Create pwind settings
            agentframework.WindSettings(
                north_percentage,
                east_percentage,
                south_percentage,
                west_percentage
            )
            self.fail()
        except Exception as e:
            self.assertIsNotNone(e)

    def test_get_next_north(self):

        # Initialize parameters
        north_percentage = 100
        east_percentage = 0
        south_percentage = 0
        west_percentage = 0

        # Create wind settings
        wind_settings = agentframework.WindSettings(
            north_percentage,
            east_percentage,
            south_percentage,
            west_percentage
        )

        # Verify the next direction
        next_direction = wind_settings.get_next()
        self.assertEqual(next_direction, agentframework.Direction.NORTH)

    def test_get_next_east(self):

        # Initialize parameters
        north_percentage = 0
        east_percentage = 100
        south_percentage = 0
        west_percentage = 0

        # Create wind settings
        wind_settings = agentframework.WindSettings(
            north_percentage,
            east_percentage,
            south_percentage,
            west_percentage
        )

        # Verify the next direction
        next_direction = wind_settings.get_next()
        self.assertEqual(next_direction, agentframework.Direction.EAST)

    def test_get_next_south(self):

        # Initialize parameters
        north_percentage = 0
        east_percentage = 0
        south_percentage = 100
        west_percentage = 0

        # Create wind settings
        wind_settings = agentframework.WindSettings(
            north_percentage,
            east_percentage,
            south_percentage,
            west_percentage
        )

        # Verify the next direction
        next_direction = wind_settings.get_next()
        self.assertEqual(next_direction, agentframework.Direction.SOUTH)

    def test_get_next_west(self):

        # Initialize parameters
        north_percentage = 0
        east_percentage = 0
        south_percentage = 0
        west_percentage = 100

        # Create wind settings
        wind_settings = agentframework.WindSettings(
            north_percentage,
            east_percentage,
            south_percentage,
            west_percentage
        )

        # Verify the next direction
        next_direction = wind_settings.get_next()
        self.assertEqual(next_direction, agentframework.Direction.WEST)


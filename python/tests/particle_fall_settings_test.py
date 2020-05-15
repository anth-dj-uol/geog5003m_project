#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Particle Fall Settings unit tests

@author: Anthony Jarrett
"""

import unittest

from python.src.simulation import particleframework

class ParticleFallSettingsTestCase(unittest.TestCase):

    def test_init(self):

        # Initialize parameters
        up_percentage = 10
        down_percentage = 20
        no_change_percentage = 70

        # Create particle fall settings
        particle_fall_settings = particleframework.ParticleFallSettings(
            up_percentage,
            down_percentage,
            no_change_percentage
        )

        # Verify the particle fall settings
        self.assertIsNotNone(particle_fall_settings)
        self.assertEqual(particle_fall_settings.up_percentage, up_percentage)
        self.assertEqual(particle_fall_settings.down_percentage, down_percentage)
        self.assertEqual(particle_fall_settings.no_change_percentage, no_change_percentage)

    def test_sum_too_large(self):

        # Initialize parameters
        up_percentage = 10
        down_percentage = 20
        no_change_percentage = 80

        # Create particle fall settings
        try:
            particle_fall_settings = particleframework.ParticleFallSettings(
                up_percentage,
                down_percentage,
                no_change_percentage
            )
            self.fail()
        except Exception as e:
            self.assertIsNotNone(e)

    def test_sum_too_small(self):

        # Initialize parameters
        up_percentage = 10
        down_percentage = 20
        no_change_percentage = 10

        # Create particle fall settings
        try:
            particle_fall_settings = particleframework.ParticleFallSettings(
                up_percentage,
                down_percentage,
                no_change_percentage
            )
            self.fail()
        except Exception as e:
            self.assertIsNotNone(e)

    def test_get_next_up(self):

        # Initialize parameters
        up_percentage = 100
        down_percentage = 0
        no_change_percentage = 0

        # Create particle fall settings
        particle_fall_settings = particleframework.ParticleFallSettings(
            up_percentage,
            down_percentage,
            no_change_percentage
        )

        # Verify the next direction
        next_fall = particle_fall_settings.get_next()
        self.assertEqual(next_fall, particleframework.Fall.UP)

    def test_get_next_down(self):

        # Initialize parameters
        up_percentage = 0
        down_percentage = 100
        no_change_percentage = 0

        # Create particle fall settings
        particle_fall_settings = particleframework.ParticleFallSettings(
            up_percentage,
            down_percentage,
            no_change_percentage
        )

        # Verify the next direction
        next_fall = particle_fall_settings.get_next()
        self.assertEqual(next_fall, particleframework.Fall.DOWN)

    def test_get_next_no_change(self):

        # Initialize parameters
        up_percentage = 0
        down_percentage = 0
        no_change_percentage = 100

        # Create particle fall settings
        particle_fall_settings = particleframework.ParticleFallSettings(
            up_percentage,
            down_percentage,
            no_change_percentage
        )

        # Verify the next direction
        next_fall = particle_fall_settings.get_next()
        self.assertEqual(next_fall, particleframework.Fall.NONE)

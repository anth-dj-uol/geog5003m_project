#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Particle unit tests

@author: Anthony Jarrett
"""

import unittest

from python.src.simulation import particleframework

# Initialize test parameters
TEST_PARTICLE_FALL_SETTINGS = particleframework.ParticleFallSettings()
TEST_WIND_SETTINGS = particleframework.WindSettings()
TEST_POSITION = particleframework.Position(1, 2)
TEST_BUILDING_HEIGHT = 12

class ParticleTestCase(unittest.TestCase):

    def test_init(self):

        # Create test particle
        particle = ParticleTestCase.create_particle()

        # Verify particle state
        self.assertIsNotNone(particle)
        self.assertTrue(particle._particle_fall_settings.equals(TEST_PARTICLE_FALL_SETTINGS))
        self.assertTrue(particle._wind_settings.equals(TEST_WIND_SETTINGS))
        self.assertTrue(particle.position.equals(TEST_POSITION))
        self.assertEqual(particle._building_height, TEST_BUILDING_HEIGHT)

    def test_move(self):

        # Create test particle
        particle = ParticleTestCase.create_particle()

        # Move the particle
        particle.move()
        
        # Verify particle movement
        self.assertFalse(particle.position.equals(TEST_POSITION))


    def test_fall(self):

        # Create particle fall settings to force downward wind
        particle_fall_settings = particleframework.ParticleFallSettings(0, 100, 0)

        # Initialize building height
        building_height = 10

        # Create test particle
        particle = ParticleTestCase.create_particle(
            particle_fall_settings=particle_fall_settings,
            building_height=building_height
        )

        # Move the particle
        particle.fall()
        
        # Verify particle movement
        self.assertEqual(particle._height, building_height-1)

    def test_fall_on_ground(self):

        # Create particle fall settings to force downward wind
        particle_fall_settings = particleframework.ParticleFallSettings(0, 100, 0)

        # Initialize building height
        building_height = 0

        # Create test particle
        particle = ParticleTestCase.create_particle(
            particle_fall_settings=particle_fall_settings,
            building_height=building_height
        )

        self.assertFalse(particle.can_fall())

        # Attempt to move the particle
        particle.fall()
        
        # Verify no particle movement
        self.assertEqual(particle._height, building_height)


    @staticmethod
    def create_particle(
        particle_fall_settings=None,
        wind_settings=None,
        position=None,
        building_height=None
    ):
        # Create particle
        return particleframework.Particle(
            TEST_PARTICLE_FALL_SETTINGS if particle_fall_settings is None else particle_fall_settings,
            TEST_WIND_SETTINGS if wind_settings is None else wind_settings,
            TEST_POSITION if position is None else position,
            TEST_BUILDING_HEIGHT if building_height is None else building_height,
            
        )
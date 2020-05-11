#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent unit tests

@author: Anthony Jarrett
"""

import unittest

from python.src.abm import agentframework

# Initialize test parameters
TEST_PARTICLE_FALL_SETTINGS = agentframework.ParticleFallSettings()
TEST_WIND_SETTINGS = agentframework.WindSettings()
TEST_POSITION = agentframework.Position(1, 2)
TEST_BUILDING_HEIGHT = 12

class AgentTestCase(unittest.TestCase):

    def test_init(self):

        # Create test agent
        agent = AgentTestCase.create_agent()

        # Verify agent state
        self.assertIsNotNone(agent)
        self.assertTrue(agent._particle_fall_settings.equals(TEST_PARTICLE_FALL_SETTINGS))
        self.assertTrue(agent._wind_settings.equals(TEST_WIND_SETTINGS))
        self.assertTrue(agent.position.equals(TEST_POSITION))
        self.assertEqual(agent._building_height, TEST_BUILDING_HEIGHT)

    def test_move(self):

        # Create test agent
        agent = AgentTestCase.create_agent()

        # Move the agent
        agent.move()
        
        # Verify agent movement
        self.assertFalse(agent.position.equals(TEST_POSITION))


    def test_fall(self):

        # Create particle fall settings to force downward wind
        particle_fall_settings = agentframework.ParticleFallSettings(0, 100, 0)

        # Initialize building height
        building_height = 10

        # Create test agent
        agent = AgentTestCase.create_agent(
            particle_fall_settings=particle_fall_settings,
            building_height=building_height
        )

        # Move the agent
        agent.fall()
        
        # Verify agent movement
        self.assertEqual(agent._height, building_height-1)

    def test_fall_on_ground(self):

        # Create particle fall settings to force downward wind
        particle_fall_settings = agentframework.ParticleFallSettings(0, 100, 0)

        # Initialize building height
        building_height = 0

        # Create test agent
        agent = AgentTestCase.create_agent(
            particle_fall_settings=particle_fall_settings,
            building_height=building_height
        )

        self.assertFalse(agent.can_fall())

        # Attempt to move the agent
        agent.fall()
        
        # Verify no agent movement
        self.assertEqual(agent._height, building_height)


    @staticmethod
    def create_agent(
        particle_fall_settings=None,
        wind_settings=None,
        position=None,
        building_height=None
    ):
        # Create agent
        return agentframework.Agent(
            TEST_PARTICLE_FALL_SETTINGS if particle_fall_settings is None else particle_fall_settings,
            TEST_WIND_SETTINGS if wind_settings is None else wind_settings,
            TEST_POSITION if position is None else position,
            TEST_BUILDING_HEIGHT if building_height is None else building_height,
            
        )
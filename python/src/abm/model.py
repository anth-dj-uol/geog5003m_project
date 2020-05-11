#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model module

Provides classes used to represent agent-based models.

@author: Anthony Jarrett
"""

import os

from . import agentframework, logger

DEFAULT_NUM_OF_PARTICLES = 5000
DEFAULT_BOMB_HEIGHT_METRES = 75
DEFAULT_BOMB_LOCATION_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + \
    os.sep + '../wind.raster'

class Model():

    def __init__(self, parameters=None):

        # If parameters are not provided, use default values
        if parameters is None:
            parameters = self._get_default_parameters()

        # Set the model parameters
        self._parameters = parameters

        # Initialize the model agents
        self.initialize()


    def __str__(self):
        return \
"""=======================================
                Model
---------------------------------------

{}
=======================================""".format(self._parameters)

    @property
    def parameters(self):
        """
        Get the model parameters.
        """
        return self._parameters

    @parameters.deleter
    def parameters(self):
        """
        Delete the model parameters property.
        """
        del self._parameters

    @property
    def agents(self):
        """
        Get the model agents.
        """
        return self._agents

    @agents.deleter
    def agents(self):
        """
        Delete the model agents property.
        """
        del self._agents

    def initialize(self):

        # Set the model agents
        self._agents = self._create_agents(self._parameters.num_of_particles)


    def run(self):

        logger.log("Starting model simulation...")

        # Track the iteration count
        iteration_count = 0

        # Track whether the model can iterate
        can_iterate = True

        # Run model iterations while at least one particle can move
        while can_iterate:

            # Increment the iteration count
            iteration_count += 1

            # Iterate the model
            can_iterate = self.iterate()
        
        logger.log("Done model simulation after iteration {}", iteration_count)

        # Return the resulting particle density environment
        return self._get_particle_density_environment()

    def iterate(self):

        can_iterate = False

        # Move each agent in the model
        for agent in self._agents:
            agent.move()
            agent.fall()
            if agent.can_move():
                can_iterate = True

        return can_iterate


    def update_parameters(self, particle_fall_settings, wind_settings, num_of_particles):
        self.parameters.particle_fall_settings = particle_fall_settings
        self.parameters.wind_settings = wind_settings
        self.parameters.num_of_particles = num_of_particles


    def _get_particle_density_environment(self):

        # Create a new environment using the size of the bomb environment
        environment = agentframework.Environment.create_from_size(
            self._parameters._environment.height,
            self._parameters._environment.width
        )
        
        # Increment the environment value at the position of each agent
        for agent in self._agents:

            # Check if the agent position is within the environment bounds
            if environment.contains(agent.position):

                # Increment the environment location value
                environment.plane[agent.position.y][agent.position.x] += 1

        return environment

    def _get_default_parameters(self):

        # Create default particle fall settings
        particle_fall_settings = agentframework.ParticleFallSettings()

        # Create default wind settings
        wind_settings = agentframework.WindSettings()

        # Load bomb environment
        environment = agentframework.BombEnvironment.create_from_file(DEFAULT_BOMB_LOCATION_FILE_PATH)

        # Set default number of particles
        num_of_particles = DEFAULT_NUM_OF_PARTICLES

        # Set default bomb height
        bomb_height_metres = DEFAULT_BOMB_HEIGHT_METRES

        # Return parameters
        return Parameters(particle_fall_settings, wind_settings, environment, num_of_particles, bomb_height_metres)

    def _create_agents(self, num_of_agents):

        # Initialize agents list
        agents = []

        # Create each agent
        for i in range(num_of_agents):
            agents.append(agentframework.Agent(
                self._parameters.particle_fall_settings,
                self._parameters.wind_settings,
                self._parameters.environment.bomb_position,
                self._parameters.bomb_height_metres
            ))

        return agents


class Parameters():

    def __init__(self, particle_fall_settings, wind_settings, environment, num_of_particles, bomb_height_metres):
        self._particle_fall_settings = particle_fall_settings
        self._wind_settings = wind_settings
        self._environment = environment
        self._num_of_particles = num_of_particles
        self._bomb_height_metres = bomb_height_metres

    def __str__(self):
        return \
"""Particle Fall Settings
{}

Wind Settings
{}

Environment
{}

Number of particles
{}

Bomb height (m)
{}
""".format(
    self.particle_fall_settings,
    self.wind_settings,
    self.environment,
    self.num_of_particles,
    self.bomb_height_metres
)

    @property
    def particle_fall_settings(self):
        """
        Get the particle fall settings.
        """
        return self._particle_fall_settings

    @particle_fall_settings.setter
    def particle_fall_settings(self, value):
        """
        Set the particle fall settings.
        """
        self._particle_fall_settings = value

    @particle_fall_settings.deleter
    def particle_fall_settings(self):
        """
        Delete the particle fall settings property.
        """
        del self._particle_fall_settings

    @property
    def wind_settings(self):
        """
        Get the wind settings.
        """
        return self._wind_settings

    @wind_settings.setter
    def wind_settings(self, value):
        """
        Set the wind settings.
        """
        self._wind_settings = value

    @wind_settings.deleter
    def wind_settings(self):
        """
        Delete the wind settings property.
        """
        del self._wind_settings

    @property
    def environment(self):
        """
        Get the environment.
        """
        return self._environment

    @environment.setter
    def environment(self, value):
        """
        Set the environment.
        """
        self._environment = value

    @environment.deleter
    def environment(self):
        """
        Delete the environment property.
        """
        del self._environment

    @property
    def num_of_particles(self):
        """
        Get the number of particles.
        """
        return self._num_of_particles
    
    @num_of_particles.setter
    def num_of_particles(self, value):
        """
        Set the number of particles.
        """
        self._num_of_particles = value
    
    @num_of_particles.deleter
    def num_of_particles(self):
        """
        Delete the number of particles property.
        """
        del self._num_of_particles

    @property
    def bomb_height_metres(self):
        """
        Get the bomb height in metres.
        """
        return self._bomb_height_metres
    
    @bomb_height_metres.setter
    def bomb_height_metres(self, value):
        """
        Set the bomb height in metres.
        """
        self._bomb_height_metres = value
    
    @bomb_height_metres.deleter
    def bomb_height_metres(self):
        """
        Delete the bomb height property.
        """
        del self._bomb_height_metres


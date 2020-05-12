#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model module

Provides classes used to represent agent-based models.

@author: Anthony Jarrett
"""

import os

from . import agentframework, logger


# Initialize default values
DEFAULT_NUM_OF_PARTICLES = 5000
DEFAULT_BUILDING_HEIGHT_METRES = 75
DEFAULT_MAX_NUM_OF_ITERATIONS = 1000
DEFAULT_BOMB_LOCATION_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + \
    os.sep + '../wind.raster'

class Model():
    """
    Implementation of an agent-based model.
    
    Public Methods:
        
        initialize -        initializes the model instance
                    
        run -               run a model simulation
        
        update_parameters - update the model parameters
    """

    def __init__(self, parameters=None):
        """
        Create a new Model instance.

        Parameters
        ----------
        parameters : Parameters, optional
            Used as the model parameters, or default parameters are used if 
            None is specified. The default is None.

        Returns
        -------
        None.

        """

        logger.log("Instantiating a Model.")

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

    @property
    def result_environment(self):
        """
        Get the result environment.
        """
        return self._result_environment

    @result_environment.deleter
    def result_environment(self):
        """
        Delete the result environment property.
        """
        del self._result_environment


    def initialize(self):
        """
        Creates a new list of model agents using the currently configured
        parameters.

        Returns
        -------
        None.

        """

        # Set the model agents
        self._agents = self._create_agents(self._parameters.num_of_particles)

        # Clear the result environment
        self._result_environment = None


    def run(self):
        """
        Run a model simulation.
        
        The resulting particle density environment will be stored in the model.

        Returns
        -------
        agentframework.Environment
            The restuling particle density environment.

        """

        logger.log("Starting model simulation...")

        # Track the maximum iteration count
        max_iteration_count = 0

        # Track the number of particles that did not land in time
        num_particles_still_in_air = 0

        for agent in self._agents:

            # Track the iteration count
            iteration_count = 0

            # Run model iterations while at least one particle can move
            while agent.can_fall():

                # Move the particle according to the wind settings
                agent.move()

                # Drop the particle according to the particle fall settings
                agent.fall()

                # Increment the iteration count
                iteration_count += 1
            
                # Abort if the maximum number of iterations has been reached
                if iteration_count >= self.parameters.max_num_of_iterations:
                    num_particles_still_in_air += 1
                    break

            # Update the maximum iteration count
            if iteration_count > max_iteration_count:
                max_iteration_count = iteration_count

        logger.log("{} particles did no reach the ground in time", num_particles_still_in_air)
        logger.log("Done simulation. Last particle reached the ground at {} seconds", max_iteration_count)

        # Set and return the resulting particle density environment
        self._result_environment = self._get_particle_density_environment()
        return self._result_environment


    def update_parameters(
        self,
        particle_fall_settings,
        wind_settings,
        num_of_particles,
        building_height_metres,
        max_num_of_iterations
    ):
        """
        Update the model parameters

        Parameters
        ----------
        particle_fall_settings : agentframework.ParticleFallSettings
            The particle fall settings.
        wind_settings : agentframework.WindSettings
            The wind settings.
        num_of_particles : int
            The number of particles to simulate.
        building_height_metres : int
            The building height, used as the initial partical heights.
        max_num_of_iterations : int
            The maximum number of iterations allowed in a simulation.

        Returns
        -------
        None.

        """

        # Update the model parameter values
        self.parameters.particle_fall_settings = particle_fall_settings
        self.parameters.wind_settings = wind_settings
        self.parameters.num_of_particles = num_of_particles
        self.parameters.building_height_metres = building_height_metres
        self.parameters.max_num_of_iterations = max_num_of_iterations


    def _get_particle_density_environment(self):
        """
        Create a particle density environment.
        
        Each cell in the environment will contain a value representing the
        number of particles that have landed at that position.

        Returns
        -------
        environment : agentframework.Environment
            The resulting particle density environment.

        """

        # Create a new environment using the size of the bomb environment
        environment = agentframework.Environment.create_from_size(
            self._parameters._environment.width,
            self._parameters._environment.height
        )
        
        # Increment the environment value at the position of each agent
        for agent in self._agents:

            # Check if the agent position is within the environment bounds
            if environment.contains(agent.position):

                # Increment the environment location value
                environment.plane[agent.position.y][agent.position.x] += 1

        return environment

    def _get_default_parameters(self):
        """
        Get the default model parameters.

        Returns
        -------
        Parameters
            The default model parameters.

        """

        # Return default parameters
        return Parameters(
            agentframework.ParticleFallSettings(),
            agentframework.WindSettings(),
            agentframework.BombEnvironment.create_from_file(DEFAULT_BOMB_LOCATION_FILE_PATH),
            DEFAULT_NUM_OF_PARTICLES,
            DEFAULT_BUILDING_HEIGHT_METRES,
            DEFAULT_MAX_NUM_OF_ITERATIONS
        )

    def _create_agents(self, num_of_agents):
        """
        Create a list of agents.

        Parameters
        ----------
        num_of_agents : int
            Number of agents to create.

        Returns
        -------
        agents : list[agentframework.Agent]
            A list of agents.

        """

        # Initialize agents list
        agents = []

        # Create each agent
        for i in range(num_of_agents):
            agents.append(agentframework.Agent(
                self._parameters.particle_fall_settings,
                self._parameters.wind_settings,
                self._parameters.environment.bomb_position,
                self._parameters.building_height_metres
            ))

        # Return the resulting list of agents
        return agents


class Parameters():
    """
    A collection of model parameters.
    """

    def __init__(self, particle_fall_settings, wind_settings, environment, num_of_particles, building_height_metres, max_num_of_iterations):
        """
        Create a new Parameters instance.

        Parameters
        ----------
        particle_fall_settings : agentframework.ParticleFallSettings
            The particle fall settings.
        wind_settings : agentframework.WindSettings
            The wind settings.
        environment : agentframework.BombEnvironment
            The bomb environment.
        num_of_particles : int
            The number of particles in the model.
        building_height_metres : int
            The building height at which the bacterial bomb is released.
        max_num_of_iterations : int
            The maximum number of iterations allowed in the simulation.

        Returns
        -------
        None.

        """
        # Initialize the parameters properties
        self._particle_fall_settings = particle_fall_settings
        self._wind_settings = wind_settings
        self._environment = environment
        self._num_of_particles = num_of_particles
        self._building_height_metres = building_height_metres
        self._max_num_of_iterations = max_num_of_iterations

    def __str__(self):
        """
        Get a string representation of the parameters.

        Returns
        -------
        None.

        """
        return \
"""Particle Fall Settings
{}

Wind Settings
{}

Environment
{}

Number of particles
{}

Building height (m)
{}

Maximum number of iterations: {}
""".format(
    self.particle_fall_settings,
    self.wind_settings,
    self.environment,
    self.num_of_particles,
    self.building_height_metres,
    self.max_num_of_iterations
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
    def building_height_metres(self):
        """
        Get the building height in metres.
        """
        return self._building_height_metres
    
    @building_height_metres.setter
    def building_height_metres(self, value):
        """
        Set the building height in metres.
        """
        self._building_height_metres = value
    
    @building_height_metres.deleter
    def building_height_metres(self):
        """
        Delete the building height property.
        """
        del self._building_height_metres

    @property
    def max_num_of_iterations(self):
        """
        Get the maximum number of iterations.
        """
        return self._max_num_of_iterations
    
    @max_num_of_iterations.setter
    def max_num_of_iterations(self, value):
        """
        Set the maximum number of iterations.
        """
        self._max_num_of_iterations = value
    
    @max_num_of_iterations.deleter
    def max_num_of_iterations(self):
        """
        Delete the maximum number of iterations property.
        """
        del self._max_num_of_iterations


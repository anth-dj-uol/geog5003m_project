#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model module

Provides classes used to represent agent-based models.

@author: Anthony Jarrett
"""

import csv


DEFAULT_NUM_OF_PARTICLES = 5000
DEFAULT_BOMB_LOCATION_FILE_PATH = 'wind.raster'
DEFAULT_LIMIT_ENVIRONMENT= False

class Model():

    def __init__(self, parameters):
        self._parameters = parameters


class Parameters():

    def __init__(self, wind_model, bomb_location,
        num_of_particles=DEFAULT_NUM_OF_PARTICLES,
        bomb_location_file_path=DEFAULT_BOMB_LOCATION_FILE_PATH,
        limit_environment=DEFAULT_LIMIT_ENVIRONMENT):
        self._wind_model = wind_model
        self._bomb_location = bomb_location
        self._num_of_particles = num_of_particles
        self._limit_environment = limit_environment

    @property
    def wind_model(self):
        """
        Get the wind model.
        """
        return self._wind_model

    @wind_model.setter
    def wind_model(self, value):
        """
        Set the wind model.
        """
        self._wind_model = value

    @wind_model.deleter
    def wind_model(self):
        """
        Delete the wind model property.
        """
        del self._wind_model

    @property
    def bomb_location(self):
        """
        Get the bomb location.
        """
        return self._bomb_location

    @bomb_location.setter
    def bomb_location(self, value):
        """
        Set the bomb location.
        """
        self._bomb_location = value

    @wind_model.deleter
    def bomb_location(self):
        """
        Delete the bomb location property.
        """
        del self._bomb_location

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
    
    @wind_model.deleter
    def num_of_particles(self):
        """
        Delete the number of particles property.
        """
        del self._num_of_particles


class LocationReader():

    def __init__(self, file_path):
        self._file_path = file_path

    def read_location(self):

        # Initialize the environment plane
        environment_plane = []

        # Open the given file
        try:
            with open(self._file_path, newline='') as f:
                
                # Create a CSV reader
                reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
                
                # Read in each row and column to obtain the 2-D environment data
                for row in reader:
                    row_list = []
                    for value in row:
                        row_list.append(value)
                    environment_plane.append(row_list)
        except:
            # Display error message on enviroment read failure
            raise Exception("Unable to read environment from file: {}".format(self._file_path))
            
            # Abort creation of new environment
            return

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Framework module

Provides classes used to represent agents and their data.

@author: Anthony Jarrett
"""

import csv

DEFAULT_WIND_NORTH_PERCENTAGE = .1
DEFAULT_WIND_EAST_PERCENTAGE = .75
DEFAULT_WIND_SOUTH_PERCENTAGE = .1
DEFAULT_WIND_WEST_PERCENTAGE = .05

class Agent():

    def __init__(self, wind_settings, start_position):
        self._wind_settings = wind_settings
        self._position = start_position

    def move(self):
        pass


class WindSettings():

    def __init__(self, north_percentage=DEFAULT_WIND_NORTH_PERCENTAGE,
        east_percentage=DEFAULT_WIND_EAST_PERCENTAGE,
        south_percentage=DEFAULT_WIND_SOUTH_PERCENTAGE,
        west_percentage=DEFAULT_WIND_WEST_PERCENTAGE):
        self._north_percentage = north_percentage
        self._east_percentage = east_percentage
        self._south_percentage = south_percentage
        self._west_percentage = west_percentage

    @property
    def north_percentage(self):
        """
        Get the chance of wind blowing north.
        """
        return self._north_percentage

    @north_percentage.deleter
    def north_percentage(self):
        """
        Delete the north percentage property.
        """
        del self._north_percentage

    @property
    def east_percentage(self):
        """
        Get the chance of wind blowing east.
        """
        return self._east_percentage

    @east_percentage.deleter
    def east_percentage(self):
        """
        Delete the east percentage property.
        """
        del self._east_percentage

    @property
    def south_percentage(self):
        """
        Get the chance of wind blowing south.
        """
        return self._south_percentage

    @south_percentage.deleter
    def south_percentage(self):
        """
        Delete the south percentage property.
        """
        del self._south_percentage

    @property
    def west_percentage(self):
        """
        Get the chance of wind blowing west.
        """
        return self._west_percentage

    @west_percentage.deleter
    def west_percentage(self):
        """
        Delete the west percentage property.
        """
        del self._west_percentage


class Position():

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        Get the x-axis position.
        """
        return self._x

    @x.deleter
    def x(self):
        """
        Delete the x-axis position.
        """
        del self._x

    @property
    def y(self):
        """
        Get the y-axis position.
        """
        return self._y

    @y.deleter
    def y(self):
        """
        Delete the y-axis position.
        """
        del self._y


class Environment():

    def __init__(self, plane):
        self._plane = plane

    @property
    def plane(self):
        """
        Get the plane 2-D array.
        """
        return self._plane

    @plane.deleter
    def plane(self):
        """
        Delete the plane property.
        """
        del self._plane

    @staticmethod
    def read_from_file(file_path):

        # Initialize the environment plane
        environment_plane = []

        # Open the given file
        try:
            with open(file_path, newline='') as f:
                
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
            raise Exception("Unable to read environment from file: {}".format(file_path))
            
            # Abort creation of new environment
            return
        
        # Return the resulting environment
        return Environment(environment_plane)

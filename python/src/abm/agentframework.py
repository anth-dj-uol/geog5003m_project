#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Framework module

Provides classes used to represent agents and their data.

@author: Anthony Jarrett
"""

import csv

from . import logger

# Set default values

DEFAULT_FALL_UP_PERCENTAGE = .2
DEFAULT_FALL_DOWN_PERCENTAGE = .7
DEFAULT_FALL_NO_CHANGE_PERCENTAGE = .1

DEFAULT_WIND_NORTH_PERCENTAGE = .1
DEFAULT_WIND_EAST_PERCENTAGE = .75
DEFAULT_WIND_SOUTH_PERCENTAGE = .1
DEFAULT_WIND_WEST_PERCENTAGE = .05

DEFAULT_BOMB_POSITION_MARK = 255

class Agent():

    def __init__(self, particle_fall_settings, wind_settings, start_position, start_height):
        self._particle_fall_settings = particle_fall_settings
        self._wind_settings = wind_settings
        self._position = start_position
        self._height = start_height

    def move(self):
        pass

    def can_move(self):
        return False

class ParticleFallSettings():

    def __init__(self, up_percentage=DEFAULT_FALL_UP_PERCENTAGE,
        down_percentage=DEFAULT_FALL_DOWN_PERCENTAGE,
        no_change_percentage=DEFAULT_FALL_NO_CHANGE_PERCENTAGE):
        self._up_percentage = up_percentage
        self._down_percentage = down_percentage
        self._no_change_percentage = no_change_percentage

    def __str__(self):
        return """Chance of moving up: {}
Chance of moving down: {}
Chance of no vertical movement: {}""".format(
    self._up_percentage,
    self._down_percentage,
    self._no_change_percentage
)

    @property
    def up_percentage(self):
        """
        Get the chance of upward particle movement.
        """
        return self._up_percentage

    @up_percentage.deleter
    def up_percentage(self):
        """
        Delete the upward movement chance property.
        """
        del self._up_percentage

    @property
    def down_percentage(self):
        """
        Get the chance of downward particle movement.
        """
        return self._down_percentage

    @down_percentage.deleter
    def down_percentage(self):
        """
        Delete the downward movement chance property.
        """
        del self._down_percentage

    @property
    def no_change_percentage(self):
        """
        Get the chance of no vertical particle movement.
        """
        return self._no_change_percentage

    @no_change_percentage.deleter
    def no_change_percentage(self):
        """
        Delete the no change movement chance property.
        """
        del self._no_change_percentage


class WindSettings():

    def __init__(self, north_percentage=DEFAULT_WIND_NORTH_PERCENTAGE,
        east_percentage=DEFAULT_WIND_EAST_PERCENTAGE,
        south_percentage=DEFAULT_WIND_SOUTH_PERCENTAGE,
        west_percentage=DEFAULT_WIND_WEST_PERCENTAGE):
        self._north_percentage = north_percentage
        self._east_percentage = east_percentage
        self._south_percentage = south_percentage
        self._west_percentage = west_percentage

    def __str__(self):
        return """Chance of north travel: {}
Chance of east travel: {}
Chance of south travel: {}
Chance of west travel: {}""".format(
    self._north_percentage,
    self._east_percentage,
    self._south_percentage,
    self._west_percentage
)

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

    def __str__(self):
        return """{},{}""".format(self.x, self.y)

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

    def __init__(self, plane, bomb_position):
        self._plane = plane
        self._bomb_position = bomb_position

        self._width = len(self._plane)
        self._height = len(self._plane[0])

    def __str__(self):
        return """Size: {}x{}
Bomb Position: {}""".format(
    self._width,
    self._height,
    self._bomb_position
)


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

    @property
    def bomb_position(self):
        """
        Get the bomb position.
        """
        return self._bomb_position

    @bomb_position.deleter
    def bomb_position(self):
        """
        Delete the bomb position property.
        """
        del self._bomb_position


    @staticmethod
    def read_from_file(file_path, bomb_position_mark=DEFAULT_BOMB_POSITION_MARK):

        # Initialize the environment plane
        environment_plane = []

        # Initialize the bomb position
        bomb_position = None

        # Open the given file
        try:
            with open(file_path, newline='') as f:
                
                # Create a CSV reader
                reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)

                # Store a reference to the current row being processed
                row_index = 0

                # Read in each row and column to obtain the 2-D environment data
                for row in reader:
                    row_list = []

                    # Store a reference to the current column being processed
                    column_index = 0

                    for value in row:
                        row_list.append(value)

                        # Store the bomb position when found
                        if value == bomb_position_mark:
                            bomb_position = Position(column_index, row_index)

                        # Increment the current column index
                        column_index += 1

                    # Add the environment row
                    environment_plane.append(row_list)

                    # Increment the current row index
                    row_index += 1
        except:
            # Raise an error on enviroment read failure
            raise Exception("Unable to read environment from file: {}".format(file_path))
            
            # Abort creation of new environment
            return

        # Raise an error when bomb position is not found
        if bomb_position is None:
            raise Exception("Environment does not contain a bomb position (indicated by value: {})" \
                .format(bomb_position_mark))
        
        # Return the resulting environment
        return Environment(environment_plane, bomb_position)

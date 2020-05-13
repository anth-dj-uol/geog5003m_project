#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Framework module

Provides classes used to represent agents and their data.

@author: Anthony Jarrett
"""

import csv
from enum import Enum
from random import random

from . import logger


# Set default values
DEFAULT_FALL_UP_PERCENTAGE = 20
DEFAULT_FALL_DOWN_PERCENTAGE = 70
DEFAULT_FALL_NO_CHANGE_PERCENTAGE = 10
DEFAULT_WIND_NORTH_PERCENTAGE = 10
DEFAULT_WIND_EAST_PERCENTAGE = 75
DEFAULT_WIND_SOUTH_PERCENTAGE = 10
DEFAULT_WIND_WEST_PERCENTAGE = 5
DEFAULT_BOMB_POSITION_MARK = 255


class Agent():
    """
    An implementation of a bacterial bomb partical agent.
    
    The Agent can move and fall according to the configured wind and particle
    fall settings. The particle will start its fall from its configured
    start position and building height.
    
    Public Methods:
        
        move -  moves the Agent one metre North, East, South or West using the
                configured wind settings probabilities.
        
        fall -  causes a particle to fall upward, downward or to have no
                vertical movement using the configured particle fall settings
                probabilities.

        can_fall - returns True if the particle has not yet hit the ground
    """

    def __init__(self, particle_fall_settings, wind_settings, start_position, building_height):
        """
        Create an Agent instance.

        Parameters
        ----------
        particle_fall_settings : agentframework.ParticleFallSettings
            The particle fall settings for the agent.
        wind_settings : agentframework.WindSettings
            The wind settings for the agent.
        start_position : agentframework.Position
            The start position for the agent.
        building_height : int
            The start height of the agent.

        Returns
        -------
        None.

        """

        # Set agent properties
        self._particle_fall_settings = particle_fall_settings
        self._wind_settings = wind_settings
        self._position = Position.create_from(start_position)
        self._building_height = building_height
        self._height = building_height

    @property
    def position(self):
        """
        Get the agent position.
        """
        return self._position

    @position.deleter
    def position(self):
        """
        Delete the agent position property.
        """
        del self._position

    def move(self):
        """
        Move the agent along the environment plane.
        
        This method will move the agent North, East, South or West according
        to the configured wind settings probabilities.

        Returns
        -------
        None.

        """

        # Get a new wind direction
        direction = self._wind_settings.get_next()

        # Move the particle in the obtained direction
        if direction == Direction.NORTH:
            self._position.y += 1
        elif direction == Direction.EAST:
            self._position.x += 1
        elif direction == Direction.SOUTH:
            self._position.y -= 1
        else:
            self._position.x -= 1

    def fall(self):
        """
        Move the agent along the altitude plane.
        
        This method will move the agent up, down or not move at all according
        to the configured particle fall settings probabilities.

        Returns
        -------
        None.

        """

        # Check if the particle can fall any further
        if self.can_fall():

            # If below the building height, particle always falls
            if self._height < self._building_height:
                self._height -= 1

            else:
                # Get a new fall direction
                fall = self._particle_fall_settings.get_next()

                # Change the particle height according to the fall direction
                if fall == Fall.UP:
                    self._height += 1
                elif fall == Fall.DOWN:
                    self._height -= 1

    def can_fall(self):
        """
        Return if the particle has not yet hit the ground.

        Returns
        -------
        bool
            True if the particle has not yet hit the ground, otherwise False.

        """
        return self._height > 0


class Fall(Enum):
    """
    An enum representing possiblt fall directions.
    """
    UP = 1
    DOWN = 2
    NONE = 3



class ParticleFallSettings():
    """
    A collection of probability percentage values for particle fall direction.
    
    Public Methods:
        
        get_next -  returns the next fall direction using the
                    configured direction probabilities.
                    
        equals -    returns whether one instance equals another
    """

    def __init__(self, up_percentage=DEFAULT_FALL_UP_PERCENTAGE,
        down_percentage=DEFAULT_FALL_DOWN_PERCENTAGE,
        no_change_percentage=DEFAULT_FALL_NO_CHANGE_PERCENTAGE):
        """
        Create a particle fall settings instance.

        Parameters
        ----------
        up_percentage : int, optional
            The percentage probability that the particle will fall upwards.
            The default is agentframework.DEFAULT_FALL_UP_PERCENTAGE.
        down_percentage : int, optional
            The percentage probability that the particle will fall downwards.
            The default is agentframework.DEFAULT_FALL_DOWN_PERCENTAGE.
        no_change_percentage : int, optional
            The percentage probability that the particle will not change
            its vertical height. The default is
            agentframework.DEFAULT_FALL_NO_CHANGE_PERCENTAGE.

        Raises
        ------
        Exception
            An exception is raised when the given percentage values do not
            add up to 100.

        Returns
        -------
        None.

        """

        # Set particle fall settings properties
        self._up_percentage = up_percentage
        self._down_percentage = down_percentage
        self._no_change_percentage = no_change_percentage

        # Validate percentage sum
        percentage_sum = up_percentage + down_percentage + no_change_percentage
        if percentage_sum != 100:
            raise Exception("Particle fall percentages must add up to 100 (current value is {})".format(percentage_sum))

        # Precalculate thresholds to improve performance
        self._up_threshold_mark = self._up_percentage
        self._down_threshold_mark = self._up_threshold_mark + self._down_percentage

        logger.log("Up threshold mark: {}", self._up_threshold_mark)
        logger.log("Down threshold mark: {}", self._down_threshold_mark)


    def __str__(self):
        """
        Return a string representation of the object.

        Returns
        -------
        None.

        """
        return """Chance of moving up: {}
Chance of moving down: {}
Chance of no vertical movement: {}""".format(
    self._up_percentage,
    self._down_percentage,
    self._no_change_percentage
)

    def get_next(self):
        """
        Get the next fall direction using the configured probabilities.

        Returns
        -------
        agentframework.Fall
            The next fall direction.

        """

        # Generate a random number from 0 - 100
        value = random() * 100

        # Return the fall direction according to the stored thresholds
        if value <= self._up_threshold_mark:
            return Fall.UP
        elif value <= self._down_threshold_mark:
            return Fall.DOWN
        return Fall.NONE


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

    def equals(self, other):
        """
        Check if the current settings are equal to the specified settings.

        Parameters
        ----------
        other : agentframework.ParticleFallSettings
            The object to compare.

        Returns
        -------
        bool
            Returns True if euqal probabilities, otherwise returns false.

        """

        return  self.down_percentage == other.down_percentage and \
                self.up_percentage == other.up_percentage and \
                self.no_change_percentage == other.no_change_percentage


class Direction(Enum):
    """
    An enum representing the possible particle movement directions.
    """
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class WindSettings():
    """
    A collection of probability percentage values for particle movement
    direction along the environment plane.
    
    Public Methods:
        
        get_next -  returns the next movement direction using the
                    configured direction probabilities.
            
        equals -    returns whether one instance equals another
    """

    def __init__(self, north_percentage=DEFAULT_WIND_NORTH_PERCENTAGE,
        east_percentage=DEFAULT_WIND_EAST_PERCENTAGE,
        south_percentage=DEFAULT_WIND_SOUTH_PERCENTAGE,
        west_percentage=DEFAULT_WIND_WEST_PERCENTAGE):
        """
        Create a wind settings instance.

        Parameters
        ----------
        north_percentage : int, optional
            The percentage probability that the particle will move North.
            The default is agentframework.DEFAULT_WIND_NORTH_PERCENTAGE.
        east_percentage : int, optional
            The percentage probability that the particle will move East.
            The default is agentframework.DEFAULT_WIND_EAST_PERCENTAGE.
        south_percentage : int, optional
            The percentage probability that the particle will move South.
            The default is agentframework.DEFAULT_WIND_SOUTH_PERCENTAGE.
        west_percentage : int, optional
            The percentage probability that the particle will move West.
            The default is agentframework.DEFAULT_WIND_WEST_PERCENTAGE.

        Raises
        ------
        Exception
            An exception is raised when the given percentage values do not
            add up to 100.

        Returns
        -------
        None.

        """

        # Set the wind settings properties
        self._north_percentage = north_percentage
        self._east_percentage = east_percentage
        self._south_percentage = south_percentage
        self._west_percentage = west_percentage

        # Validate percentage sum
        percentage_sum = north_percentage + east_percentage + south_percentage + west_percentage
        if percentage_sum != 100:
            raise Exception("Wind direction percentages must add up to 100 (current value is{})".format(percentage_sum))

        # Precalculate thresholds to improve performance
        self._north_percentage_threshold = self._north_percentage
        self._east_percentage_threshold = self._north_percentage_threshold + self._east_percentage
        self._south_percentage_threshold = self._east_percentage_threshold + self._south_percentage

        logger.log("North threshold mark: {}", self._north_percentage_threshold)
        logger.log("East threshold mark: {}", self._east_percentage_threshold)
        logger.log("South threshold mark: {}", self._south_percentage_threshold)


    def __str__(self):
        """
        Get a string representation of the wind settings.

        Returns
        -------
        None.

        """

        return """Chance of north travel: {}
Chance of east travel: {}
Chance of south travel: {}
Chance of west travel: {}""".format(
    self._north_percentage,
    self._east_percentage,
    self._south_percentage,
    self._west_percentage
)

    def get_next(self):
        """
        Get the next movement direction using the configured probabilities.

        Returns
        -------
        agentframework.Direction
            The next movement direction.

        """

        # Generate a random number from 0-100
        value = random() * 100

        # Return the wind direction according to the stored thresholds
        if value <= self._north_percentage_threshold:
            return Direction.NORTH
        elif value <= self._east_percentage_threshold:
            return Direction.EAST
        elif value <= self._south_percentage_threshold:
            return Direction.SOUTH
        return Direction.WEST

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

    def equals(self, other):
        """
        Check if the current settings are equal to the specified settings.

        Parameters
        ----------
        other : agentframework.WindSettings
            The object to compare.

        Returns
        -------
        bool
            Returns True if euqal probabilities, otherwise returns false.

        """

        # Check if all properties are equal
        return  self.north_percentage == other.north_percentage and \
                self.east_percentage == other.east_percentage and \
                self.south_percentage == other.south_percentage and \
                self.west_percentage == other.west_percentage


class Position():
    """
    A class representing a position within a 2-dimensional plane.
    The plane origin is at the bottom-left corner of the environment.
    
    Public Methods:
        
        equals - returns whether one instance equals another
        
    Public Static Methods:
        
        create_from - creates a new instance from the given Position
    """

    def __init__(self, x, y):
        """
        Create a new Position instance.

        Parameters
        ----------
        x : int
            x-axis position.
        y : int
            y-axis position.

        Returns
        -------
        None.

        """
        # Set the position properties
        self._x = x
        self._y = y

    def __str__(self):
        """
        Get a string representation of a Position.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return """{},{}""".format(self.x, self.y)

    @property
    def x(self):
        """
        Get the x-axis position.
        """
        return self._x

    @x.setter
    def x(self, value):
        """
        Set the x-axis position.
        """
        self._x = value

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

    @y.setter
    def y(self, value):
        """
        Set the y-axis position.
        """
        self._y = value

    @y.deleter
    def y(self):
        """
        Delete the y-axis position.
        """
        del self._y

    def equals(self, other):
        """
        Check if the current Positionosition is equal to the specified Position.

        Parameters
        ----------
        other : agentframework.Position
            The object to compare.

        Returns
        -------
        bool
            Returns True if euqal positions, otherwise returns false.

        """

        # Check if all properties are equal
        return self.x == other.x and self.y == other.y

    @staticmethod
    def create_from(original):
        """
        Create a new instance from the specified position.

        Parameters
        ----------
        original : agentframework.Position
            The position to copy.

        Returns
        -------
        agentframework.Position
            The new Position instance.

        """
        # Return a copy of the provided position
        return Position(original.x, original.y)


class Environment():
    """
    A class representing a 2-dimensional plane.
    
    Public Methods:
        
        contains - returns whether a position is within the environment bounds.
        
    Public Static Methods:
        
        create_from_size -  creates a new instance using the specified
                            dimensions.
    """

    def __init__(self, plane):
        """
        Create a new Environment instance

        Parameters
        ----------
        plane : list[list[int]]
            2-dimensional array representing the environment plane.

        Raises
        ------
        Exception
            Raises an exception when the specified plane is not a 2-dimensional
            array.

        Returns
        -------
        None.

        """

        # Check that a valid plane is passed
        if  not isinstance(plane, list) or \
            len(plane) <= 0 or \
            not isinstance(plane[0], list):
            raise Exception("Plane must be a 2-D array")

        # Set the instance properties
        self._plane = plane
        self._height = len(self._plane)
        self._width = len(self._plane[0])

    def __str__(self):
        """
        Get a string representation of an environment.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        return """Size: {}x{}""".format(
            self._width,
            self._height
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
    def width(self):
        """
        Get the plane width.
        """
        return self._width

    @width.deleter
    def width(self):
        """
        Delete the plane width property.
        """
        del self._width

    @property
    def height(self):
        """
        Get the plane height.
        """
        return self._height

    @height.deleter
    def height(self):
        """
        Delete the plane height property.
        """
        del self._height

    def contains(self, position):
        """
        Check if the specified position is within the environment.

        Parameters
        ----------
        position : agentframework.Position
            The position to check.

        Returns
        -------
        bool
            Returns True if the position lies within the environment bounds,
            otherwise returns False.

        """

        # Check if the agent position is within the environment bounds
        return position.y < self.height and position.x < self.width

    @staticmethod
    def create_from_size(width, height, initial_value=0):
        """
        Create a new environment from the specified dimensions.

        Parameters
        ----------
        width : int
            Environment x-axis length.
        height : int
            Environment y-axis length.
        initial_value : int, optional
            Initial environment cell value. The default is 0.

        Returns
        -------
        agentframework.Environment
            A new Environment instance of the given size.

        """

        # Create initial plane array
        plane = []
        for i in range(height):

            # Create row array
            row = []
            for j in range(width):

                # Add the new cell to the current row
                row.append(initial_value)

            # Add the new row to the environment plane
            plane.append(row)

        return Environment(plane)


class BombEnvironment(Environment):
    """
    A class representing a an environment that has a bomb location.
            
    Public Static Methods:
        
        create_from_file -  creates a new instance from the specified
                            raster text file.
    """

    def __init__(self, plane, bomb_position):
        """
        Create a new BombEnvironment instance.

        Parameters
        ----------
        plane : list[list[int]]
            2-dimensional array representing the environment plane.

        bomb_position : agentframework.Position
            The location of the bomb.

        Returns
        -------
        None.

        """
        super().__init__(plane)

        # Set the bomb position property
        self._bomb_position = bomb_position

    def __str__(self):
        """
        Get a string representation of a BombEnvironment.

        Returns
        -------
        None.

        """
        return """Size: {}x{}
Bomb Position: {}""".format(
    self._width,
    self._height,
    self._bomb_position
)

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
    def create_from_file(file_path, bomb_position_mark=DEFAULT_BOMB_POSITION_MARK):
        """
        Create a new BombEnvironment from the provided raster text file path.
        
        The input file should be a text-formatted raster, where each line
        in the file contains a space-delimited row of cell values.

        Parameters
        ----------
        file_path : str
            Path to the bomb environment raster file.
        bomb_position_mark : int, optional
            The cell value that indicates the bomb location.
            The default is agentframework.DEFAULT_BOMB_POSITION_MARK.

        Raises
        ------
        Exception
            An exception is raised when the file cannot be read or does not
            have a bomb location specified.

        Returns
        -------
        agentframework.BombEnvironment
            A new BombEnvironment instance.

        """

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

                # Store a reference for the bomb position
                bomb_position = None

                # Read in each row and column to obtain the 2-D environment data
                for row in reader:
                    row_list = []

                    # Store a reference to the current column being processed
                    column_index = 0

                    for value in row:
                        row_list.append(value)

                        # Store the bomb position when found
                        if value == bomb_position_mark:

                            # Store the position as a tuple, as a transformation
                            # is needed after parsing the environment
                            bomb_position = (column_index, row_index)

                        # Increment the current column index
                        column_index += 1

                    # Add the environment row
                    environment_plane.append(row_list)

                    # Increment the current row index
                    row_index += 1

                # Transform the position according to the plane dimensions
                if bomb_position is not None:
                    bomb_position = Position(
                        bomb_position[0],
                        len(environment_plane) - bomb_position[1]
                    )
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
        return BombEnvironment(environment_plane, bomb_position)

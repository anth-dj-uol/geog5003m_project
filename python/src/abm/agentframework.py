#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Framework module

Provides classes used to represent agents and their data.

@author: Anthony Jarrett
"""

class Agent():

    def __init__(self, wind_model, start_position):
        self._wind_model = wind_model
        self._position = start_position

    def move(self):
        pass


class Wind():

    def __init__(self, north_percentage, east_percentage, south_percentage,
                 west_percentage):
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


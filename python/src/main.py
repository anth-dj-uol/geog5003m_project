#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bacterial Bomb Agent-Based Model

A project for the University of Leeds GEOG5003M course.

@author: Anthony Jarrett
"""

from abm import agentframework, model, view, logger


class Controller():

    def __init__(self, model, view_class):

        # Initialize model properties
        self.model = model              # Store a reference to the model
        self.view = view_class(self)    # Initialize the View

        # Display initial model view
        self._update_view()
        self._update_parameters_view()
        self.view.root.mainloop()

    def run_model(self):

        # Reset the model
        self.reset_model()

        # Run the model simulation
        particle_density_environment = self.model.run()

        # Display the particle density plot
        self.view.display(particle_density_environment, self.model.parameters.environment.bomb_position)

        # Render view
        self.view.canvas.draw()


    def reset_model(self):
        
        logger.log("Resetting model.")
        
        # Initialize the model agents
        self.model.initialize()

        # Update the view
        self._update_view()
        self.view.canvas.draw()

        logger.log("Model has been reset.\n{}", self.model)


    def _update_view(self):
        """
        Update the view with the current model state

        Returns
        -------
        None.

        """
        self.view.display(self.model.parameters.environment, self.model.parameters.environment.bomb_position)


    def load_parameters(self):
        """
        Load the parameters specified in the View.

        Returns
        -------
        None.

        """
        
        try:
            # Update the model
            self.update_parameters()
            
            # Reset current model
            self.reset_model()
            
        except Exception as e:
            self.view.show_error(e)


    def update_parameters(self):
        """
        Update the model parameters from values specified in the GUI.
        
        Will raise an exception when a parameter cannot be updated correctly.

        Returns
        -------
        None.

        """
        
        logger.log("Updating model parameters.")


        # Validate and get wind direction north percentage
        north_percentage = self._get_percentage_integer(
            self.view.north_percentage_entry.get(),
            "North wind direction %"
        )

        # Validate and get wind direction east percentage
        east_percentage = self._get_percentage_integer(
            self.view.east_percentage_entry.get(),
            "East wind direction %"
        )

        # Validate and get wind direction south percentage
        south_percentage = self._get_percentage_integer(
            self.view.south_percentage_entry.get(),
            "South wind direction %"
        )

        # Validate and get wind direction west percentage
        west_percentage = self._get_percentage_integer(
            self.view.west_percentage_entry.get(),
            "West wind direction %"
        )

        # Validate and get particle fall up percentage
        up_percentage = self._get_percentage_integer(
            self.view.up_percentage_entry.get(),
            "Upward wind direction %"
        )

        # Validate and get particle fall down percentage
        down_percentage = self._get_percentage_integer(
            self.view.down_percentage_entry.get(),
            "Downward wind direction %"
        )

        # Validate and get particle fall no change percentage
        no_change_percentage = self._get_percentage_integer(
            self.view.no_change_percentage_entry.get(),
            "No height change %"
        )

        # Validate and get number of iterations
        num_of_particles = None
        num_of_particles_text = self.view.num_of_particles_entry.get()
        try:
            num_of_particles = int(num_of_particles_text)
        except:
            raise Exception("Number of particles must be an integer")
        
        if num_of_particles < 0:
            raise Exception("Number of particles must be greater than 0")

        # Validate particle fall percentage sum
        particle_fall_sum = up_percentage + down_percentage + no_change_percentage
        if particle_fall_sum != 100:
            raise Exception(f"Particle fall percentage values must sum to 100 (currently {particle_fall_sum})")

        # Validate wind direction percentage sum
        wind_direction_sum = north_percentage + east_percentage + south_percentage + west_percentage
        if wind_direction_sum != 100:
            raise Exception(f"Wind direction percentage values must sum to 100 (currently: {wind_direction_sum})")

        # Update model parameters
        self.model.update_parameters(
            agentframework.ParticleFallSettings(
                self._get_percentage_decimal(up_percentage),
                self._get_percentage_decimal(down_percentage),
                self._get_percentage_decimal(no_change_percentage)
            ),
            agentframework.WindSettings(
                self._get_percentage_decimal(north_percentage),
                self._get_percentage_decimal(east_percentage),
                self._get_percentage_decimal(south_percentage),
                self._get_percentage_decimal(west_percentage)
            ),
            num_of_particles
        )

        # Update view parameters
        self._update_parameters_view()


    def _get_percentage_integer(self, percentage_text, entry_field_description):
        percentage = None
        if len(percentage_text) > 0:
            try:
               percentage = int(percentage_text)
            except:
                raise Exception("{} must be an integer between 0-100".format(entry_field_description))
        
        if percentage < 0 or percentage > 100:
            raise Exception("{} must be between 0-100".format(entry_field_description))

        return percentage


    def _get_percentage_decimal(self, percentage_integer):
        return percentage_integer / 100

    def _update_parameters_view(self):
        """
        Update the parameter entry fields in the View from values in the Model.

        Returns
        -------
        None.

        """

        logger.log("Updating view entry fields")
        
        # Update wind direction entry field values
        self.view._set_entry_field_value(self.view.north_percentage_entry,
                self._percent_to_int(self.model.parameters.wind_settings.north_percentage))
        self.view._set_entry_field_value(self.view.east_percentage_entry,
                self._percent_to_int(self.model.parameters.wind_settings.east_percentage))
        self.view._set_entry_field_value(self.view.south_percentage_entry,
                self._percent_to_int(self.model.parameters.wind_settings.south_percentage))
        self.view._set_entry_field_value(self.view.west_percentage_entry,
                self._percent_to_int(self.model.parameters.wind_settings.west_percentage))
        
        # Update particle fall entry field values
        self.view._set_entry_field_value(self.view.up_percentage_entry,
                self._percent_to_int(self.model.parameters.particle_fall_settings.up_percentage))
        self.view._set_entry_field_value(self.view.down_percentage_entry,
                self._percent_to_int(self.model.parameters.particle_fall_settings.down_percentage))
        self.view._set_entry_field_value(self.view.no_change_percentage_entry,
                self._percent_to_int(self.model.parameters.particle_fall_settings.no_change_percentage))

        # Update number of particles entry field values
        self.view._set_entry_field_value(self.view.num_of_particles_entry,
                                   self.model.parameters.num_of_particles)


    def _percent_to_int(self, value):
        return int(value * 100)



def main():
    logger.log("Starting Bacterial Bomb Agent-Based Model...")

    # Start the GUI program
    Controller(model.Model(), view.View)

# Run the main function when invoked as a script
if __name__ == '__main__':
    main()
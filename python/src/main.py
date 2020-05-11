#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bacterial Bomb Agent-Based Model

A project for the University of Leeds GEOG5003M course.

@author: Anthony Jarrett
"""

from abm import model, view, logger


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
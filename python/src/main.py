#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bacterial Bomb Agent-Based Model

A project for the University of Leeds GEOG5003M course.

@author: Anthony Jarrett
"""

import tkinter
from abm import agentframework, model, view, logger

DEFAULT_SAVE_FILE_EXTENSION = ".raster"

class Controller():
    """
    The Controller class coordinates communication between the given Model
    and View. It handles events that are triggered from the View and also
    propagates changes that occur in the Model.
    
    Public Methods:
        
        run_model - run the model simulation
        
        save_model - save model simulation result as a raster text file

        load_parameters - load the model parameters from the view

        update_parameters - updates the model parameters from the view values
    """

    def __init__(self, model, view_class):
        """
        Create a new Controller instance.

        Parameters
        ----------
        model : agentframework.Model
            The agent-based model.
        view_class : view.View
            The view that can visualize the agent-based model.

        Returns
        -------
        None.

        """

        logger.log("Instantiating a Controller.")

        # Initialize model properties
        self.model = model              # Store a reference to the model
        self.view = view_class(self)    # Initialize the View

        # Display initial model view
        self._update_view()
        self._update_parameters_view()
        self.view.root.mainloop()


    def run_model(self):
        """
        Run the model with its current parameters.
        
        This will display the model simulation results in the attached View.

        Returns
        -------
        None.

        """

        # Reset the model
        self._reset_model()

        # Run the model simulation
        particle_density_environment = self.model.run()

        # Display the particle density plot
        self.view.display(
            particle_density_environment,
            self.model.parameters.environment.bomb_position
        )

        # Render view
        self.view.canvas.draw()


    def save_model(self):
        """
        Prompt the user with a file save dialog.
        
        The selected file will have the current model simulation 
        particle density raster written in text format.

        Returns
        -------
        None.

        """

        # Check that there exists a result to save
        if self.model.result_environment is None:
            self.view.alert("The model must be run before saving the result.")
        else:
            # Ask user for the new file location
            logger.log("Prompting user for file location.")
            file = tkinter.filedialog.asksaveasfile(
                defaultextension=DEFAULT_SAVE_FILE_EXTENSION)
            if file is not None:

                # Write the environment as text
                logger.log("Writing result environment contents...")
                self._save_environment_as_text(file, self.model.result_environment)
                logger.log("Completed file write as text.")

                # Display a success message
                self.view.alert("File saved successfully.", is_error=False)


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
            self._reset_model()

            return True
            
        except Exception as e:
            self.view.alert(e)

        return False


    def update_parameters(self):
        """
        Update the model parameters from values specified in the View.
        
        This method will raise an exception when a parameter cannot be updated
        correctly.

        Returns
        -------
        success : bool
            Returns True if parameters are successfully updated, otherwise
            returns False

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

        # Validate and get maximum number of iterations
        max_num_of_iterations = None
        max_num_of_iterations_text = self.view.max_num_of_iterations_entry.get()
        try:
            max_num_of_iterations = int(max_num_of_iterations_text)
        except:
            raise Exception("Max number of iterations must be an integer")
        
        # Ensure that the value is greater than or equal to 0
        if max_num_of_iterations is not None and max_num_of_iterations < 0:
            raise Exception("Max number of iterations must be greater than 0")

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

        # Validate and get number of particles
        num_of_particles = None
        num_of_particles_text = self.view.num_of_particles_entry.get()
        try:
            num_of_particles = int(num_of_particles_text)
        except:
            raise Exception("Number of particles must be an integer")

        # Ensure that the value is greater than or equal to 0
        if num_of_particles is not None and num_of_particles < 0:
            raise Exception("Number of particles must be greater than 0")

        # Validate and get building height in metres
        building_height_metres = None
        building_height_metres_text = self.view.building_height_metres_entry.get()
        try:
            building_height_metres = int(building_height_metres_text)
        except:
            raise Exception("Building height must be an integer")

        # Ensure that the value is greater than or equal to 0
        if building_height_metres is not None and building_height_metres < 0:
            raise Exception("Building height must be greater than 0")

        # Validate particle fall percentage sum
        particle_fall_sum = up_percentage + down_percentage + no_change_percentage
        if particle_fall_sum is not None and particle_fall_sum != 100:
            raise Exception(f"Particle fall percentage values must sum to 100 (currently {particle_fall_sum})")

        # Validate wind direction percentage sum
        wind_direction_sum = north_percentage + east_percentage + \
            south_percentage + west_percentage
        if wind_direction_sum != 100:
            raise Exception(f"Wind direction percentage values must sum to 100 (currently: {wind_direction_sum})")

        # Update model parameters
        self.model.update_parameters(
            agentframework.ParticleFallSettings(
                up_percentage,
                down_percentage,
                no_change_percentage
            ),
            agentframework.WindSettings(
                north_percentage,
                east_percentage,
                south_percentage,
                west_percentage
            ),
            num_of_particles,
            building_height_metres,
            max_num_of_iterations
        )

        # Update view parameters
        self._update_parameters_view()


    def _reset_model(self):
        """
        Reset the current model state.
        
        This method will recreate all configured agents and update the View.

        Returns
        -------
        None.

        """

        logger.log("Resetting model.")
        
        # Initialize the model agents
        self.model.initialize()

        # Update the view
        self._update_view()
        self.view.canvas.draw()

        logger.log("Model has been reset.\n{}", self.model)


    def _save_environment_as_text(self, file, environment):
        """
        Write the provided environment to a file.
        
        This method will create a raster file in text format, where each line
        contains a space-delimited list of cell integer values representing
        particle density. The cell value equals the number of particles that
        landed in that cell.

        Parameters
        ----------
        file : file object
            The file that will be written to.
        environment : agentframework.Environment
            The environment that will be written to the file.

        Returns
        -------
        None.

        """

        # Iterate through each row in the environment
        for row in environment.plane:

            # Iterate through each cell in the environment
            for column in row:

                # Write out the cell value
                file.write(str(column) + " ")
            
            # Complete the row
            file.write("\n")


    def _update_view(self):
        """
        Update the view with the current model state

        Returns
        -------
        None.

        """

        self.view.display(self.model.parameters.environment, self.model.parameters.environment.bomb_position)


    def _get_percentage_integer(self, percentage_text, entry_field_description):
        """
        Get the integer percentage value.
        
        This method will return an integer percentage value between 0-100 that
        is read from the specified string. An exception is raised if the
        provided string value cannot be interpreted as a percentage integer.

        Parameters
        ----------
        percentage_text : str
            The integer percentage text value.
        entry_field_description : str
            The message used if an error occurs.

        Raises
        ------
        Exception
            Occurs when the string value cannot be interpreted as a percentage
            integer value.

        Returns
        -------
        percentage : int
            The percentage value stored as an integer between 0-100.

        """
        # Set the default percentage value as None to indicate no change
        percentage = None
        
        # Set the error message
        error_message = "{} must be an integer from 0-100".format(entry_field_description)

        # Check if the percentage text contains a value
        if len(percentage_text) > 0:
            try:
                # Attempt to parse an integer from the text value
                percentage = int(percentage_text)

                # Ensure that the percentage value is between 0 and 100
                if percentage < 0 or percentage > 100:
                    raise Exception(error_message)
            except:
                raise Exception(error_message)
        else:
            # Return an error if a value is not present
            raise Exception(error_message)

        # Return the percentage integer value
        return percentage


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
                self.model.parameters.wind_settings.north_percentage)
        self.view._set_entry_field_value(self.view.east_percentage_entry,
                self.model.parameters.wind_settings.east_percentage)
        self.view._set_entry_field_value(self.view.south_percentage_entry,
                self.model.parameters.wind_settings.south_percentage)
        self.view._set_entry_field_value(self.view.west_percentage_entry,
                self.model.parameters.wind_settings.west_percentage)

        # Update building height entry field value
        self.view._set_entry_field_value(self.view.max_num_of_iterations_entry,
                                   self.model.parameters.max_num_of_iterations)

        # Update particle fall entry field values
        self.view._set_entry_field_value(self.view.up_percentage_entry,
                self.model.parameters.particle_fall_settings.up_percentage)
        self.view._set_entry_field_value(self.view.down_percentage_entry,
                self.model.parameters.particle_fall_settings.down_percentage)
        self.view._set_entry_field_value(self.view.no_change_percentage_entry,
                self.model.parameters.particle_fall_settings.no_change_percentage)

        # Update number of particles entry field value
        self.view._set_entry_field_value(self.view.num_of_particles_entry,
                                   self.model.parameters.num_of_particles)

        # Update building height entry field value
        self.view._set_entry_field_value(self.view.building_height_metres_entry,
                                   self.model.parameters.building_height_metres)



def main():
    """
    Launch the program GUI.
    
    This function will instantiate the Model-View-Controller pattern.

    Returns
    -------
    None.

    """
    
    # Enable logging
    logger.configure(True)

    # Start the GUI program
    logger.log("Starting Bacterial Bomb Agent-Based Model...")
    Controller(model.Model(), view.View)



# Run the main function when invoked as a script
if __name__ == '__main__':
    main()
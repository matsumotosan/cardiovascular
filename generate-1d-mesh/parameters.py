#!/usr/bin/env python


class Parameters():
    """ The Parameter class stores the input parameters for a 1D mesh generation.
    """
    def __init__(self):

        self.boundary_surfaces_dir = None
        self.output_directory = None
        self.centerlines_input_file = None
        self.centerlines_output_file = None
        self.compute_centerlines = True
        self.surface_model = None
        self.uniform_bc = False
        self.uniform_material = True
        self.wall_properties_input_file = None
        self.wall_properties_output_file = None

        # Physical parameters.
        self.c1 = 0.0e7
        self.c2 = -22.5267
        self.c3 = 2.65e5
        self.density = 1.055
        self.mattype = "OLUFSEN"
        self.viscosity = 0.04


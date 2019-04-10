#!/usr/bin/env python

""" 
This module provides the interface to the modules creating a 1D mesh used for 1D simulations. 

"""
import argparse
import sys
from os import path

from manage import get_logger_name, init_logging
from parameters import Parameters
from centerlines import *
from mesh import *
from utils import write_polydata, read_polydata

logger = logging.getLogger(get_logger_name())

class Args(object):
    """ This class defines the command line arguments to the generate-1d-mesh script.
    """
    PREFIX = "--"
    BOUNDARY_SURFACE_DIR = "boundary_surfaces_directory"
    CENTERLINE_INPUT_FILE = "centerlines_input_file"
    CENTERLINE_OUTPUT_FILE = "centerlines_output_file"
    COMPUTE_CENTERLINES = "compute_centerlines"
    COMPUTE_MESH = "compute_mesh"
    INFLOW_INPUT_FILE = "inflow_input_file"
    MESH_OUTPUT_FILE = "mesh_output_file"
    OUTFLOW_BC_TYPE = "outflow_bc_type"
    OUTPUT_DIRECTORY = "output_directory"
    SOLVER_OUTPUT_FILE = "solver_output_file"
    SURFACE_MODEL = "surface_model"
    UNIFORM_BC = "uniform_bc"
    WALL_PROPERTIES_INPUT_FILE = "wall_properties_input_file"
    WALL_PROPERTIES_OUTPUT_FILE = "wall_properties_output_file"
    WRITE_MESH_FILE = "write_mesh_file"
    WRITE_SOLVER_FILE = "write_solver_file"
    
def cmd(name):
    """ Create an argparse command argument.
    """
    return Args.PREFIX + name.replace("_", "-")

def parse_args():
    """ Parse command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(cmd(Args.BOUNDARY_SURFACE_DIR), 
      help="Directory containing the boundary (inlet/outlet) surface files")

    parser.add_argument(cmd(Args.CENTERLINE_INPUT_FILE), 
      help="The name of the file to read centerline geometry from.")

    parser.add_argument(cmd(Args.CENTERLINE_OUTPUT_FILE), 
      help="The name of the file to write centerline geometry to.")

    parser.add_argument(cmd(Args.COMPUTE_CENTERLINES), const=True, nargs='?', default=False, 
      help="If given or value is set to 1 then compute centerlines.")

    parser.add_argument(cmd(Args.COMPUTE_MESH), const=True, nargs='?', default=False, 
      help="If given or value is set to 1 then compute a mesh from centerlines..")

    parser.add_argument(cmd(Args.INFLOW_INPUT_FILE), 
      help="The name of the file to read inflow data from.")

    parser.add_argument(cmd(Args.MESH_OUTPUT_FILE), 
      help="The name of the file to write the mesh to.")

    parser.add_argument(cmd(Args.OUTFLOW_BC_TYPE), 
      help="The output boundary condition type (RESISTANCE, RCR).")

    parser.add_argument(cmd(Args.OUTPUT_DIRECTORY), required=True, 
      help="The directory where output files are written.")

    parser.add_argument(cmd(Args.SOLVER_OUTPUT_FILE), 
      help="The name of the file to write the solver input to.")

    parser.add_argument(cmd(Args.SURFACE_MODEL), 
      help="The surface model used to compute centerlines.")

    parser.add_argument(cmd(Args.UNIFORM_BC),
      help = "If set to (true,1,on) then read BC files")

    parser.add_argument(cmd(Args.WALL_PROPERTIES_INPUT_FILE), 
      help = "The name of the file read surface wall material properties from.")

    parser.add_argument(cmd(Args.WALL_PROPERTIES_OUTPUT_FILE), 
      help = "The name of the file write grouped wall material properties to.")

    parser.add_argument(cmd(Args.WRITE_MESH_FILE), const=True, nargs='?', default=False, 
      help="If given or value is set to 1 then write a mesh file..")

    parser.add_argument(cmd(Args.WRITE_SOLVER_FILE), const=True, nargs='?', default=False, 
      help="If given or value is set to 1 then write a solver file..")

    return parser.parse_args(), parser.print_help

def set_parameters(**kwargs):
    """ Set the values of parameters input from the command line.
    """
    logger.info("Parse arguments ...")
    print(kwargs)

    ## Create a Parameters object to store parameters.
    params = Parameters()

    ## Process arguments.
    #
    true_values = ["on", "true", "1"]

    if kwargs.get(Args.BOUNDARY_SURFACE_DIR): 
        params.boundary_surfaces_dir = kwargs.get(Args.BOUNDARY_SURFACE_DIR)
        logger.info("Surface directory: %s" % params.boundary_surfaces_dir)
        if not os.path.exists(params.boundary_surfaces_dir):
            logger.error("The surface directory '%s' was not found." % params.boundary_surfaces_dir)
            return None

    if kwargs.get(Args.CENTERLINE_INPUT_FILE):
        params.centerlines_input_file = kwargs.get(Args.CENTERLINE_INPUT_FILE)
        logger.info("Centerlines input file: %s" % params.centerlines_input_file)
        if not os.path.exists(params.centerlines_input_file):
            logger.error("The centerlines input file '%s' was not found." % params.centerlines_input_file)
            return None

    if kwargs.get(Args.CENTERLINE_OUTPUT_FILE): 
        params.centerlines_output_file = kwargs.get(Args.CENTERLINE_OUTPUT_FILE)
        logger.info("Centerlines output file: %s" % params.centerlines_output_file)
        if not os.path.exists(params.centerlines_output_file):
            logger.error("The centerlines output file '%s' was not found." % 
              params.centerlines_output_file)
            return None

    # The 'compute_centerlines' parameter is set to True if the COMPUTE_CENTERLINES 
    # argument is given with no value. Otherwise it is set to the value given.
    params.compute_centerlines = (kwargs.get(Args.COMPUTE_CENTERLINES) == True) or \
      (kwargs.get(Args.COMPUTE_CENTERLINES) in true_values)
    logger.info("Compute centerlines: %s" % params.compute_centerlines) 

    # The 'compute_mesh' parameter is set to True if the COMPUTE_MESH 
    # argument is given with no value. Otherwise it is set to the value given.
    params.compute_mesh = (kwargs.get(Args.COMPUTE_MESH) == True) or \
      (kwargs.get(Args.COMPUTE_MESH) in true_values)

    if kwargs.get(Args.INFLOW_INPUT_FILE):
        params.inflow_input_file = kwargs.get(Args.INFLOW_INPUT_FILE)
        logger.info("Inflow input file: %s" % params.inflow_input_file)
        if not os.path.exists(params.surface_model):
            logger.error("The inflow input file '%s' was not found." % params.inflow_input_file) 
            return None

    params.output_directory = kwargs.get(Args.OUTPUT_DIRECTORY)
    if not os.path.exists(params.output_directory):
        logger.error("The output directory '%s' was not found." % params.output_directory)
        return None

    if kwargs.get(Args.MESH_OUTPUT_FILE):
        params.mesh_output_file = kwargs.get(Args.MESH_OUTPUT_FILE)
        if not os.path.exists(params.mesh_output_file):
            logger.info("Mesh output file: %s" % params.mesh_output_file)

    if kwargs.get(Args.OUTFLOW_BC_TYPE):
        bc_type = kwargs.get(Args.OUTFLOW_BC_TYPE).lower()
        if not bc_type in self.outflow_bc_types:
            logger.error("Unknown BC type '%s'." % bc_type) 
            return None
        params.outflow_bc_type = bc_type
        params.outflow_bc_file = self.outflow_bc_types[bc_type]
        logger.info("Outflow bc type: %s" % params.outflow_bc_type)
        logger.info("Outflow bc file: %s" % params.outflow_bc_file)

    if kwargs.get(Args.SOLVER_OUTPUT_FILE):
        params.solver_output_file = kwargs.get(Args.SOLVER_OUTPUT_FILE)
        logger.info("Solver output file: %s" % params.solver_output_file)

    if kwargs.get(Args.SURFACE_MODEL):
        params.surface_model = kwargs.get(Args.SURFACE_MODEL)
        logger.info("Surface model: %s" % params.surface_model)
        if not os.path.exists(params.surface_model):
            logger.error("The surface model file '%s' was not found." % params.surface_model)
            return None

    if kwargs.get(Args.WALL_PROPERTIES_INPUT_FILE):
        params.wall_properties_input_file = kwargs.get(Args.WALL_PROPERTIES_INPUT_FILE)
        logger.info("Wall properties input file: %s" % params.wall_properties_input_file)
        if not os.path.exists(params.wall_properties_input_file):
            logger.error("The wall properties input file '%s' was not found." % 
              params.wall_properties_input_file)
            return None
        params.uniform_material = False
        logger.info("Wall properties are not uniform.")
    else:
        logger.info("Wall properties are uniform.")

    if kwargs.get(Args.WALL_PROPERTIES_OUTPUT_FILE):
        params.wall_properties_output_file = kwargs.get(Args.WALL_PROPERTIES_OUTPUT_FILE)
        logger.info("Wall properties output file: %s" % params.wall_properties_output_file)

    # The 'write_mesh_file' parameter is set to True if the WRITE_MESH_FILE
    # argument is given with no value. Otherwise it is set to the value given.
    params.write_mesh_file = (kwargs.get(Args.WRITE_MESH_FILE) == True) or \
      (kwargs.get(Args.WRITE_MESH_FILE) in true_values)
    logger.info("Write mesh file: %s" % params.write_mesh_file)

    # The 'write_solver_file' parameter is set to True if the WRITE_SOLVER_FILE
    # argument is given with no value. Otherwise it is set to the value given.
    params.write_solver_file = (kwargs.get(Args.WRITE_SOLVER_FILE) == True) or \
      (kwargs.get(Args.WRITE_SOLVER_FILE) in true_values)
    logger.info("Write solver file: %s" % params.write_solver_file)


    ## Check for argument consistency.
    #
    if params.compute_centerlines and params.centerlines_input_file: 
        logger.error("Both compute centerlines and read centerlines are given.")
        return None

    if params.wall_properties_input_file and not params.wall_properties_output_file: 
        logger.error("If a wall properties input file is given then a wall properties output file must also be given.")
        return None

    return params 

def read_centerlines(params):
    """ Read centerlines for a surface model from a file.
    """
    centerlines = Centerlines()
    centerlines.branch_geometry = read_polydata(params.centerlines_input_file)

    logger.info("Read centerlines from the file: %s", params.centerlines_input_file) 
    logger.info("   Number of points: %d ", centerlines.branch_geometry.GetNumberOfPoints())
    logger.info("   Number of cells: %d ", centerlines.branch_geometry.GetNumberOfCells())
    logger.info("   Number of arrays: %d", centerlines.branch_geometry.GetCellData().GetNumberOfArrays())

    return centerlines

def compute_centerlines(params):
    """ Compute the centerlines for a surface model.
    """

    ## Check input parameters.
    #
    if not params.surface_model:
        logger.error("No surface model has been specified.")
        return

    if not params.centerlines_output_file:
        logger.error("No centerlines output file has been specified.")
        return

    # Create Centerlines object that encapsulats centerline calculations. 
    centerlines = Centerlines()

    # Extract centerlines.
    centerlines.extract_center_lines(params)

    # Split and group centerlines along branches. 
    centerlines.extract_branches(params)

    # Write the centerlines branches to a file.
    if centerlines.branch_geometry:
        write_polydata(params.centerlines_output_file, centerlines.branch_geometry)

    return centerlines

def run(**kwargs):
    """ Execute the 1D mesh generation using passed parameters.
    """

    ## Set input parameters.
    params = set_parameters(**kwargs)
    if not params:
        return False

    centerlines = None 

    ## Extract surface centerlines.
    if params.compute_centerlines:
        centerlines = compute_centerlines(params)

    ## Read surface centerlines.
    elif params.centerlines_input_file:
        centerlines = read_centerlines(params)

    if not centerlines:
        logger.error("No centerlines calculated or read in.")
        sys.exit(1)

    ## Generate a 1D mesh.
    mesh = Mesh()
    mesh.generate(params, centerlines)

    return True

if __name__ == '__main__':
    init_logging()
    args, print_help = parse_args()
    if not run(**vars(args)):
        print_help()
        sys.exit(1)

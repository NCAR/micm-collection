#!/usr/bin/python3
from shutil import copyfile as cp
import argparse

# needs to check the python v3 is running

# Parse arguments.  They override those defaults specified in the argument parser
#default_preprocessor_server = "www.acom.ucar.edu"

parser = argparse.ArgumentParser(
                      description='Distribute Fortran from a particular directory into MICM_chemistry',
                      formatter_class=argparse.ArgumentDefaultsHelpFormatter
                      )


parser.add_argument('-source_dir_kinetics', type=str, required=True,
                    help='Source directory containing kinetics FORTRAN code')

parser.add_argument('-target_dir_kinetics', type=str, default="../MICM_chemistry/src", 
                    help='Where the code should be placed')

parser.add_argument('-target_host_model_mechanism_location', type=str, default="../MusicBox_host/",
                    help='Where to place the molecular information for the host model')

parser.add_argument('-target_host_model_environmental_conditions_dir', type=str, default="../MusicBox_host/data/",
                    help='Where to place the molecular information for the host model')

parser.add_argument('-source_environmental', type=str, default="./environmental_conditions/boulder.complete.nc",
                    help='Where to place the molecular information for the host model')




args = parser.parse_args()
print(args)

cp( args.source_dir_kinetics + "/rate_constants_utility.F90", args.target_dir_kinetics     + "/kinetics/rate_constants_utility.F90" )
cp( args.source_dir_kinetics + "/factor_solve_utilities.F90", args.target_dir_kinetics     + "/kinetics/factor_solve_utilities.F90" )
cp( args.source_dir_kinetics + "/kinetics_utilities.F90"    , args.target_dir_kinetics     + "/kinetics/kinetics_utilities.F90" )
cp( args.source_dir_kinetics + "/mechanism.json"            , args.target_host_model_mechanism_location + "molec_info.json" )
cp( args.source_environmental         , args.target_host_model_environmental_conditions_dir + "env_conditions.nc" )

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
                    help='Source directory containing preprocessed kinetics FORTRAN code and mechanism json')

parser.add_argument('-target_dir_chemistry', type=str, default="../MICM_chemistry/src",
                    help='Chemistry module source code folder. Kinetics code will be placed in the target_dir_chemistry\kinetics folder')

parser.add_argument('-target_dir_host_model', type=str, default="../MusicBox_host/",
                    help='Host model root directory. The chemical mechanism description will be placed here as molec.json')

parser.add_argument('-source_file_environmental_conditions', type=str, default="./environmental_conditions/boulder.complete.nc",
                    help='Path to the environmental conditions NetCDF file.')

parser.add_argument('-target_dir_environmental_conditions', type=str, default="../MusicBox_host/data/",
                    help='Host model data directory. Environmental conditions will be placed here as env_conditions.nc')



args = parser.parse_args()
print(args)

cp( args.source_dir_kinetics + "/rate_constants_utility.F90", args.target_dir_chemistry  + "/kinetics/rate_constants_utility.F90" )
cp( args.source_dir_kinetics + "/factor_solve_utilities.F90", args.target_dir_chemistry  + "/kinetics/factor_solve_utilities.F90" )
cp( args.source_dir_kinetics + "/kinetics_utilities.F90"    , args.target_dir_chemistry  + "/kinetics/kinetics_utilities.F90" )
cp( args.source_dir_kinetics + "/mechanism.json"            , args.target_dir_host_model + "molec_info.json" )
cp( args.source_dir_environmental_conditions, args.target_dir_environmental_conditions + "env_conditions.nc" )

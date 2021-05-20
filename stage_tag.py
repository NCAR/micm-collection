#!/usr/bin/python3

# Copyright (C) 2020 National Center for Atmospheric Research
# SPDX-License-Identifier: Apache-2.0

from shutil import copyfile as cp
import argparse

# needs to check the python v3 is running

# Parse arguments.  They override those defaults specified in the argument parser
#default_preprocessor_server = "www.acom.ucar.edu"

parser = argparse.ArgumentParser(
                      description='Distribute Fortran from a particular directory into the MICM source folder',
                      formatter_class=argparse.ArgumentDefaultsHelpFormatter
                      )


parser.add_argument('-source_dir_kinetics', type=str, required=True,
                    help='Source directory containing preprocessed kinetics FORTRAN code')

parser.add_argument('-target_dir_chemistry', type=str, default="../micm/src/preprocessor_output/",
                    help='Chemistry module source code folder for preprocessor output. Kinetics code will be placed here.')

parser.add_argument('-source_file_environmental_conditions', type=str, default="./environmental_conditions/boulder.complete.nc",
                    help='Path to the environmental conditions NetCDF file.')

parser.add_argument('-target_dir_data', type=str, default="../../build/data/",
                    help='Host model data directory. Environmental conditions will be placed here as env_conditions.nc')



args = parser.parse_args()
print(args)

cp( args.source_dir_kinetics + "/rate_constants_utility.F90", args.target_dir_chemistry  + "rate_constants_utility.F90" )
cp( args.source_dir_kinetics + "/factor_solve_utilities.F90", args.target_dir_chemistry  + "factor_solve_utilities.F90" )
cp( args.source_dir_kinetics + "/kinetics_utilities.F90"    , args.target_dir_chemistry  + "kinetics_utilities.F90" )
cp( args.source_file_environmental_conditions,                args.target_dir_data       + "env_conditions.nc" )

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


parser.add_argument('-source_dir', type=str, required=True,
                    help='Source directory containing kinetics FORTRAN code')

parser.add_argument('-target_dir', type=str, default="../MICM_chemistry/src", 
                    help='Where the code should be placed')

parser.add_argument('-host_model_dir', type=str, default="../MusicBox_host/",
                    help='Where to place the molecular information for the host model')



args = parser.parse_args()
print(args)

cp( args.source_dir + "/rate_constants_utility.F90", args.target_dir     + "/kinetics/rate_constants_utility.F90" )
cp( args.source_dir + "/factor_solve_utilities.F90", args.target_dir     + "/kinetics/factor_solve_utilities.F90" )
cp( args.source_dir + "/kinetics_utilities.F90"    , args.target_dir     + "/kinetics/kinetics_utilities.F90" )
cp( args.source_dir + "/mechanism.json"            , args.host_model_dir + "molec_info.json" )

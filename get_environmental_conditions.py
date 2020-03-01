#!/usr/bin/python3
import argparse
import os.path as path
import sys
from ftplib import FTP

# needs to check the python v3 is running

# Parse arguments.  They override those defaults specified in the argument parser
parser = argparse.ArgumentParser(
                    description='Collect Environmental Conditions File.',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                    )

parser.add_argument('-environmental_conditions_file', type=str, default="f.e21.FW2000climo.f09_f09_mg17.n03.cam.h2.0001-01-01-00000.nc",
                    help='Name of environmental conditions file at ftp://ftp.acom.ucar.edu/')
parser.add_argument('-path_to_environmental_conditions', type=str, default="./environmental_conditions/",
                    help='Name of environmental conditions file at ftp://ftp.acom.ucar.edu/')

args = parser.parse_args()


print('retrieve environmental conditions file:')
print(args.environmental_conditions_file)

target_path_file = args.path_to_environmental_conditions+args.environmental_conditions_file
print("Target path and file " + target_path_file)

target_file_exists = path.isfile(target_path_file)

if target_file_exists:
  print("Target file exists " + str(target_file_exists))
  sys.exit('Exiting ')
else:
  with FTP('ftp.acom.ucar.edu') as ftp:
    ftp.login(user='anonymous', passwd='anonymous')
    ftp.cwd('micm_environmental_conditions')
    ftp.retrbinary('RETR '+ args.environmental_conditions_file, open(args.path_to_environmental_conditions+args.environmental_conditions_file, 'wb').write)
    ftp.quit

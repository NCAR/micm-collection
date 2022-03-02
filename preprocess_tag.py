#!/usr/bin/python3

# Copyright (C) 2020 National Center for Atmospheric Research
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
from os.path import abspath
import sys
from ftplib import FTP
from http.client import HTTPSConnection
import json
import requests

# Parse arguments.  They override those defaults specified in the argument parser
default_preprocessor_server = "www.acom.ucar.edu"
parser = argparse.ArgumentParser(
                    description='Solve a mechanism tag using the sparse solver branch of MusicBox/MICM.',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                    )
parser.add_argument('-c','--configuration-file-path', type=abspath, default=abspath("config.json"),
                    help='path to the mechanism configuration file')
parser.add_argument('-p','--preprocessor', type=str, default=default_preprocessor_server,
                    help='url of preprocessor')
args = parser.parse_args()

# Connection to the preprocessor location
processor_location = args.preprocessor
preprocessor_con = HTTPSConnection(processor_location, 3000)

# combine mechanism configuration into single json object
mechanism_json = json.loads('{}')
configuration_folder = os.path.split(args.configuration_file_path)[0];
with open(args.configuration_file_path, 'r') as configuration_file:
  configuration_json = json.load(configuration_file)
  for file_name in configuration_json['camp-files']:
      with open(os.path.join(configuration_folder, file_name), 'r') as mechanism_file:
          mechanism_json[file_name] = json.load(mechanism_file)

#
#    Turn mechanism.json into fortran code!
#
# get preprocessed code
res = requests.post("http://"+args.preprocessor+"/constructJacobian/", auth=('user', 'pass'), json=mechanism_json)
if res.status_code != 200 : exit()
jacobian = res.text
jacobian_json = json.loads(jacobian)

# write preprocessed code to output folder
output_folder = os.path.join(configuration_folder, 'output')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
with open(os.path.join(output_folder, 'kinetics_utilities.F90'), 'w') as k_file:
  k_file.write(jacobian_json["kinetics_utilities_module"])
with open(os.path.join(output_folder, 'rate_constants_utility.F90'), 'w') as r_file:
  r_file.write(jacobian_json["rate_constants_utility_module"])
with open(os.path.join(output_folder, 'factor_solve_utilities.F90'), 'w') as f_file:
  f_file.write(jacobian_json["factor_solve_utilities_module"])


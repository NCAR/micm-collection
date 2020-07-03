#!/usr/bin/python3
import argparse
import os
import sys
from ftplib import FTP

from http.client import HTTPSConnection
import json

import requests

headers = {
        "cache-control": "no-cache",
        "x-dreamfactory-api-key": "YOUR_API_KEY"
}

userAndPass = bytes('username' + ':' + 'password', "utf-8") #convert to utf-8


# needs to check that ssl is enabled
#import socket
#socket.ssl
# expect something like<function ssl at 0x4038b0>

# needs to check the python v3 is running

# Parse arguments.  They override those defaults specified in the argument parser
default_preprocessor_server = "www.acom.ucar.edu"
parser = argparse.ArgumentParser(
                    description='Solve a mechanism tag using the sparse solver branch of MusicBox/MICM.',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                    )
parser.add_argument('-mechanism_source_path', type=str, required=True,
                    help='path to mechanism store location of tag')
parser.add_argument('-preprocessor', type=str, default=default_preprocessor_server,
                    help='url of preprocessor')
parser.add_argument('-overwrite', type=bool, default=False,
                    help='overwrite the target_dir')
 


args = parser.parse_args()

mechanism_source_path = args.mechanism_source_path+"/"

with open(mechanism_source_path+'this_configuration', 'w') as configuration_filehandle:
  configuration_filehandle.write(str(args))

# Connection to the preprocessor location
processor_location = args.preprocessor
preprocessor_con = HTTPSConnection(processor_location, 3000)

# check connection status:
#exception http.client.HTTPException
#  The base class of the other exceptions in this module. It is a subclass of Exception.
#exception http.client.NotConnected
#  A subclass of HTTPException.

#
with open(mechanism_source_path+'source_mechanism.json', 'r') as json_mechanism_file:
  mech_json = json.load(json_mechanism_file)

#
#    Turn mechanism.json into fortran code!
#
# preprocessor headers
headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-type': 'application/json', 'Accept': 'text/plain' }

# Construct factor_solve_utilities.F90, kinetics_utilities.F90, rate_constants_utilities.F90
#mech_json_string = json.dumps(mech_json)
#print(mech_json_string)
version = mech_json["mechanism"]["version"]
res = requests.post("http://"+args.preprocessor+"/constructJacobian/v"+version, auth=('user', 'pass'), json=mech_json)
#print(res.status_code)
#print(res.encoding)
#print(res.json)
if res.status_code != 200 : exit()
jacobian = res.text
jacobian_json = json.loads(jacobian)
#print(jacobian_json)

#service = '/preprocessor/constructJacobian'
#preprocessor_con.request('POST', service, mechanism, headers=headers)
#res = preprocessor_con.getresponse()
#jacobian = res.read()  
#jacobian_json = json.loads(jacobian)


# write factor_solve_utilities.F90, kinetics_utilities.F90, rate_constants_utilities.F90
with open(mechanism_source_path+'kinetics_utilities.F90', 'w') as k_file:
  k_file.write(jacobian_json["kinetics_utilities_module"])

with open(mechanism_source_path+'rate_constants_utility.F90', 'w') as r_file:
  r_file.write(jacobian_json["rate_constants_utility_module"])

with open(mechanism_source_path+'factor_solve_utilities.F90', 'w') as f_file:
  f_file.write(jacobian_json["factor_solve_utilities_module"])


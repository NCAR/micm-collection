#!/usr/bin/python3
import argparse
import os
import sys

from http.client import HTTPSConnection
import json

# needs to check that ssl is enabled
#import socket
#socket.ssl
# expect something like<function ssl at 0x4038b0>

# needs to check the python v3 is running

# Parse arguments.  They override those defaults specified in the argument parser
default_tag = 255
default_tag_server = "cafe-devel.acom.ucar.edu"
default_preprocessor_server = "www.acom.ucar.edu"
default_configured_tag_location = str(default_tag)
parser = argparse.ArgumentParser(description='Solve a mechanism tag using the sparse solver branch of MusicBox/MICM.')
parser.add_argument('-tag_id', type=int, default=default_tag,
                    help='Tag number for Chemistry Cafe mechanism tag')
parser.add_argument('-tag_server', type=str, default=default_tag_server,
                    help='url of tag server')
parser.add_argument('-preprocessor', type=str, default=default_preprocessor_server,
                    help='url of preprocessor')
parser.add_argument('-target_dir', type=str, default=default_configured_tag_location,
                    help='url of preprocessor')
parser.add_argument('-git_user', metavar='git_user', type=str, default="",
                    help='user name for github access')
parser.add_argument('-git_pw', metavar='git_pw', type=str, default="",
                    help='password for user on github')

args = parser.parse_args()

outpath = "configured_tags/"+args.target_dir+"/"

# make target_tag_location director
try:
  os.mkdir(outpath)
except Exception as e:
  print("Directory "+args.target_dir+" already exists.  Delete it if you want new data.")
  print("Exception: "+str(3))
  sys.exit(1)


with open(outpath+'this_configuration', 'w') as configuration_filehandle:
  configuration_filehandle.write(str(args))

# Connection to the Cafe
mechanism_store_location = args.tag_server
mechanism_con = HTTPSConnection(mechanism_store_location)

# Connection to the preprocessor location
processor_location = args.preprocessor
preprocessor_con = HTTPSConnection(processor_location)

# check connection status:
#exception http.client.HTTPException
#  The base class of the other exceptions in this module. It is a subclass of Exception.
#exception http.client.NotConnected
#  A subclass of HTTPException.

# Simple authorization.  With this there could be 'man-in-middle'.
userAndPass = bytes('username' + ':' + 'password', "utf-8") #convert to utf-8
headers = { 'Authorization' : 'Basic %s' %  userAndPass }

#
#    Collect Tag and preprocess it
#
# Get tag from server
mechanism_con.request('GET', '/node_processes/tags.php?action=return_tag&tag_id='+str(args.tag_id), headers=headers)
res = mechanism_con.getresponse()
# Check status

# Collect the data, write a copy to file
# error testing?
mechanism = res.read()  
mech_json = json.loads(mechanism)
with open(outpath+'mechanism.json', 'w') as mechanism_outfile:
  json.dump(mech_json, mechanism_outfile, indent=2)


#
#    Turn mechanism.json into fortran code!
#
# preprocessor headers
headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-type': 'application/json', 'Accept': 'text/plain' }

# construct Logical Jacobian Factorization
service = '/preprocessor/constructJacobian'
preprocessor_con.request('POST', service, mechanism, headers=headers)
res = preprocessor_con.getresponse()
jacobian = res.read()  
jacobian_json = json.loads(jacobian)

with open(outpath+'jacobian.json', 'w') as jacobian_outfile:
  json.dump(jacobian_json, jacobian_outfile, indent=2)
with open(outpath+'rate_constants_utility.F90', 'w') as rate_constants_outfile:
  rate_constants_outfile.write(jacobian_json["rate_constant_module"])


# Get construct fortran for Sparse Factorization and Sparse Solve (and Sparse Multiply)
service = '/preprocessor/constructSparseLUFactor'
preprocessor_con.request('POST', service, jacobian, headers=headers)
LU_SparseSolve_res =  preprocessor_con.getresponse()
LU_SparseSolve = LU_SparseSolve_res.read()
LU_SparseSolve_json = json.loads(LU_SparseSolve)

with open(outpath+'LU_sparse_solve.json', 'w') as LU_sparse_solve_outfile:
  json.dump(LU_SparseSolve_json, LU_sparse_solve_outfile, indent=2)
with open(outpath+'factor_solve_utilities.F90', 'w') as factor_solve_utilities:
  factor_solve_utilities.write(LU_SparseSolve_json["module"])


# Get kinetics_utilities including chemical jacobian init and kinetics init using the reordered list of constituents
service = '/preprocessor/toCode'
preprocessor_con.request('POST', service, LU_SparseSolve, headers=headers)
kinetics_res = preprocessor_con.getresponse()
kinetics = kinetics_res.read()
kinetics_json = json.loads(kinetics)
with open(outpath+'init.json', 'w') as kinetics_json_outfile:
  json.dump(kinetics_json, kinetics_json_outfile, indent=2)
with open(outpath+'kinetics_utilities.F90', 'w') as kinetics_utilities_outfile:
  kinetics_utilities_outfile.write(kinetics_json["module"])


#
#    Extract the code from github to solve the system
#
# 
#path  = outpath
#clone = "git clone https://github.com/NCAR/MusicBox"

#os.system("sshpass -p your_password ssh user_name@your_localhost")
#os.chdir(path) # Specifying the path where the cloned project needs to be copied
#os.system(clone) # Cloning




#
#    Collect the environmental conditions file
#
# 




#!/usr/bin/python3
import argparse
import os
import sys
from ftplib import FTP

from http.client import HTTPSConnection
import json

import requests
jac_url = "http://acom-conleyimac2.acom.ucar.edu:3000/constructJacobian"

headers = {
        "cache-control": "no-cache",
        "x-dreamfactory-api-key": "YOUR_API_KEY"
}


# needs to check that ssl is enabled
#import socket
#socket.ssl
# expect something like<function ssl at 0x4038b0>

# needs to check the python v3 is running

# Parse arguments.  They override those defaults specified in the argument parser
default_tag_server = "cafe-devel.acom.ucar.edu"
default_preprocessor_server = "www.acom.ucar.edu"
parser = argparse.ArgumentParser(
                    description='Solve a mechanism tag using the sparse solver branch of MusicBox/MICM.',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                    )
parser.add_argument('-tag_id', type=int, required=True,
                    help='Tag number for Chemistry Cafe mechanism tag')
parser.add_argument('-tag_server', type=str, default=default_tag_server,
                    help='url of tag server')
parser.add_argument('-overwrite', type=bool, default=False,
                    help='overwrite the target_dir')
parser.add_argument('-target_dir', type=bool, default=False,
                    help='target name for mechanism to be stored locally ')
 


args = parser.parse_args()


if(args.target_dir):
  outpath = "configured_tags/"+args.target_dir+"/"
else:
  outpath = "configured_tags/"+str(args.tag_id)+"/"

# make target_tag_location director
try:
  if(args.overwrite):
    os.system("rm -rf "+outpath)
    os.mkdir(outpath)
  else:
    os.mkdir(outpath)
except Exception as e:
  print("Directory "+outpath+" already exists.  Delete it if you want new data.")
  print("Exception: "+str(3))
  sys.exit(1)


with open(outpath+'this_configuration', 'w') as configuration_filehandle:
  configuration_filehandle.write(str(args))

# Connection to the Cafe
mechanism_store_location = args.tag_server
mechanism_con = HTTPSConnection(mechanism_store_location)

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


#!/usr/bin/python3

# Copyright (C) 2020 National Center for Atmospheric Research
# SPDX-License-Identifier: Apache-2.0

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

class tag_server:
  def __init__(self, nickname, server, accessor):
    self.nickname = nickname
    self.server = server
    self.accessor = accessor

  def connnection(self):
    return HTTPSConnection(self.server)


default_tag_server = tag_server("Published","www.acom.ucar.edu","/cgi-bin/acd/mechanism.py?hash=")
alternate_tag_server = tag_server("cafe-devel","chemistrycafe-devel.acom.ucar.edu","/node_processes/tags.php?action=return_tag&tag_id=")

tag_server_collection = [default_tag_server,alternate_tag_server]

def extract_server_nickname(server):
  return server.nickname

# needs to check that ssl is enabled
#import socket
#socket.ssl
# expect something like<function ssl at 0x4038b0>

# needs to check the python v3 is running

# Parse arguments.  They override those defaults specified in the argument parser
default_tag_server = "chemistrycafe-devel.acom.ucar.edu"
parser = argparse.ArgumentParser(
                    description='Solve a mechanism tag using the sparse solver branch of MusicBox/MICM.',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                    )
parser.add_argument('-tag_id', type=str, required=True,
                    help='Tag number for Chemistry Cafe mechanism tag')
#parser.add_argument('-tag_server', type=str, default=default_tag_server, help='url of tag server')
parser.add_argument('-overwrite', type=bool, default=False,
                    help='overwrite the target_dir')
parser.add_argument('-target_dir', type=bool, default=False,
                    help='target name for mechanism to be stored locally ')
parser.add_argument('-tag_server', default='Published', choices=list(map(extract_server_nickname,tag_server_collection)))

args = parser.parse_args()

# get the server corresponding to the nickname chosen
tagServer = next( (ts for ts in tag_server_collection if ts.nickname == args.tag_server), None)
print("Downloading tag from server: " +tagServer.server)

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

# Connection to the mechanism sever
try:
  mechanism_con = HTTPSConnection(tagServer.server)
except Exception as e:
  print("Unable to connect to server: "+tagServer.server)
  sys.exit(1)

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
print("Collecting tag using protocol: " + tagServer.accessor+str(args.tag_id))
try:
  mechanism_con.request('GET', tagServer.accessor+str(args.tag_id), headers=headers)
except Exception as e:
  print("Unable to connect to get tag_id: "+str(args.tag_id))
  print("From server:  "+str(tagServer.server))
  print(e)
  sys.exit(1)

try:
  res = mechanism_con.getresponse()
except Exception as e:
  print("Unable to get response from server: "+arts.tag_id)
  sys.exit(1)

# Collect the data, write a copy to file
# error testing?
mechanism = res.read()
try:
  mech_json = json.loads(mechanism)
except Exception as e:
  print("Server does not produce valid JSON mechanism file")
  sys.exit(1)

with open(outpath+'source_mechanism.json', 'w') as mechanism_outfile:
  json.dump(mech_json, mechanism_outfile, indent=2)

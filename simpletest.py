#!/usr/bin/env python

import qrcode
import qrcode.image.svg
import xml.etree.ElementTree as ET
from spacebro_client import SpacebroClient
from pathlib import Path
import json
import os
import sys, getopt
from wand.api import library
import wand.color
import wand.image
import urlparse

settings_files = ["settings/settings.default.json", "settings/settings.json"]
settings = {}
# get argv
def help():
    print 'qr-bro.py --settings <settingsfile>'
    print '-s <settingsfile>, --settings <settingsfile>'
    print '\t json settings file'

try:
  opts, args = getopt.getopt(sys.argv[1:],"hs:",["settings="])
except getopt.GetoptError:
  help()
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
     help()
     sys.exit()
  elif opt in ("-s", "--settings"):
     settings_files.append(arg)

# get settings
for file in settings_files:
  try:
    with open(file) as settings_file:
        settings.update(json.load(settings_file))
  except IOError:
    pass

print "Connecting to spacebro on ", settings['service']['spacebro']['host'], settings['service']['spacebro']['port'], '@',settings['service']['spacebro']['channelName']
spacebro = SpacebroClient(settings['service']['spacebro']['host'], settings['service']['spacebro']['port'], {'clientName': settings['service']['spacebro']['clientName'], 'channelName': settings['service']['spacebro']['channelName'], 'verbose': False})

# Listen
spacebro.wait(seconds=1)
spacebro.emit(settings['service']['spacebro']['inputMessage'], {'file': 'file.png'})
spacebro.wait()

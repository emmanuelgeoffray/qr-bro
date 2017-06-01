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



# get template
template = ET.parse(settings['recipe']).getroot()

# init folders
if not os.path.exists(settings['folder']['output']):
      os.makedirs(settings['folder']['output'])

def make_qrcode(input_url, file_name):

  print "Make qr code for url " + input_url
  img = qrcode.make(input_url, image_factory=qrcode.image.svg.SvgPathImage, border=0)
  img._img.append(img.make_path())

  path_template = template.findall(".//*[@id='qr-path']")
  path_img = img._img.findall('path')
  if (len(path_template) > 0 and path_img > 0):
    path_template = path_template[0]
    path_img = path_img[0]
    path_template.set('d', path_img.get('d'))

    symbol_template = template.findall(".//*[@id='qr-code']")[0]
    symbol_template.set('viewBox', img._img.get('viewBox'))
    img._img = template
  else:
    print "Issue with svg, path not found"

  image_file = open(file_name, 'w+')
  ET.ElementTree(img._img).write(image_file, encoding="UTF-8",
                                          xml_declaration=True)
  image_file.close()

def make_png (svg_file_path, png_file_path) :
  svg_file = open(svg_file_path, 'r')
  with wand.image.Image() as image:
        with wand.color.Color('transparent') as background_color:
            library.MagickSetBackgroundColor(image.wand, 
                                             background_color.resource) 
#image.read(blob=svg_file.read(), format="svg")
        image.read(blob=svg_file.read(), resolution=431)
        # colorize
        image.level(white=0)
        with wand.image.Image() as colorImage:
          colorImage.read(filename='recipes/color.png')
          colorImage.composite_channel(channel='opacity', image=image, left=0, top=0, operator='multiply')
          png_image = colorImage.make_blob("png32")

  with open(png_file_path, "wb") as out:
				out.write(png_image)

def on_new_media(args):
    #print('on_new_media', args)
    #print('file', args['file'])
    file_name = Path(args['url']).stem + '.svg'
    file_path = os.path.join(settings['folder']['output'], file_name)
    make_qrcode(args['url'], file_path)
    png_file_name = Path(args['url']).stem + '.png'
    png_file_path = os.path.join(settings['folder']['output'], png_file_name)
    make_png(file_path, png_file_path)
    args.setdefault('details', {})
    args['details']['qrcode'] = {'file': file_name, 'type': 'image/svg+xml', 'path': file_path}
    args['details']['qrcode-png'] = {'file': png_file_name, 'type': 'image/png', 'path': png_file_path}
    spacebro.emit(settings['service']['spacebro']['outputMessage'], args)
    print 'new qr code generated'
    print args


#make_qrcode('https://doublechee.se/en', "qrcode.svg")
print "Connecting to spacebro on ", settings['service']['spacebro']['host'], settings['service']['spacebro']['port'], '@',settings['service']['spacebro']['channelName']
spacebro = SpacebroClient(settings['service']['spacebro']['host'], settings['service']['spacebro']['port'], {'clientName': settings['service']['spacebro']['clientName'], 'channelName': settings['service']['spacebro']['channelName'], 'verbose': False})

# Listen
spacebro.wait(seconds=1)
spacebro.on(settings['service']['spacebro']['inputMessage'], on_new_media)
#spacebro.emit(settings['service']['spacebro']['inputMessage'], {'url': 'https://github.com:soixantecircuits/qr-bro.git'})
spacebro.wait()

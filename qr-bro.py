#!/usr/bin/env python

import qrcode
import qrcode.image.svg
import xml.etree.ElementTree as ET
from spacebro_client import SpacebroClient
from pathlib import Path

template = ET.parse("recipes/qrcode-path.svg").getroot()

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

def on_new_media(args):
    #print('on_new_media', args)
    #print('type', type (args))
    #print('file', args['file'])
    file_name = Path(args['file']).stem + '.svg'
    make_qrcode(args['src'], file_name)

#make_qrcode('https://doublechee.se/en', "qrcode.svg")
#make_qrcode('https://drive.google.com/drive/u/0/folders/0Bx68fA5yBZLwS0lWZG9fSzNCTk0', "qrcode_fr.svg")
socketIO = SpacebroClient('localhost', 8888, {'clientName': 'qr-bro', 'channelName': 'zhaoxiangjs', 'verbose': False})

# Listen
socketIO.wait(seconds=1)
socketIO.on('video-saved', on_new_media)
socketIO.emit('album-saved', {'src': '/home/emmanuel/Videos/2017-03-08T11-07-35-698'})
socketIO.wait()

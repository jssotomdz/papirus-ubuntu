#!/usr/bin/python3

import codecs
import os
import sys
import math
import random
import re
from glob import glob

ubuntuColors = ['#e95420', '#77216f']
symlinks = []
pending = []
    
def colorPickerR(g):
  if(g > 0.5):
    return 75*math.sqrt(g)+179
  else:
    return 476*(g**2)

def colorPickerG(g):
  if(g > 0.5):
    return 583*math.sqrt(g)-329
  else:
    return 132*(g**2)

def colorPickerB(g):
  if(g > 0.5):
    return 761*math.sqrt(g)-506
  else:
    return 444*(g**2)

def processFolder(folder):
  for filename in glob(os.path.join(folder, "*")):
    if os.path.islink(filename):
      symlinks.append(filename)
    else:
      if(os.path.isdir(filename)) and "Ubuntu" not in filename:
        processFolder(filename)
      elif "svg" in filename or "SVG" in filename:
        outName = filename.replace(filename.split('/')[1], filename.split('/')[1] + "-Ubuntu")
        if not os.path.exists(outName) and not os.path.islink(filename):
          print(outName)
          os.makedirs(os.path.dirname(outName), exist_ok=True)
          out = open(outName, "x")
          f = codecs.open(filename, encoding='utf-8', errors='ignore')
          content = f.read()

          colors = dict()
          colors2replace = dict()

          start_index=0
          for i in range(len(content)):
            j = content.find('#',start_index)
            if(j!=-1):
              start_index = j+1
              color = content[j:j+7]
              match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
              if match:                      
                if color in colors:
                  colors[color] += 1
                else:
                  colors[color] = 1

          for color, val in colors.items():
              d2w = math.sqrt((int(color[1:3], 16)-int("FF", 16))**2 + (int(color[3:5], 16)-int("FF", 16))**2 + (int(color[5:], 16)-int("FF", 16))**2) < 30
              d2b = math.sqrt((int(color[1:3], 16)-int("00", 16))**2 + (int(color[3:5], 16)-int("00", 16))**2 + (int(color[5:], 16)-int("00", 16))**2) < 30
              gray = abs(int(color[1:3], 16) - int(color[3:5], 16)) < 5 and abs(int(color[3:5], 16) == int(color[5:], 16)) < 5 and abs(int(color[3:5], 16) == int(color[5:], 16)) < 5
              if d2w or d2b:
                pass
              else:
                colors2replace[color] = val
        
          colors2replace = dict(sorted(colors2replace.items(), key=lambda item: item[1], reverse=True))

          for color in colors2replace:
            gray = int(color[1:3], 16)/255 * 0.3 + int(color[3:5], 16)/255 * 0.59 + int(color[5:], 16)/255 * 0.11
            R = int(colorPickerR(gray))
            G = int(colorPickerG(gray))
            B = int(colorPickerB(gray))
            newColor = '#' + bytearray([R, G, B]).hex()
            content = content.replace(color, newColor)
          out.write(content)
          f.close()



dirs = glob("./*/", recursive = True)

for item in dirs:
  folderName = item[:-1]
  if "Ubuntu" not in folderName:
    processFolder(folderName)

for filename in symlinks:
  outName = filename.replace(filename.split('/')[1], filename.split('/')[1] + "-Ubuntu")
  if not os.path.exists(outName):
    try:
      os.symlink(os.readlink(filename).replace(filename.split('/')[1], filename.split('/')[1] + "-Ubuntu"), outName)
    except:
      pending.append(filename)
    
for filename in pending:
  outName = filename.replace(filename.split('/')[1], filename.split('/')[1] + "-Ubuntu")
  if not os.path.exists(outName):
    try:
      os.makedirs(os.path.dirname(outName), exist_ok=True)
      os.symlink(os.readlink(filename).replace(filename.split('/')[1], filename.split('/')[1] + "-Ubuntu"), outName)
    except:
      print("Failed: " + outName + " -> "+ os.readlink(filename).replace(filename.split('/')[1], filename.split('/')[1] + "-Ubuntu"))

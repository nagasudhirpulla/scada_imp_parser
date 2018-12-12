# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:47:41 2018

@author: Nagasudhir
"""
import json
from impParser import ImpParser

# name of the file to parse
filename = 'bachu.imp'
parser = ImpParser()
parser.processImpFile(filename)

with open('bachu.json', 'w') as f:
    json.dump(parser.substations, f, indent = 4)
    
from impDBCreation import create_db

create_db()
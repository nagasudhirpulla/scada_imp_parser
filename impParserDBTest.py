# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 15:00:06 2018

@author: Nagasudhir
"""

from impParserDB import ImpParserDB
import os
import glob

# fall back input folder name
inputFolder = r'C:\Users\Nagasudhir\Documents\Python Projects\python_freq_analysis'

# get the directory of the script file
if('__file__' in globals()):
    inputFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'impFiles')

sqlite_db_config = {'drivername': 'sqlite', 'database': 'test.sqlite'}
parser = ImpParserDB(sqlite_db_config)

dataFilesList = glob.glob(inputFolder + '/*.imp')

for fileIter, inputFilename in enumerate(dataFilesList):
    # name of the file to parse
    # inputFilename = 'argbd_pg.imp'
    parser.processImpFile(inputFilename)

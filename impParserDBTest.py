# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 15:00:06 2018

@author: Nagasudhir
"""

from impParserDB import ImpParserDB

# name of the file to parse
filename = 'bachu.imp'
sqlite_db_config = {'drivername': 'sqlite', 'database': 'test.sqlite'}
parser = ImpParserDB(sqlite_db_config)
parser.processImpFile(filename)

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:47:41 2018

@author: Nagasudhir
"""
class ImpParser:
    substations = []    
    currentSub = None
    currentDevType = None
    currentDevice = None
            
    def processImpFile(self, filename):
        # text lines in the file
        textLines = []
        # open the file and read the text lines
        with open('bachu.imp', 'r+') as f:
            for line in f.readlines():
                textLines.append(line)
        
        # strip text lines off the spaces
        textLines = [textLine.strip() for textLine in textLines]
        
        # process each text line
        for textLine in textLines:
            self.processTextLine(textLine)
        if(self.currentSub != None):
                self.substations.append(self.currentSub)
        
    # do line processing
    def processTextLine(self, textLine):
        # ignore the line if it starts with #
        if(textLine.startswith('#')):            
            return
        
        # split the line with , delimiter to get the line columns
        cols = textLine.split(',')
        
        # strip off the spaces, strip off " also while processing column values
        cols = [col.strip().strip('"') for col in cols]
        
        # if line cols start with SUBSTN,it is a substation record
        if(cols[0] == 'SUBSTN'):
            # hence update **current substation**. substation id col = 1, substation name col = 2
            if(self.currentSub != None):
                self.substations.append(self.currentSub)
            self.currentSub = dict(name = cols[2],id = cols[1], devices = [])
            return
        
        # if line cols start with DEVTYP,it is a device type record
        if(cols[0] == 'DEVTYP'):
            # hence update **current device type**. device type name col = 1
            self.currentDevType = cols[1]
        
        # if line cols start with DEVICE
        if(cols[0] == 'DEVICE'):
            # it is a device record, hence upadte **current device**
            # device id col = 1, device name col = 2, device voltage = 5
            if(self.currentDevice != None):
                self.currentSub['devices'].append(self.currentDevice)
            self.currentDevice = dict(name = cols[2], type = self.currentDevType, nodes = [], id = cols[1], voltage = cols[5], substationId = self.currentSub['id'])
            
            # if the device is a BUS, then it is node by itself
            if(self.currentDevType == "BUS"):
                # hence it has only one node. The node name is device id col, i.e., column 1
                self.currentDevice['nodes'].append(dict(name=cols[1], substationId = self.currentSub['id']))
                return
            
            # if the device is a line, then the node pair is stored in the device definition itself
            if(self.currentDevType == "LINE"):
                # the current substation node is col 7 and remote substation id is col 11, remote substation node is col 10
                self.currentDevice['nodes'].append(dict(name=cols[7], substationId = self.currentSub['id']))
                self.currentDevice['nodes'].append(dict(name=cols[10], substationId = cols[11]))
            
            # if the device is a RE, then the node is stored in the device definition itself, the node name is col 7
            if(self.currentDevType in ["RE", "ZBR"]):
                self.currentDevice['nodes'].append(dict(name=cols[7], substationId = self.currentSub['id']))
            return
                
        # if the line cols start with POINT,STTD
        if(cols[0] == 'POINT' and cols[1] == 'STTD'):
            # update the **current point**. the node pair columns are 4 and 5    
            self.currentDevice['nodes'].append(dict(name=cols[4], substationId = self.currentSub['id']))
            self.currentDevice['nodes'].append(dict(name=cols[5], substationId = self.currentSub['id']))
        return
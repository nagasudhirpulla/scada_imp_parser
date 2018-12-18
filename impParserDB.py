# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:47:41 2018

@author: Nagasudhir
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from impDBModel import ImpHelper, Region, DeviceType, Device, Node, Substation

class ImpParserDB:
    substations = []    
    currentSub = None
    currentDevType = None
    currentDevice = None
    db_config_dict = None
    db_helper = None
    session= None
    currentRegion = None
    
    # constructor
    def __init__(self, db_config_dict):
        self.db_config_dict = db_config_dict
        self.db_helper = ImpHelper(db_config_dict)
        # create db if not present
        self.db_helper.create_db()
        # create session
        Session = sessionmaker()
        Session.configure(bind=self.db_helper.get_engine())
        # open session
        self.session = Session()
        # add the region initially
        region = Region(name='WR')
        self.AddRegion(region, False)
        self.currentRegion = self.session.query(Region).filter(Region.name == region.name).all()[0]
        
    def AddRegion(self, region, updateExisting=True):
        if(region != None):
            # check if deviceType is already present
            queriedRegions = self.session.query(Region).filter(Region.name==region.name).all()
            if(len(queriedRegions) == 0):
                # add the region and commit
                self.session.add(region)
                self.session.commit()
            else:
                # The deviceType is already present
                if(updateExisting == True):
                    # update the deviceType only if desired else donot add the deviceType
                    queriedRegions[0].name = region.name
                    self.session.commit()
    
    def AddSubstation(self, substation, updateExisting=True):
        if(substation != None):
            # check if substation is already present
            queriedSubstations = self.session.query(Substation).filter(Substation.name==substation.name).all()
            if(len(queriedSubstations) == 0):
                # add the substation to the region and commit
                substation.region_id = self.currentRegion.id
                self.session.add(substation)
                self.session.commit()
            else:
                # The substation is already present
                if(updateExisting == True):
                    # update the substation only if desired else donot add the substation
                    queriedSubstations[0].name = substation.name
                    queriedSubstations[0].alias_name = substation.alias_name
                    self.session.commit()
    
    def AddDeviceType(self, deviceType, updateExisting=True):
        if(deviceType != None):
            # check if deviceType is already present
            queriedDeviceTypes = self.session.query(DeviceType).filter(DeviceType.name==deviceType.name).all()
            if(len(queriedDeviceTypes) == 0):
                # add the deviceType and commit
                self.session.add(deviceType)
                self.session.commit()
            else:
                # The deviceType is already present
                if(updateExisting == True):
                    # update the deviceType only if desired else donot add the deviceType
                    queriedDeviceTypes[0].name = deviceType.name
                    self.session.commit()
    
    def AddDevice(self, device, updateExisting=True):
        if(device != None):
            # check if device is already present
            queriedDevices = self.session.query(Device).filter(and_(Device.unique_name==device.unique_name, Device.device_type_id == device.device_type_id)).all()
            if(len(queriedDevices) == 0):
                # add the device and commit
                self.session.add(device)
                self.session.commit()
            else:
                # The device is already present
                if(updateExisting == True):
                    # update the device only if desired else donot add the device
                    queriedDevices[0].unique_name = device.unique_name
                    queriedDevices[0].name = device.name
                    queriedDevices[0].alias_name = device.alias_name
                    queriedDevices[0].device_type_id = device.device_type_id
                    self.session.commit()
    
    def AddNode(self, node_el, updateExisting=True):
        if(node_el != None):
            # check if device is already present
            queriedNodes = self.session.query(Node).filter(and_(Node.name==node_el.name, Node.ssid==node_el.ssid)).all()
            if(len(queriedNodes) == 0):
                # add the device and commit
                self.session.add(node_el)
                self.session.commit()
            else:
                # The device is already present
                if(updateExisting == True):
                    # update the device only if desired else donot add the device
                    queriedNodes[0].name = node_el.name
                    queriedNodes[0].ssid = node_el.ssid
                    self.session.commit()
    
    def processImpFile(self, filename):
        # text lines in the file
        textLines = []
        # open the file and read the text lines
        with open(filename, 'r+') as f:
            for line in f.readlines():
                textLines.append(line)
        
        # strip text lines off the spaces
        textLines = [textLine.strip() for textLine in textLines]
        
        # process each text line
        for textLine in textLines:
            self.processTextLine(textLine)
        self.AddSubstation(self.currentSub)
        
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
            # self.AddSubstation(self.currentSub)
            self.AddSubstation(Substation(name=cols[1], alias_name=cols[2]))
            self.currentSub = self.session.query(Substation).filter(Substation.name == cols[1]).all()[0]
            return
        
        # if line cols start with DEVTYP,it is a device type record
        if(cols[0] == 'DEVTYP'):
            # hence update **current device type**. device type name col = 1
            # self.AddDeviceType(self.currentDevType)
            self.AddDeviceType(DeviceType(name=cols[1]), False)
            self.currentDevType = self.session.query(DeviceType).filter(DeviceType.name == cols[1]).all()[0]
            
        
        # if line cols start with DEVICE
        if(cols[0] == 'DEVICE'):
            # it is a device record, hence upadte **current device**
            # device id col = 1, device name col = 2, device voltage = 5
            # if(self.currentDevice != None):
                # self.AddDevice(self.currentDevice)
            # to derive unique device name, we append ss name if the device is not a line
            if(self.currentDevType.name != "LINE"):
                uniqueDeviceName = '{0}_{1}'.format(cols[1], self.currentSub.name)
            else:
                uniqueDeviceName = cols[1]
            self.AddDevice(Device(name=cols[1], unique_name = uniqueDeviceName, alias_name=cols[2], voltage=cols[5], device_type = self.currentDevType))
            self.currentDevice = self.session.query(Device).filter(and_(Device.unique_name == uniqueDeviceName, Device.device_type_id == self.currentDevType.id)).all()[0]
            
            # if the device is a BUS, then it is node by itself
            if(self.currentDevType.name == "BUS"):
                # hence it has only one node. The node name is device id col, i.e., column 1
                node_el = Node(name=cols[1])
                node_el.ssid = self.currentSub.id
                self.AddNode(node_el, False)
                node_el = self.session.query(Node).filter(and_(Node.name==node_el.name, Node.ssid==node_el.ssid)).all()[0]
                self.currentDevice.nodes.append(node_el)
                self.session.commit()
                return
            
            # if the device is a line, then the node pair is stored in the device definition itself
            if(self.currentDevType.name == "LINE"):
                # the current substation node is col 7 and remote substation id is col 11, remote substation node is col 10
                node_el = Node(name=cols[7])
                node_el.ssid = self.currentSub.id
                self.AddNode(node_el, False)
                node_el = self.session.query(Node).filter(and_(Node.name==node_el.name, Node.ssid==node_el.ssid)).all()[0]
                self.currentDevice.nodes.append(node_el)
                self.session.commit()
                # create remote ss if not present
                remoteSubstation = Substation(name=cols[11])
                self.AddSubstation(remoteSubstation, False)
                remoteSubstation = self.session.query(Substation).filter(Substation.name==remoteSubstation.name).all()[0]
                node_el2 = Node(name=cols[10])
                node_el2.ssid = remoteSubstation.id
                self.AddNode(node_el2, False)
                node_el2 = self.session.query(Node).filter(and_(Node.name==node_el2.name, Node.ssid==node_el2.ssid)).all()[0]
                self.currentDevice.nodes.append(node_el2)
                self.session.commit()
            
            # if the device is a RE, then the node is stored in the device definition itself, the node name is col 7
            if(self.currentDevType.name in ["RE", "ZBR"]):
                node_el = Node(name=cols[7])
                node_el.ssid = self.currentSub.id
                self.AddNode(node_el, False)
                node_el = self.session.query(Node).filter(and_(Node.name==node_el.name, Node.ssid==node_el.ssid)).all()[0]
                self.currentDevice.nodes.append(node_el)
                self.session.commit()
            return
                
        # if the line cols start with POINT,STTD
        if(cols[0] == 'POINT' and cols[1] == 'STTD'):
            # update the **current point**. the node pair columns are 4 and 5
            node_el = Node(name=cols[4])
            node_el.ssid = self.currentSub.id
            self.AddNode(node_el, False)
            node_el = self.session.query(Node).filter(and_(Node.name==node_el.name, Node.ssid==node_el.ssid)).all()[0]
            self.currentDevice.nodes.append(node_el)
            self.session.commit()
            node_el2 = Node(name=cols[5])
            node_el2.ssid = self.currentSub.id
            self.AddNode(node_el2, False)
            node_el2 = self.session.query(Node).filter(and_(Node.name==node_el2.name, Node.ssid==node_el2.ssid)).all()[0]
            self.currentDevice.nodes.append(node_el2)
            self.session.commit()
        return
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 10:41:13 2018

@author: Nagasudhir

# defining primary key in pydal - https://stackoverflow.com/questions/25674752/how-can-i-define-a-custom-primary-key-in-web2py

# sqlalchemy cheat sheet - https://www.pythonsheets.com/notes/python-sqlalchemy.html
# sqlalchemy unique key multiple columns - https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
# sqlalchemy many to many relashionships - https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
# overall example - https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from impDBModel import ImpHelper, Region, DeviceType, Device, Node, Substation
import contextlib

# create db helper from other class
sqlite_db = {'drivername': 'sqlite', 'database': 'test.sqlite'}
db_helper = ImpHelper(sqlite_db)

# clear all the tables
meta = MetaData()
with contextlib.closing(db_helper.get_engine().connect()) as con:
    trans = con.begin()
    for table in reversed(meta.sorted_tables):
        con.execute(table.delete())
    trans.commit()

# create the database
db_helper.create_db()

# create session
Session = sessionmaker()
Session.configure(bind=db_helper.get_engine())

# open session
session = Session()

# create a new region object to add
wr_region = Region(name='WR')
session.add(wr_region)

# create a substation
subs_el = Substation(name='SS1', alias_name='ss1 alias')
subs_el.region = wr_region

# create a device type
line_type = DeviceType(name='line')
session.add(line_type)

# create a device of type line
line_device = Device(name='line_device', device_type_id=session.query(DeviceType).filter(DeviceType.name==line_type.name).all()[0].id)
session.add(line_device)

# create a node elements
node_el = Node(name='test_node1')
node_el.substation = subs_el
node_el2 = Node(name='test_node2')
node_el2.substation = subs_el

# link device to the nodes
line_device.nodes = [node_el, node_el2]

# commit the session
session.commit()

# update the region
session.query(Region).update({Region.name:'WR'})
session.commit()

# printing all the regions
regions = session.query(Region).all()
for region in regions:
    print('Region => {0}'.format(region.name))

# printing all the device types
device_types = session.query(DeviceType).all()
for device_type in device_types:
    print('Device Type => {0}'.format(device_type.name))

# printing all devices
devices = session.query(Device).all()
for device in devices:
    print('Device => {0}, device_type => {1}'.format(device.name, device.device_type.name))

# close the session
session.close()

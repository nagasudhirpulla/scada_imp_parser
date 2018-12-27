# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 10:41:13 2018

@author: Nagasudhir

# defining primary key in pydal - https://stackoverflow.com/questions/25674752/how-can-i-define-a-custom-primary-key-in-web2py

# sqlalchemy cheat sheet - https://www.pythonsheets.com/notes/python-sqlalchemy.html
# sqlalchemy unique key multiple columns - https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
# sqlalchemy many to many relashionships - https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
# overall example - https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/

# Python get the object status in session [persistent, pending, transcient] - https://www.pythoncentral.io/understanding-python-sqlalchemy-session/
# Python unbind object from session - https://stackoverflow.com/questions/11213665/unbind-object-from-session
"""

from sqlalchemy import create_engine, ForeignKey, Table
import datetime as dt
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
# from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

# get connected to the database
'''
postgres_db = {'drivername': 'postgres',
               'username': 'postgres',
               'password': 'postgres',
               'host': '192.168.99.100',
               database='dbname',
               'port': 5432}
'''
Base = declarative_base()
class Region(Base):
    __tablename__ = 'regions'
    id   = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default = dt.datetime.now)
    updated_at = Column(DateTime, default = dt.datetime.now, onupdate = dt.datetime.now)

class Substation(Base):
    __tablename__ = 'substations'
    id   = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False, unique=True)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    region = relationship('Region', backref='substations')
    alias_name  = Column(String, unique=False) # kept False since we encountered error in pmu
    created_at = Column(DateTime, default = dt.datetime.now)
    updated_at = Column(DateTime, default = dt.datetime.now, onupdate = dt.datetime.now)

class DeviceType(Base):
    __tablename__ = 'device_types'
    id   = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default = dt.datetime.now)
    updated_at = Column(DateTime, default = dt.datetime.now, onupdate = dt.datetime.now)

DeviceNode = Table('device_nodes', Base.metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('device_id', Integer(), ForeignKey('devices.id')),
                   Column('node_id', Integer(), ForeignKey('nodes.id')),
                   UniqueConstraint('node_id', 'device_id', name='device_node_unique'))

class Device(Base):
    __tablename__ = 'devices'
    id   = Column(Integer, primary_key=True)
    unique_name = Column(String, nullable=False)
    name = Column(String, nullable=False)
    device_type_id = Column(Integer, ForeignKey('device_types.id'), nullable=False)
    alias_name = Column(String, nullable=False)
    voltage = Column(String, nullable=False)
    created_at = Column(DateTime, default = dt.datetime.now)
    updated_at = Column(DateTime, default = dt.datetime.now, onupdate = dt.datetime.now)
    nodes = relationship('Node', secondary = DeviceNode, backref = 'devices')
    device_type = relationship("DeviceType", backref='devices')
    __table_args__ = (
            UniqueConstraint('unique_name', 'device_type_id'),            
            )

class Node(Base):
    __tablename__ = 'nodes'
    id   = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False)
    ssid = Column(Integer, ForeignKey('substations.id'), nullable=False)
    created_at = Column(DateTime, default = dt.datetime.now)
    updated_at = Column(DateTime, default = dt.datetime.now, onupdate = dt.datetime.now)
    substation = relationship("Substation", backref='nodes')
    __table_args__ = (
            UniqueConstraint('name', 'ssid'),            
            )

class ImpHelper:
    db_uri = None
    engine = None
    
    def __init__(self, db_config_dict):
        self.db_uri = URL(**db_config_dict)
        self.engine = create_engine(self.db_uri)
    
    def create_db(self):
        # create all tables if db does not exists
        Base.metadata.create_all(self.engine)
    
    def get_engine(self):
        return self.engine
import serial
from threading import Thread
from datetime import datetime
from firebase import firebase
import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref

from Queue import Queue



Base = declarative_base()

class PersonEvent(Base):

    __tablename__ = 'personEvents'

    id          =   Column(Integer, primary_key=True)
    eventType   =   Column(Integer, default=0)
    timestamp   =   Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        str_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return "<PersonEvent (id='%s', type='%d', timestamp=%s)>" % (self.id, self.eventType, str_timestamp)


class PersonCounter:

    def __init__(self, port="/dev/ttyACM0", baud=115200, firebaseConf=None):
        self.port = port
        self.baud = baud
        self.firebaseConf = {}
        if firebaseConf != None:
            self.firebaseConf = firebaseConf

        self.serial = serial.Serial(self.port, self.baud, timeout=0)
        self.serial_thread = Thread(target=self.serialLoop)
        self.serial_thread.daemon = True

        # db
        self.engine = create_engine('sqlite:///:memory:', echo=True)

    def serialLoop(self):
        pass
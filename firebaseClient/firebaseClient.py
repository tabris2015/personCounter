#!/usr/bin/python
import threading
import serial
import time
from datetime import datetime
from firebase import firebase
import sqlite3
from datetime import datetime, timedelta


#///////////////////////////////////////////
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#/////////////////////////////////////////////////

events = []
events2 = []
####
connected = False

def handle_data_s1(data):
    #print(type(data), data)
    #print("code: ", data[0])
    event_dic = {}
    code = data[0]
    global events
    if code == 'I':
        event_dic["tipo_marcado"] = 1
        event_dic["fecha"] = datetime.utcnow()
        event_dic["id_sensor"] = 1
        events2.append((datetime.now(), 1))
        print("in1")
        events.append(event_dic)
        #first_event = True
    elif code == 'O':
        event_dic["tipo_marcado"] = 0
        event_dic["fecha"] = datetime.utcnow()
        event_dic["id_sensor"] = 1
        events2.append((datetime.now(), 0))
        print("out1")
        #first_event = True
        events.append(event_dic)
    else:
        pass
        #print("no code")

def handle_data_s2(data):
    #print(type(data), data)
    #print("code: ", data[0])
    event_dic = {}
    code = data[0]
    global events
    if code == 'I':
        event_dic["tipo_marcado"] = 1
        event_dic["fecha"] = datetime.utcnow()
        event_dic["id_sensor"] = 2
        events2.append((datetime.now(), 1))
        print("in2")
        events.append(event_dic)
        #first_event = True
    elif code == 'O':
        event_dic["tipo_marcado"] = 0
        event_dic["fecha"] = datetime.utcnow()
        event_dic["id_sensor"] = 2
        events2.append((datetime.now(), 0))
        print("out2")
        #first_event = True
        events.append(event_dic)
    else:
        pass
        #print("no code")



def read_from_port1(ser):
    global connected
    print("hilo serial 1")
    while not connected:
        connected = True

        while True:
            #print("test")
            if ser.in_waiting:
                reading = ser.readline()
                ser.flush()
                if reading:
                    handle_data_s1(reading)

                time.sleep(0.05)


def read_from_port2(ser):
    global connected
    print("hilo serial 2")
    while not connected:
        connected = True

        while True:
            #print("test")
            if ser.in_waiting:
                reading = ser.readline()
                ser.flush()
                if reading:
                    handle_data_s2(reading)

                time.sleep(0.05)



def pushToLocalDB(db, event):
    insert_SQL = '''INSERT INTO personEvent(tstamp, type) VALUES(?, ?)'''
    c = db.cursor()
    c.execute(insert_SQL,(event['tstamp'], event['type']))
    db.commit()



def select_all_events(conn):
    """
    Query all rows in the events table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM personEvent")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


def select_last_events(conn):
    """
    Query all rows in the events table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM personEvent ORDER BY id DESC LIMIT 3")
 
    rows = cur.fetchall()
    
    print("last 3 events: ")
    for row in rows:
        print(row)
 

def periodicDBInsert(key):
    #///////////////////
    cred = credentials.Certificate(key)
    firebase_admin.initialize_app(cred)
    dbFs = firestore.client()
    # for sqlite
    
    insert_SQL = '''INSERT INTO personEvent(tstamp, type) VALUES(?, ?)'''
    global events
    global events2

    #db = sqlite3.connect('local.db')
    c = db.cursor()
    while True:
        if not events:
            print("no hay eventos!")
        else:
            print("insertando eventos...")
            # for event in events:
            #     pushToLocalDB(db, event)
            # creando doc
            doc_ref = dbFs.collection(u'marcados_eventos').document(unicode(datetime.now()))
            doc_data = {
                            'marcados':events,
                            'id_evento': 1,

            }   
            doc_ref.set(doc_data)

            #c.executemany(insert_SQL, events2)
            #db.commit()
            #select_last_events(db)
            events = []
            events2 = []

        time.sleep(30)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='contador de personas')
    parser.add_argument('-serial1', required=True, action='store',help='for serial port1')
    parser.add_argument('-serial2', required=True, action='store',help='for serial port2')
    parser.add_argument('-key', required=True, action='store',help='path to key for remote connection')
    
    args = parser.parse_args()
    keyPath = ""
    if args.key != None:
        keyPath = args.key

    if args.serial1 != None and args.serial2 != None:
        print("puerto serial!")
        port1 = args.serial1
        port2 = args.serial2
        baud = 115200

        serial_port1 = serial.Serial(port1, baud, timeout=0)
        print("serial1 conectado!")
        serial_port2 = serial.Serial(port2, baud, timeout=0)
        print("serial2 conectado!")
        
        serialTh1 = threading.Thread(target=read_from_port1, args=(serial_port1,))
        serialTh2 = threading.Thread(target=read_from_port2, args=(serial_port2,))
        serialTh1.daemon = True
        serialTh2.daemon = True
        serialTh1.start()
        serialTh2.start()
    else:
        port = "/dev/ttyUSB0"


    #first_event = False

    dbTh = threading.Thread(target=periodicDBInsert, args=(keyPath,))

    #dbTh = threading.Timer(5, periodicDBInsert, args=(db,))
    dbTh.daemon = True
    # -----
    dbTh.start()
    ###

    URL = ".."

    SECRET = "...."
    EMAIL = "000000"
    EXTRA = "EEEEE"
    #authentication = firebase.FirebaseAuthentication(SECRET, EMAIL, extra=EXTRA)

    #firebase = firebase.FirebaseApplication(URL, authentication=authentication)

    while True:
        pass
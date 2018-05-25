import threading
import serial
import time
from datetime import datetime
from firebase import firebase
import sqlite3
from datetime import datetime, timedelta

#/////////////////////////////////////////////////

events = []

events2 = []
####
connected = False

def handle_data(data):
    #print(type(data), data)
    #print("code: ", data[0])
    event_dic = {}
    code = data[0]
    global events
    if code == 'I':
        event_dic["type"] = 'IN'
        event_dic["tstamp"] = datetime.now()
        events2.append((datetime.now(), 'IN'))
        print("in")
        events.append(event_dic)
        #first_event = True
    elif code == 'O':
        event_dic["type"] = 'OUT'
        event_dic["tstamp"] = datetime.now()
        events2.append((datetime.now(), 'OUT'))
        print("out")
        #first_event = True
        events.append(event_dic)
    else:
        print("no code")



def read_from_port(ser):
    global connected
    while not connected:
        connected = True

        while True:
            #print("test")
            reading = ser.readline()
            if reading:
                handle_data(reading)

            time.sleep(0.1)




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
 

def periodicDBInsert():
    # for sql
    insert_SQL = '''INSERT INTO personEvent(tstamp, type) VALUES(?, ?)'''
    global events
    global events2
    db = sqlite3.connect('local.db')
    c = db.cursor()
    while True:
        if not events:
            print("no hay eventos!")
        else:
            print("insertando eventos...")
            # for event in events:
            #     pushToLocalDB(db, event)

            c.executemany(insert_SQL, events2)
            db.commit()
            select_last_events(db)
            events = []
            events2 = []

        time.sleep(10)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='contador de personas')
    parser.add_argument('-serial', action='store',help='for serial port')

    args = parser.parse_args()

    if args.serial != None:
        print("puerto serial!")
        port = args.serial
    else:

        port = "/dev/ttyUSB0"

    baud = 115200

    serial_port = serial.Serial(port, baud, timeout=0)


    first_event = False
    serialTh = threading.Thread(target=read_from_port, args=(serial_port,))
    serialTh.daemon = True

    dbTh = threading.Thread(target=periodicDBInsert)

    #dbTh = threading.Timer(5, periodicDBInsert, args=(db,))
    dbTh.daemon = True
    # -----
    dbTh.start()
    serialTh.start()
    ###

    URL = ".."

    SECRET = "...."
    EMAIL = "000000"
    EXTRA = "EEEEE"
    #authentication = firebase.FirebaseAuthentication(SECRET, EMAIL, extra=EXTRA)

    #firebase = firebase.FirebaseApplication(URL, authentication=authentication)


    while True:
        pass
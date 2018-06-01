#!/usr/bin/python
import threading
import Queue
import serial
import time
from datetime import datetime
from firebase import firebase
import sqlite3
from datetime import datetime, timedelta

from gpiozero import Button

#///////////////////////////////////////////
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#/////////////////////////////////////////////////

##### pin definitions

IN1 = 13
OUT1 = 6
IN2 = 26
OUT2 = 19

in1_button = Button(IN1, pull_up=False)
out1_button = Button(OUT1, pull_up=False)
in2_button = Button(IN2, pull_up=False)
out2_button = Button(OUT2, pull_up=False)

eventQueue = Queue.Queue()
####
connected = False

def queue_get_all(q):
    items = []
    maxItemsToRetreive = 10000
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            items.append(q.get_nowait())
        except:
            break
    return items


def in1Event():
    print("in1!")
    event_dic = {}
    event_dic["tipo_marcado"] = 1
    event_dic["fecha"] = datetime.utcnow()
    event_dic["id_sensor"] = 1
    eventQueue.put(event_dic)

def out1Event():
    print("out1!")
    event_dic = {}
    event_dic["tipo_marcado"] = 0
    event_dic["fecha"] = datetime.utcnow()
    event_dic["id_sensor"] = 1
    eventQueue.put(event_dic)

def in2Event():
    print("in2!")
    event_dic = {}
    event_dic["tipo_marcado"] = 1
    event_dic["fecha"] = datetime.utcnow()
    event_dic["id_sensor"] = 2
    eventQueue.put(event_dic)

def out2Event():
    print("out1!")
    event_dic = {}
    event_dic["tipo_marcado"] = 0
    event_dic["fecha"] = datetime.utcnow()
    event_dic["id_sensor"] = 2
    eventQueue.put(event_dic)


def periodicDBInsert(key):
    #///////////////////
    cred = credentials.Certificate(key)
    firebase_admin.initialize_app(cred)
    dbFs = firestore.client()
    # for sqlite
  
    while True:
        
        if eventQueue.empty():
            print("no hay eventos!")
        else:
            print("insertando eventos...")
            # for event in events:
            #     pushToLocalDB(db, event)
            # creando doc
            events = queue_get_all(eventQueue)
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


        time.sleep(60)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='contador de personas')
    parser.add_argument('-key', required=True, action='store',help='path to key for remote connection')
    
    args = parser.parse_args()
    keyPath = ""
    if args.key != None:
        keyPath = args.key

    #first_event = False

    dbTh = threading.Thread(target=periodicDBInsert, args=(keyPath,))

    #dbTh = threading.Timer(5, periodicDBInsert, args=(db,))
    dbTh.daemon = True
    # -----
    dbTh.start()
    ###

    #firebase = firebase.FirebaseApplication(URL, authentication=authentication)
    in1_button.when_pressed = in1Event
    out1_button.when_pressed = out1Event
    in2_button.when_pressed = in2Event
    out2_button.when_pressed = out2Event
    
    while True:
        time.sleep(0.1)
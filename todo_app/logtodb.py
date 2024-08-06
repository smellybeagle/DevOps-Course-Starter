import datetime
import pymongo
import os,time
from pymongo import ASCENDING
from logging import Formatter

Formatter.converter= time.gmtime


def writelogtodb(msg):
    dbconnection = os.getenv("MONGODB_CONN")
    client = pymongo.MongoClient(dbconnection) 
    db = client.logging
    collection = db.log
    #log_collection.ensure_index()  
    entry = {}
    entry['timestamp'] = datetime.datetime.utcnow()
    entry['msg'] = msg
    collection.insert_one(entry)#.ensure_index([("timestamp", ASCENDING)])

    





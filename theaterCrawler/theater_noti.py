#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import telebot
import threading
import time
import pymongo
from pymongo.cursor import CursorType
import datetime
from datetime import timedelta
from datetime import datetime

tb = telebot.TeleBot("173966270:AAHkLiAImcKi_1-2RJkGFI78uJ7zIWNsgHU") 
mongo_url = 'mongodb://localhost:27017'
connection = pymongo.MongoClient(mongo_url)
mydb = connection['theater']
collection = mydb['info']

db = pymongo.MongoClient(mongo_url).local
last_ts = db.oplog.rs.find().sort('$natural', -1)[0]['ts'];
print last_ts

@tb.message_handler(commands=['start'])
def send_welcome(message):
    global collection
    
    tb.reply_to(message, "noti mode ON!")
    chat_id = message.chat.id

    if collection is not None:
        while True:
            query = { 'ts': { '$gt': last_ts } }
            cursor =  db.oplog.rs.find(query, cursor_type = CursorType.TAILABLE_AWAIT, oplog_replay=True)
            print 'cursor created.'
            while cursor.alive:
                print 'polling...'
                try:
                    log = cursor.next()
                    print 'got doc'
                    print log
                    
                    doc = log['o']
                    if doc.get('state') == 'Running':
                        for movie in doc['moviename']:
                            tb.send_message(chat_id, "date : %s, movie : %s" % (doc['date'], movie))
                except StopIteration:
                    time.sleep(1)

    print 'exit from send_welcome'
tb.polling(False)

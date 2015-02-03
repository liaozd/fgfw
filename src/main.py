#!/usr/bin/python
import time

from listener import listener
from puller import puller
from pusher import pusher

import thread

__author__ = 'liao_zd@hotmail.com'

'''
 +----------+                  
 | litsener +-----+            
 +----------+     |            
                +-v+           
          +-----+DB+---+       
          |     +--+   |       
          |            |       
          |            |       
+---------+---+        |       
|   Puller    |      +-+------+
| get new URL +------> Pusher |
+-------------+      |   To   |
                     | Youku  |
                     +--------+
'''

listener_sleeptime = 450
puller_sleeptime = 500
pusher_sleeptime = 350

try:
    thread.start_new_thread(listener, (10, listener_sleeptime,))
    time.sleep(0.5)
    thread.start_new_thread(puller, (puller_sleeptime,))
    time.sleep(0.5)
    thread.start_new(pusher, (pusher_sleeptime,))
except:
   print "Error: unable to start thread"

while 1:
   pass
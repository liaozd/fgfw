#!/usr/bin/python

__author__ = 'liao'
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


from listener import listener
from puller import puller
from pusher import pusher

import thread
try:
    thread.start_new_thread(listener, (10, 400,))
    thread.start_new_thread(puller, (500,))
    thread.start_new(pusher, (360,))
except:
   print "Error: unable to start thread"

while 1:
   pass
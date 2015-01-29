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
+-------------+ Trig |   To   |
                     | Youku  |
                     +--------+
'''

import thread
import time

from listener import listener

listener(15)

# try:
#     thread.start_new_thread(print_time, ("Thread-1", 2,))
#     # thread.start_new_thread(print_time, ("Thread-2", 4,))
# except:
#    print "Error: unable to start thread"
#
# while 1:
#    pass
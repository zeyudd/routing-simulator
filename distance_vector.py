#!/usr/bin/env python3

# Programming assignment 3: implementing distributed, asynchronous,
#                           distance vector routing.
#
# THIS IS THE MAIN ROUTINE.  IT SHOULD NOT BE TOUCHED AT ALL BY STUDENTS!

import random

from utils import LINKCHANGES, TRACE, YES, NO, \
                  FROM_LAYER2, LINK_CHANGE, \
                  Rtpkt, Event, evlist, clocktime, insertevent
from node0 import rtinit0, rtupdate0, linkhandler0
from node1 import rtinit1, rtupdate1, linkhandler1
from node2 import rtinit2, rtupdate2
from node3 import rtinit3, rtupdate3


# ***************** NETWORK EMULATION CODE STARTS BELOW ***********
# The code below emulates the layer 2 and below network environment:
#   - emulates the tranmission and delivery (with no loss and no
#     corruption) between two physically connected nodes
#   - calls the initializations routines rtinit0, etc., once before
#     beginning emulation
#
# THERE IS NOT REASON THAT ANY STUDENT SHOULD HAVE TO READ OR UNDERSTAND
# THE CODE BELOW.  YOU SHOLD NOT TOUCH, OR REFERENCE (in your code) ANY
# OF THE DATA STRUCTURES BELOW.  If you're interested in how I designed
# the emulator, you're welcome to look at the code - but again, you should have
# to, and you defeinitely should not have to modify
# ******************************************************************


def main():
    init()
    while evlist:
        event = evlist.pop(0)
        if TRACE > 1:
            print("MAIN: rcv event, t=%.3f, at %d" % (event.evtime, event.eventity))
            if event.evtype == FROM_LAYER2:
                print(" src:%2d," % event.rtpktptr.sourceid)
                print(" dest:%2d," % event.rtpktptr.destid)
                print(" contents: %3d %3d %3d %3d\n" %
                      (event.rtpktptr.mincost[0], event.rtpktptr.mincost[1],
                       event.rtpktptr.mincost[2], event.rtpktptr.mincost[3]))
        clocktime = event.evtime;    # update time to next event time

        if event.evtype == FROM_LAYER2:
            if event.eventity == 0:
                rtupdate0(event.rtpktptr)
            elif event.eventity == 1:
                rtupdate1(event.rtpktptr)
            elif event.eventity == 2:
                rtupdate2(event.rtpktptr)
            elif event.eventity == 3:
                rtupdate3(event.rtpktptr)
            else:
                print("Panic: unknown event entity\n")
                exit(0)
        elif event.evtype == LINK_CHANGE:
            if (clocktime<10001.0):
                linkhandler0(1,20)
                linkhandler1(0,20)
            else:
                linkhandler0(1,1)
                linkhandler1(0,1)
        else:
            print("Panic: unknown event type\n")
            exit(0)
        #print(event)
        #input()
        if event.evtype == FROM_LAYER2:
            del event.rtpktptr        # free memory for packet, if any
        del event                     # free memory for event struct


    print("\nSimulator terminated at t=%f, no packets in medium\n" % clocktime);


# initialize the simulator
def init():
    #int i
    #float sum, avg
    #struct event *evptr;
    
    global TRACE

    TRACE = int(input("Enter TRACE:"))

    random.seed(9999)              # init random number generator
    clocktime = 0.0                # initialize time to 0.0
    rtinit0()
    rtinit1()
    rtinit2()
    rtinit3()

    # initialize future link changes
    if LINKCHANGES == 1:
        event = Event(evtime=10000.0,
                      evtype=LINK_CHANGE,
                      eventity=-1,
                      rtpktptr=None)
        insertevent(event)
        event = Event(evtime=20000.0,
                      evtype=LINK_CHANGE,
                      eventity=-1,
                      rtpktptr=None)
        insertevent(event)

if __name__ == '__main__':
    main()

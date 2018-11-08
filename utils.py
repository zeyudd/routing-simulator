#!/usr/bin/env python3
import random
import copy

LINKCHANGES = 1

TRACE = 1;             # for my debugging
YES = 1;
NO = 0;

evlist = []   # the event list
clocktime = 0.000

# a rtpkt is the packet sent from one routing update process to
# another via the call tolayer3()
class Rtpkt:
    #sourceid       # id of sending router sending this pkt
    #destid         # id of router to which pkt being sent
                   # (must be an immediate neighbor)
    #mincost[4]     # min cost to node 0 ... 3

    def __init__(self, srcid, destid, mincost):
        self.sourceid = srcid
        self.destid = destid
        self.mincost = mincost[:4]

    def __repr__(self):
        return (#'Packet Object:\n'
                '    Source ID: %s\n'
                '    Destination ID: %s\n'
                '    Cost: %s\n' % (self.sourceid, self.destid, self.mincost))

class Event:
    #evtime           # event time
    #evtype             # event type code
    #eventity           # entity where event occurs

    #rtpkt *rtpktptr # ptr to packet (if any) assoc w/ this event
    def __init__(self, evtime=None, evtype=None, eventity=None, rtpktptr=None):
        self.evtime = evtime
        self.evtype = evtype
        self.eventity = eventity
        self.rtpktptr = rtpktptr

    def __repr__(self):
        return ('Event Object:\n'
                '  Time: %s\n'
                '  Type: %s\n'
                '  Entity: %s\n'
                '  Packet: \n%s\n' % (self.evtime, self.evtype,
                                      self.eventity, self.rtpktptr))

# possible events:
FROM_LAYER2 = 2
LINK_CHANGE = 10



#********************* EVENT HANDLINE ROUTINES *******
#*  The next set of routines handle the event list   *
#*****************************************************
def insertevent(p):
    # struct event *p;
    # struct event *q,*qold;
    if TRACE > 3:
        print("            INSERTEVENT: time is %lf\n" % clocktime)
        print("            INSERTEVENT: future time will be %lf\n" % p.evtime)

    evlist.append(p)
    evlist.sort(key=lambda e: e.evtime)

def printevlist():
    print("--------------\nEvent List Follows:\n")
    for event in evlist:
        print("Event time: %f, type: %d entity: %d\n" % (event.evtime, event.evtype, event.eventity))
    print("--------------\n")


# ************************** TOLAYER2 ***************
def tolayer2(packet):
    connectcosts = [[0 for j in range(4)] for i in range(4)]

    # initialize by hand since not all compilers allow array initilization
    connectcosts[0][0]=0;  connectcosts[0][1]=1;  connectcosts[0][2]=3;
    connectcosts[0][3]=7;
    connectcosts[1][0]=1;  connectcosts[1][1]=0;  connectcosts[1][2]=1;
    connectcosts[1][3]=999;
    connectcosts[2][0]=3;  connectcosts[2][1]=1;  connectcosts[2][2]=0;
    connectcosts[2][3]=2;
    connectcosts[3][0]=7;  connectcosts[3][1]=999;  connectcosts[3][2]=2;
    connectcosts[3][3]=0;

    # be nice: check if source and destination id's are reasonable
    if (packet.sourceid < 0) or (packet.sourceid > 3):
        print("WARNING: illegal source id in your packet, ignoring packet!\n")
        return
    if (packet.destid < 0) or (packet.destid > 3):
        print("WARNING: illegal dest id in your packet, ignoring packet!\n")
        return
    if (packet.sourceid == packet.destid):
        print("WARNING: source and destination id's the same, ignoring packet!\n")
        return
    if (connectcosts[packet.sourceid][packet.destid] == 999):
        print(packet)
        print("WARNING: source and destination not connected, ignoring packet!\n")
        return

    # make a copy of the packet student just gave me since he/she may decide
    # to do something with the packet after we return back to him/her
    mypktptr = copy.deepcopy(packet)
    if TRACE > 2:
        print("    TOLAYER2: source: %d, dest: %d\n              costs:" %
              (mypktptr.sourceid, mypktptr.destid))
        for i in range(4):
            print("%d  " % (mypktptr.mincost[i]))
        print("\n")

    # create future event for arrival of packet at the other side
    evptr = Event(evtype=FROM_LAYER2, eventity=packet.destid, rtpktptr=mypktptr)

    # finally, compute the arrival time of packet at the other end.
    # medium can not reorder, so make sure packet arrives between 1 and 10
    # time units after the latest arrival time of packets
    # currently in the medium on their way to the destination
    lastime = clocktime
    for q in evlist:
        if ( (q.evtype == FROM_LAYER2)  and (q.eventity == evptr.eventity) ):
            lastime = q.evtime
    evptr.evtime =  lastime + 2. * random.uniform(0, 1)


    if TRACE > 2:
        print("    TOLAYER2: scheduling arrival on other side\n")
    insertevent(evptr)

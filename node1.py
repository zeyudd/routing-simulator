from utils import TRACE, YES, NO, Rtpkt, tolayer2


class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt = DistanceTable()
connectcosts1 = [1,  0,  1, 999]

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [1, 0, 1, 999]
node_id = 1
node_dv = edges
neighbor_id = [i for i in range(4) if edges[i]>0 and edges[i]<999]

def rtinit1():
    for i in range(4):
        for j in range(4):
            if j == node_id:
                dt.costs[i][j] = edges[i]
            else:
                dt.costs[i][j] = 999       
    for i in neighbor_id:
        packet = Rtpkt(node_id, i, node_dv)
        tolayer2(packet)
    print("rt%d: initializing, distance vector %s sent to neighbors\n" % 
            (node_id, node_dv))


def rtupdate1(rcvdpkt):
    global node_dv
    src_id, dst_id, src_dv = rcvdpkt.sourceid, rcvdpkt.destid, rcvdpkt.mincost
    print("rt%d: received packet from rt%d with distance vector %s" 
            % (node_id, src_id, src_dv))
    if src_id not in neighbor_id:
        print("WARNING: illegal src id in received packet, ignoring packet!\n")
        return
    if dst_id != node_id:
        print("WARNING: illegal dst id in received packet, ignoring packet!\n")
        return
    dt_update = False    
    for i in range(4):
        cost = src_dv[i] + edges[src_id]
        if cost > 999:
            cost = 999
        if dt.costs[i][src_id] != cost:
            dt_update = True
            dt.costs[i][src_id] = cost
    if(dt_update):
        print("rt%d: distance table changed to" % node_id)
        printdt1(dt)
    else:
        print("rt%d: distance table not changed" % node_id)
    new_dv = [min([dt.costs[i][j] for j in range(4)]) for i in range(4)]    
    if node_dv != new_dv:
        node_dv = new_dv
        for i in neighbor_id:
            packet = Rtpkt(node_id, i, node_dv)
            tolayer2(packet)
        print("rt%d: distance vector changed to %s and sent to neighbors\n" % 
                (node_id, node_dv))
    else:
        print("rt%d: distance vector not changed, no packets sent\n" % node_id)


def printdt1(dtptr):
    print("             via   \n")
    print("   D1 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n" % (dtptr.costs[0][0], dtptr.costs[0][2]))
    print("dest 2|  %3d   %3d\n" % (dtptr.costs[2][0], dtptr.costs[2][2]))
    print("     3|  %3d   %3d\n" % (dtptr.costs[3][0], dtptr.costs[3][2]))


def linkhandler1(linkid, newcost):
    '''called when cost from 0 to linkid changes from current value to newcost
    You can leave this routine empty if you're an undergrad. If you want
    to use this routine, you'll need to change the value of the LINKCHANGE
    constant definition in prog3.c from 0 to 1
    '''
    global edges, node_dv, dt
    print("rt%d: link to rt%d changed from %d to %d" %
            (node_id, linkid, edges[linkid], newcost))
    for i in range(4):
        dt.costs[i][linkid] = dt.costs[i][linkid] - edges[linkid] + newcost
    dt.costs[linkid][node_id] = newcost
    print("rt%d: distance table changed to" % node_id)
    printdt1(dt)
    edges[linkid] = newcost
    new_dv = [min([dt.costs[i][j] for j in range(4)]) for i in range(4)]    
    if node_dv != new_dv:
        node_dv = new_dv
        for i in neighbor_id:
            packet = Rtpkt(node_id, i, node_dv)
            tolayer2(packet)
        print("rt%d: distance vector changed to %s and sent to neighbors\n" % (node_id, node_dv))
    else:
        print("rt%d: distance vector not changed, no packets sent\n" % node_id)

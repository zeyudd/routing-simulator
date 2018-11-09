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


def rtupdate1(rcvdpkt):
    global node_dv, dt
    src_id, dst_id, src_dv = rcvdpkt.sourceid, rcvdpkt.destid, rcvdpkt.mincost
    if src_id not in neighbor_id:
        print("WARNING: illegal src id in received packet, ignoring packet!\n")
        return
    if dst_id != node_id:
        print("WARNING: illegal dst id in received packet, ignoring packet!\n")
        return
    for i in range(4):
        dt.costs[i][src_id] = src_dv[i] + edges[src_id]
    new_dv = [min(node_dv[i], dt.costs[i][src_id]) for i in range(4)]    
    if node_dv != new_dv:
        node_dv = new_dv
        for i in neighbor_id:
            packet = Rtpkt(node_id, i, node_dv)
            tolayer2(packet)


def printdt1(dtptr):
    print("             via   \n")
    print("   D1 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n" % (dtptr.costs[0][0], dtptr.costs[0][2]))
    print("dest 2|  %3d   %3d\n" % (dtptr.costs[2][0], dtptr.costs[2][2]))
    print("     3|  %3d   %3d\n" % (dtptr.costs[3][0], dtptr.costs[3][2]))


def linkhandler1(linkid, newcost):
    '''called when cost from 1 to linkid changes from current value to newcost
    You can leave this routine empty if you're an undergrad. If you want
    to use this routine, you'll need to change the value of the LINKCHANGE
    constant definition in prog3.c from 0 to 1
    '''
    global edges, node_dv, dt
    for i in range(4):
        dt.costs[i][linkid] = dt.costs[i][linkid] - edges[linkid] + newcost
    edges[linkid] = newcost
    new_dv = [min(node_dv[i], dt.costs[i][linkid]) for i in range(4)]    
    if node_dv != new_dv:
        node_dv = new_dv
        for i in neighbor_id:
            packet = Rtpkt(node_id, i, node_dv)
            tolayer2(packet)

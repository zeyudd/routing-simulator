from utils import TRACE, YES, NO, Rtpkt, tolayer2


class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt = DistanceTable()

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [3, 1, 0, 2]
node_id = 2

def rtinit2():
    pass

def rtupdate2(rcvdpkt):
    pass
    

def printdt2(dtptr):
  print("                via     \n")
  print("   D2 |    0     1    3 \n")
  print("  ----|-----------------\n")
  print("     0|  %3d   %3d   %3d\n" %
        (dtptr.costs[0][0], dtptr.costs[0][1], dtptr.costs[0][3]))
  print("dest 1|  %3d   %3d   %3d\n" %
        (dtptr.costs[1][0], dtptr.costs[1][1], dtptr.costs[1][3]))
  print("     3|  %3d   %3d   %3d\n" %
        (dtptr.costs[3][0], dtptr.costs[3][1], dtptr.costs[3][3]))

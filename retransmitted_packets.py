sample_interval = 10
interface="wlp3s0"
privateNet="10.12.0.0/16"


#import ipaddress
from scapy.all import *
from collections import Counter
ids=deque()    

def traffic_monitor_callback(pkt):
    #pkt.show()
    global ids
    if pkt.haslayer(TCP):
        seqID=pkt[TCP].seq
        #print(seqID)
        if seqID in ids:
            print("DUPLICATEEEE!")
            print(seqID)
        else:
            ids.append(pkt[TCP].seq)
	
    while(len(ids)>=50):
       ids.popleft()



def checkDuplicate(newPkt, oldPkt):
    pass
	
def getData():
    sniff(iface=interface, prn=traffic_monitor_callback, store=False,timeout=sample_interval)

    
print(getData())

    

#counting number of packets and bandwidth
#sample_interval = 5
interface="wlp3s0"
privateNet="10.12.0.0/16"

from netaddr import IPAddress, IPNetwork
from scapy.all import *
from collections import Counter


ids = deque()
traffic = Counter()

# You should probably use a cache for your IP resolutions
hosts = {}
packet_host={}
retransmittedPktHosts={}
combine=[] #number of packets dictionary and speed

def isInNetwork(ipadd):
    if IPAddress(ipadd) in IPNetwork(privateNet):
        return True
    return False

def human(num):
    for x in ['', 'k', 'M', 'G', 'T']:
        if num < 1024.: return "%3.1f %sB" % (num, x)
        num /= 1024.
    # just in case!
    return  "%3.1f PB" % (num)

def traffic_monitor_callback(pkt):
    if IP in pkt:
        pkt = pkt[IP]
        # You don't want to use sprintf here, particularly as you're
        # converting .len after that!
        # Here is the first place where you're happy to use a Counter!
        # We use a tuple(sorted()) because a tuple is hashable (so it
        # can be used as a key in a Counter) and we want to sort the
        # addresses to count mix sender-to-receiver traffic together
        # with receiver-to-sender
        intHost = ""
        if isInNetwork(pkt.src):
            intHost = pkt.src
        elif isInNetwork(pkt.dst):
            intHost = pkt.dst
        else:
            #print("both src and dst are not internal network packets. Weird...")
            intHost = "extIP"

        #counting number of packets    
        if intHost in packet_host:
            packet_host[intHost]+=1
        else:
            packet_host[intHost]=1

        traffic.update({tuple((intHost,None)):pkt.len})
        #traffic.update({tuple(sorted(map(atol, (pkt.src, pkt.dst)))): pkt.len})


	#get number of retransmitted packets
	global ids
	if pkt.haslayer(TCP):
		seqID=pkt[TCP].seq
		if seqID in ids:
			#print("DUPLICATEEEE!")
			if intHost in retransmittedPktHosts:
				retransmittedPktHosts[intHost] += 1
			else:
				retransmittedPktHosts[intHost] = 1
		else:
			ids.append(pkt[TCP].seq)

	while (len(ids)>=100):
		ids.popleft()

        
       
    
        #return 'Packet #{}: {} ==> {}'.format(counter, packet[0][1].src, packet[0][1].dst)

def start_sniffing():
	sniff(iface=interface, prn=traffic_monitor_callback, store=False,
	      timeout=sample_interval)

	print 'started running'
	toReturnSpeed = []
	toReturnHost = []
	toReturnCounter = []
	for host, total in traffic.most_common(10):
	    host,_ = host
	    toReturnHost.append(host)
	    toReturnSpeed.append(human(float(total)/sample_interval))
	    print "%s/s: %s" % (human(float(total)/sample_interval), host)

	for host,counter in packet_host.iteritems():
	    toReturnCounter.append(counter)
	    print host,counter

	
	return toReturnSpeed, toReturnHost, toReturnCounter


def getData(sample_interval):
 
    sniff(iface=interface, prn=traffic_monitor_callback, store=False,timeout=sample_interval)
 
 
    #compute and combien results of bandwidth
    for host, total in traffic.most_common(10):
        host,_ = host
        rate = human(float(total)/sample_interval)
        hosts[host]=rate
        #print "%s/s: %s" % (rate,host)
   
 
    #We combine the outputs into one list
    # [{"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt, "retransCount":someInt},
    #  {"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt, "retransCount":someInt},
    #  {"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt, "retransCount":someInt}]
 
    combinedOutput= []
    for host,counter in packet_host.items():
        combinedOutput.append({"type":"host","ip":host,"packetCount":counter,"bandwidth":"0"})
 
    for host,bandwidth in hosts.items():
       
        #If host is already in combined output, merely append the bandwidth to it.
        #otherwise, add a new line
        addNewLine = True
        for storedHost in combinedOutput:
            if host == storedHost['ip']:
                storedHost['bandwidth']=bandwidth+"/s"
                addNewLine=False
       
        if addNewLine:
            combinedOutput.append({"type":"host","ip":host,"packetCount":0,'bandwidth':bandwidth})
 
    for host,retransCount in retransmittedPktHosts.items():
       
        #If host is already in combined output, merely append the bandwidth to it.
        #otherwise, add a new line
        addNewLine = True
        for storedHost in combinedOutput:
            if host == storedHost['ip']:
                storedHost['retransCount']=retransCount
                addNewLine=False
       
        if addNewLine:
            combinedOutput.append({"type":"host","ip":host,"packetCount":0,'bandwidth':"0B/s"})
 
    return combinedOutput

# combine=[,packet_host]
# print combine


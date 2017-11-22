from flask import Flask, url_for, send_from_directory, request
from copy import deepcopy
from flask import render_template
from combined import getData
import os
app = Flask(__name__)

hostList = []
duration = 5
@app.route('/')
def api_root():
	
	global duration
	hosts=[]
	counters=[]
	context = {'hosts': hosts,  'counters': counters, "duration":duration}
    	return render_template('home.html', **context)

@app.route('/monitor/',methods=['POST'])
def start_monitoring():
	global hostList
	global duration
	newDuration = request.form["newDuration"]
	print(newDuration)
	if newDuration:
		duration = int(newDuration)
	listOfHosts=getData(duration)
	print(listOfHosts)
	hostList = deepcopy(listOfHosts)
	context = []
	#if listOfHosts:
	#	context = listOfHosts
	hosts= []
	counters=[]
	hostData = []
	bandwidths=[]
	bandwidthData = []
	bandwidthconv={'k':1000,'M':1000000,'G':1000000000,'T':1000000000000}
	for gottenHost in listOfHosts:
		hostString = ""
		individualBandwidth = ""
		if "ip" in gottenHost:
			hosts.append(gottenHost["ip"])
			hostString = hostString+gottenHost['ip']
			individualBandwidth += gottenHost['ip'] + ": "
		else:
			hosts.append("externalip")
			hostString = hostString+'externalIP'
		if "packetCount" in gottenHost:
			counters.append(gottenHost["packetCount"])
			hostString = hostString+"\n  packetCount: "+str(gottenHost['packetCount'])
		else:
			counters.append(0)
			hostString = hostString+"\n  packetCount: -"
		#parse the dictionary for neater labels
		if 'type' in gottenHost:
			hostString = hostString+"\n  type: "+gottenHost['type']
		if 'bandwidth' in gottenHost:
			bandwidth_string=gottenHost["bandwidth"].strip('B/s')
			if bandwidth_string[-1] in bandwidthconv:
				bandwidth_num=bandwidthconv[bandwidth_string[-1]]*float(bandwidth_string[:-1])
			elif bandwidth_string[-1].isdigit():
				bandwidth_num=float(bandwidth_string)
			else:
				bandwidth_num=0
			
			bandwidths.append(bandwidth_num)
			hostString = hostString+"\n  bandwidth: "+gottenHost['bandwidth']
			individualBandwidth += gottenHost['bandwidth']
		else:
			bandwidths.append(0)
			hostString = hostString+"\n  bandwidth: -"
		if 'retransCount' in gottenHost:
			hostString = hostString+"\n  retransCount: "+str(gottenHost['retransCount'])

		hostData.append(hostString)
		bandwidthData.append(individualBandwidth)

    # [{"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt, "retransCount":someInt},
    #  {"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt, "retransCount":someInt},
    #  {"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt, "retransCount":someInt}]

	context = {'hosts': hosts, 'bandwidths':bandwidths, 'counters': counters, 'hostData':hostData, 'duration':duration, "hostData2":listOfHosts, "bandwidthData": bandwidthData}
    	return render_template('home.html', **context)	
	


@app.route('/host/')
#@app.route('/host/<hostid>')
#def display_host_detail(hostid=None):
def display_host_detail():
	hostid = request.args.get("hostsIndex")
	global duration

    	return render_template('host.html', hostid=hostList[int(hostid)], duration=duration)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, "uploads")
    return send_from_directory(directory=uploads, filename=filename)



if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)


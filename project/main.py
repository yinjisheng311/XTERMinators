from flask import Flask, url_for, send_from_directory, request
from copy import deepcopy
from flask import render_template
from combined import getData
import os
app = Flask(__name__)

hostList = []
@app.route('/')
def api_root():
	
	hosts=[]
	counters=[]
	context = {'hosts': hosts,  'counters': counters}
    	return render_template('home.html', **context)

@app.route('/monitor/',methods=['POST'])
def start_monitoring():
	listOfHosts=getData()
	global hostList
	hostList = deepcopy(listOfHosts)
	context = []
	if listOfHosts:
		context = listOfHosts
	hosts= []
	counters=[]
	for gottenHost in listOfHosts:
		hosts.append(gottenHost["ip"])
		if gottenHost["packetCount"]:
			counters.append(gottenHost["packetCount"])
		else:
			counters.append(0)
    # [{"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt},
    #  {"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt},
    #  {"type":"host","ip":"ipadd,"bandwidth":"some_speed","packetCount":someInt}]
#	speeds,hosts,counters=start_sniffing()
	context = {'hosts': hosts,  'counters': counters}
    	return render_template('home.html', **context)	
	


@app.route('/host/')
#@app.route('/host/<hostid>')
#def display_host_detail(hostid=None):
def display_host_detail():
	hostid = request.args.get("hostsIndex")

    	return render_template('host.html', hostid=hostList[int(hostid)])

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, "uploads")
    return send_from_directory(directory=uploads, filename=filename)



if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)


from flask import Flask, url_for
from flask import render_template
from combined import start_sniffing
app = Flask(__name__)

@app.route('/')
def api_root():
	
	hosts=[]
	counters=[]
	context = {'hosts': hosts,  'counters': counters}
    	return render_template('home.html', **context)

@app.route('/monitor/',methods=['POST'])
def start_monitoring():
	speeds,hosts,counters=start_sniffing()
	context = {'hosts': hosts,  'counters': counters}
    	return render_template('home.html', **context)	
	


@app.route('/host/')
@app.route('/host/<hostid>')
def display_host_detail(hostid=None):

    	return render_template('host.html', hostid=hostid)

if __name__ == '__main__':
    app.run()


import datetime
import json
import uuid
from flask import Flask, render_template, request

# MPD Stuff
import mpd

HOST = 'carmen'
PORT = '6600'


class Model(object):
    def __init__(self, host, port):
        self.client = mpd.MPDClient(host, port)
        self.last_search_results = {}

    def next(self): self.client.next()
    def play(self): self.client.play()
    def previous(self): self.client.previous()
    def stop(self): self.client.stop()

    def search(self, type, what):
        results = self.client.search(type, what)
        for result in results:
            if 'title' not in result:
                result['title'] = "NO TITLE"
            if 'artist' not in result:
                result['artist'] = ''
        self.last_search_results = results
        return results
    def status(self):
        status = self.client.status()
        return status

    def playlistinfo(self):
        return self.client.playlistinfo()
MODEL = Model(HOST, PORT)
# Flask Code
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    print "Playing thing..."
    MODEL.play()
    return ''

@app.route('/stop', methods=['POST'])
def stop():
    MODEL.stop()
    return ''

@app.route('/next', methods=['POST'])
def next():
    MODEL.next()
    return ''

@app.route('/prev', methods=['POST'])
def prev():
    MODEL.previous()
    return ''

@app.route('/search', methods=['GET','POST'])
def search():
    print "Search"
    search_type = 'any'
    search_term = request.args.get('q', None)

    results = MODEL.search(search_type, search_term) if search_term else MODEL.last_search_results
    
    return render_template('search_results.html', results=results)

@app.route('/playlist', methods=['GET'])
def playlist():
    print "PL"
    return json.dumps(MODEL.playlistinfo())


@app.route('/status', methods=['GET'])
def status():
    status = MODEL.status()
    print status
    return json.dumps(status)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

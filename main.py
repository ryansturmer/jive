import datetime
import json
import uuid
from flask import Flask, render_template, request, redirect

# MPD Stuff
import mpd

HOST = 'carmen'
PORT = '6600'

def normalize(d, mapping):
    for key, alts in mapping.items():
        if key not in d or not d[key]:
            for alt in alts:
                if alt in d and d[alt]:
                    d[key] = d[alt]
        if key not in d:
            d[key] = "No %s" % key.capitalize()

def fmt_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return '%d:%d:%02d' % (hours, minutes, seconds)
    else:
        return '%d:%02d' % (minutes, seconds)

class Model(object):
    def __init__(self, host, port):
        self.last_search_results = {}
        self.last_search = (None, None)
        self.host, self.port = (host, port)

    def next(self): 
        with mpd.connect(self.host, self.port) as client:
            client.next()
    def play(self): 
        with mpd.connect(self.host, self.port) as client:
            client.play()
    
    def previous(self): 
        with mpd.connect(self.host, self.port) as client:
            client.previous()
    def stop(self): 
        with mpd.connect(self.host, self.port) as client:
            client.stop()

    def setvol(self,x): 
        with mpd.connect(self.host, self.port) as client:
            client.setvol(x)
    
    def search(self, type, what):
        self.last_search = (type, what)
        with mpd.connect(self.host, self.port) as client:
            results = client.search(type, what)
        results = [x for x in results if 'file' in x and x['file'].strip() != '']
        for result in results:
            normalize(result, {'title' : ('file',)})
        self.last_search_results = results
        return results
    
    def status(self):
        with mpd.connect(self.host, self.port) as client:
            status = client.status()
        try:
            a,b = status.pop('time')
            status['time'] = a.seconds
            status['duration'] = b.seconds
        except:
            pass
        return status

    def playlistinfo(self):
        with mpd.connect(self.host, self.port) as client:
            info = client.playlistinfo()
        info = [item for item in info if item]
        for item in info:
            normalize(item, {'title' : ('file',)})
            item['duration'] = fmt_time(item['time'])
        return info

    def listplaylists(self):
        with mpd.connect(self.host, self.port) as client:
            info = client.listplaylists()
        return info

    def add(self, *songs):
        with mpd.connect(self.host, self.port) as client:
            for song in songs:
                client.add(song)
    def clear(self):
        with mpd.connect(self.host, self.port) as client:
            client.clear()
    def delete(self, song):
        with mpd.connect(self.host, self.port) as client:
            client.delete(song)

    def load(self, song):
        with mpd.connect(self.host, self.port) as client:
            client.load(song)

    def currentsong(self):
        with mpd.connect(self.host, self.port) as client:
            return client.currentsong()
HOST = '192.168.1.146'
PORT = '6600'
MODEL = Model(HOST, PORT)
# Flask Code
app = Flask(__name__)

@app.route('/')
def index():
    playlist = MODEL.playlistinfo()
    status = MODEL.status()
    print status
    return render_template('index.html', playlist=playlist, status=status)

@app.route('/kindle')
def kindle():
    playlist = MODEL.playlistinfo()
    status = MODEL.status()
    return render_template('kindle.html', playlist=playlist, status=status)

@app.route('/play', methods=['POST'])
def play():
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

@app.route('/setvol', methods=['POST'])
def setvol():
    try:
        vol = request.form['volume']
    except KeyError, e:
        raise e
    MODEL.setvol(vol)
    return ''
@app.route('/song_delete', methods=['POST'])
def song_delete():
    try:
        song = request.form['song']
    except KeyError, e:
        raise e
    print song
    MODEL.delete(song)
    return ''
@app.route('/clear_playlist', methods=['POST'])
def clear_playlist():
    MODEL.clear()
    return ''

@app.route('/load_playlist', methods=['POST'])
def load_playlist():
    MODEL.load(request.form['playlist'])
    return ''

@app.route('/search', methods=['GET','POST'])
def search():
    search_type = 'any'
    search_term = request.args.get('q', None)
    results = MODEL.search(search_type, search_term) if search_term else MODEL.last_search_results
    for result in results:
        result['file'] = result['file'].replace("'", "\\'")
    return render_template('search_results.html', results=results)

@app.route('/add', methods=['POST'])
def add():
    for item in request.form:
        MODEL.add(item)
    return json.dumps(MODEL.status())

@app.route('/playlist', methods=['GET'])
def playlist():
    info = MODEL.playlistinfo()
    return json.dumps(info)

@app.route('/playlists', methods=['GET'])
def playlists():
    results = MODEL.listplaylists()
    return render_template('playlists.html', results=results)

@app.route('/status', methods=['GET'])
def status():
    status = MODEL.status()
    return json.dumps(status)

@app.route('/now_playing', methods=['GET'])
def now_playing():
    p = MODEL.currentsong()
    return json.dumps(p)

@app.route('/shuffle', methods=['POST'])
def shuffle():
    MODEL.client.shuffle()
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

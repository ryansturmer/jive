import datetime
import json
import uuid
import urllib
from flask import Flask, render_template, request, redirect, Markup

import mpd
from util import Timer, fmt_time, get_config, normalize
from model import JiveModel

CONFIG = get_config()
MODEL = JiveModel(CONFIG.get('mpd', 'host'), CONFIG.get('mpd', 'port'))

# Flask Code
app = Flask(__name__)
@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)

@app.route('/')
def index():
    playlist = MODEL.playlistinfo()
    status = MODEL.status()
    return render_template('index.html', playlist=playlist, status=status)

@app.route('/play', methods=['POST'])
def play():
    MODEL.play()
    return ''

@app.route('/pause', methods=['POST'])
def pause():
    MODEL.pause()
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
    status = MODEL.status()

    for result in results:
        result['file'] = result['file'].replace("'", "\\'")
    return render_template('search_results.html', results=results, status=status)

@app.route('/browse', methods=['GET'])
def browse():
    location = request.args.get('dir', '/')
    status = MODEL.status()
    listing = MODEL.list(location)
    dirs = location.split('/')
    path = [('','')]
    for dir in dirs:
         path.append((dir, (path[-1][1] + '/' + dir).strip('/')))
    path[0] = ('', '/')
    path = [p for p in path if p != ('','')]
    return render_template('browser.html',status=status, listing=listing, path=path)

@app.route('/add', methods=['POST'])
def add():
    print request.form
    for item in request.form:
        print item
        MODEL.add(item)
    return json.dumps(MODEL.status())

@app.route('/playlist', methods=['GET'])
def playlist():
    info = MODEL.playlistinfo()
    return json.dumps(info)

@app.route('/playlists', methods=['GET'])
def playlists():
    results = MODEL.listplaylists()
    status = MODEL.status()

    return render_template('playlists.html', results=results, status=status)

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
    app.run(host='0.0.0.0', port=CONFIG.getint('jive', 'port'), debug=True)

import datetime
import json
import uuid
from flask import Flask, render_template, request

# MPD Stuff
import mpd

HOST = 'carmen'
PORT = '6600'

MODEL = mpd.MPDClient(HOST, PORT)
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

@app.route('/db_search', methods=['POST'])
def db_search():
    search_type = 'any'
    search_term = request.form['text']
    results = MODEL.find(search_type, search_term)
    return json.dumps(results)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

import datetime
import json
import uuid
from flask import Flask, render_template, request

class Post(object):
    def __init__(self, text):
        self.uuid = uuid.uuid4().hex
        self.timestamp = datetime.datetime.now()
        self.text = text

class Model(object):
    def __init__(self):
        self.posts = []
        self.posts_by_uuid = {}
    def add_post(self, post):
        self.posts.append(post)
        self.posts_by_uuid[post.uuid] = post
    def get_posts_since(self, uuid):
        if uuid in self.posts_by_uuid:
            ref = self.posts_by_uuid[uuid]
            posts = [post for post in self.posts if post.timestamp > ref.timestamp]
        else:
            posts = self.posts
        return sorted(posts, cmp=cmp_timestamp, reverse=True)

MODEL = Model()

# Flask Code
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_posts')
def _posts():
    uuid = request.args['since']
    posts = MODEL.get_posts_since(uuid)
    html = render_template('posts.html', posts=posts)
    since = posts[0].uuid if posts else ''
    return json.dumps({
        'html': html, 
        'since': since,
        'count': len(posts),
    })

@app.route('/_add_post', methods=['POST'])
def _add_post():
    text = request.form['text']
    if text:
        post = Post(text)
        MODEL.add_post(post)
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

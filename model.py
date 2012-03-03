from util import fmt_time, normalize
import mpd

class JiveModel(object):
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
    def pause(self): 
        with mpd.connect(self.host, self.port) as client:
            client.pause()
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
            current_song = client.currentsong()
        try:
            a,b = status.pop('time')
            status['time'] = a.seconds
            status['duration'] = b.seconds
            status['title'] = current_song['title']
            status['artist'] = current_song['artist']
        except:
            pass
        return status

    def playlistinfo(self):
        with mpd.connect(self.host, self.port) as client:
            info = client.playlistinfo()
        info = [item for item in info if item]
        for item in info:
            normalize(item, {'title' : ('file',), 'artist' : tuple()})
            item['duration'] = fmt_time(item.get('time', 0))
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
            current_song = client.currentsong()
        normalize(current_song, {'title' : ('file',), 'artist' : tuple()})
        return current_song

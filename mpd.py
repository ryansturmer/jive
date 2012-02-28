import socket
import datetime
import threading

def timestamp(t):
    return datetime.datetime.fromtimestamp(float(t))

def duration(t):
    return datetime.timedelta(seconds=int(t))

def time(t):
    a,b = t.split(":")
    return datetime.timedelta(seconds=int(a)), datetime.timedelta(seconds=int(b))

MPD_TYPES = {'file' : str,
             'volume': int,
             'repeat': bool,
             'random' : bool,
             'single' : bool,
             'consume' : bool,
             'playlistlength' : int,
             'state': str,
             'songid': int,
             'nextsongid': int,
             'song': int,
             'nextsong': int,
             'pos': int,
             'uptime' : duration,
             'artists' : int,
             'playtime' : duration,
             'db_playtime' : duration,
             'songs' : int,
             'db_update' : timestamp,
             'id' : int,
             'time' : int,
             'mixrampdb' : float
             }


def parse_lines(lines, types):
    types = types or {}
    retval = [dict()]
    for line in lines:
        toks = line.split(':')
        key = unicode(toks[0].lower().strip())
        type_lookup = types if key in types else MPD_TYPES
        try:
            value = type_lookup.get(key, unicode)((':'.join(toks[1:])).strip())
            if isinstance(value, str):
                value = unicode(value)
        except ValueError:
            print "Problem Parsing %s" % key
            print "  -> %s" % value
        if key in retval[-1]:
            retval.append(dict())
        retval[-1][key] = value
    return retval

def cmd_from_function(f, *args):
    def scrub(arg):
        if isinstance(arg, str) or isinstance(arg, unicode):
            return '"%s"' % arg.replace('"', '\"')
        else:
            return str(arg)
    return ('%s %s' % (f.__name__, ' '.join(map(scrub, args)))).strip()

# Decorator that makes a magical MPD command
def mpd_command(returns=None, types=None):
    def enforce_returns(f, *args, **kwargs):
        if returns is list:
            def f_list(self, *args, **kwargs):
                return parse_lines(f(self, *args, **kwargs) or self.cmd(cmd_from_function(f, *args)), types=types)
            return f_list
        elif returns is dict:
            def f_dict(self, *args, **kwargs):
                return parse_lines(self.cmd(f(self, *args, **kwargs) or cmd_from_function(f, *args)), types=types)[0]
            return f_dict
        elif returns is int:
            def f_int(self, *args, **kwargs):
                return parse_lines(self.cmd(f(self, *args, **kwargs) or cmd_from_function(f, *args)), types=types)[0].pop()
            return f_int
        else:
            def f_none(self, *args, **kwargs):
                parse_lines(self.cmd( f(self, *args, **kwargs) or cmd_from_function(f, *args)), types=types)
            return f_none
    return enforce_returns

class MPDException(Exception): pass

class MPDClient(object):
    def __init__(self, hostname='localhost', port=6600):
        self.hostname = hostname
        self.port = port
        self.lock = threading.Lock()
        self.connect()

    def connect(self):
        self.socket = socket.create_connection((self.hostname, self.port))
        msg = self.__recv()
        ok,mpd, version = msg.split()
        if mpd != 'MPD' or ok != 'OK':
            raise MPDException("Malformed welcome from MPD server: '%s'" % msg)
        self.version = version

    def cmd(self, cmd):
        self.__send(cmd + '\n' if not cmd.endswith('\n') else cmd)
        lines = []
        line = []
        done = False
        self.lock.acquire()
        while True:
            for c in self.__recv():
                if c == '\n':
                    s = ''.join(line)
                    line = []
                    if s.startswith('ACK') or s.startswith('OK'):
                        if s.startswith('ACK'):
                            raise Exception(s)
                        done = True
                        break
                    lines.append(s)
                else:
                    line.append(c)
            if done:
                break
        self.lock.release()
        return lines

    def __send(self, data):
        return self.socket.send(data)
    def __recv(self):
        return self.socket.recv(4096)

    # Querying MPD's status
    @mpd_command
    def clearerror(self):pass
    
    @mpd_command(returns=dict)
    def currentsong(self):pass

    @mpd_command
    def idle(self):pass
    
    @mpd_command(returns=dict, types={'playlist': int, 'time':time})
    def status(self): pass

    @mpd_command(returns=dict)
    def stats(self): pass
    
    # Playback Options
    @mpd_command(returns=None)
    def consume(self, state): pass

    @mpd_command(returns=None)
    def crossfade(self, seconds): pass

    @mpd_command(returns=None)
    def mixrampdelay(self, seconds): pass

    @mpd_command(returns=None)
    def random(self, state): pass

    @mpd_command(returns=None)
    def setvol(self, vol): pass

    @mpd_command(returns=None)
    def single(self, state): pass

    @mpd_command(returns=None)
    def replay_gain_mode(self, mode): pass

    @mpd_command(returns=dict)
    def replay_gain_status(self): pass

    # Controlling Playback
    @mpd_command(returns=None)
    def next(self): pass

    @mpd_command(returns=None)
    def pause(self, pause): pass

    @mpd_command(returns=None)
    def play(self, songpos=''): pass
    
    @mpd_command(returns=None)
    def playid(self, songid): pass

    @mpd_command(returns=None)
    def previous(self): pass

    @mpd_command(returns=None)
    def seek(self, songpos, time): pass

    @mpd_command(returns=None)
    def seekid(self, songid, time): pass

    @mpd_command(returns=None)
    def seekcur(self, time): pass

    @mpd_command(returns=None)
    def stop(self): pass

    # The Current Playlist
    @mpd_command(returns=None)
    def add(self, uri): pass

    #@mpd_command(returns=int)
    #def add(self, uri, position=''): pass

    @mpd_command(returns=None)
    def clear(self):pass

    @mpd_command(returns=None)
    def delete(self, idx): pass

    @mpd_command(returns=None)
    def deleteid(self, id): pass

    @mpd_command(returns=None)
    def move(self, fro, to): pass

    @mpd_command(returns=list)
    def playlistfind(self, tag, needle): pass # Tag is a scope specifier: artist|album|title|track|name|genre|date|composer|performer|comment|disc

    @mpd_command(returns=list)
    def playlistid(self, songid): pass

    @mpd_command(returns=list)
    def playlistinfo(self): pass   #TODO Look at the 'track' field... wonder what's up with that?
   
    @mpd_command(returns=list)
    def playlistsearch(self, tag, needle): pass # See above for definition of tag

    @mpd_command(returns=list)
    def plchanges(self, version): pass

    @mpd_command(returns=list)
    def plchangesposid(self, version): pass

    @mpd_command(returns=None)
    def prio(self, priority, *ranges): pass

    @mpd_command(returns=None)
    def prioid(self, priority, *ids): pass

    @mpd_command(returns=None)
    def shuffle(self, range=''): pass

    @mpd_command(returns=None)
    def swap(self, a, b): pass

    @mpd_command(returns=None)
    def swapid(self, a, b): pass

    # Stored Playlists
    @mpd_command(returns=list)
    def listplaylist(self, name):pass

    @mpd_command(returns=list)
    def listplaylistinfo(self, name):pass

    @mpd_command(returns=list)
    def listplaylists(self):pass

    @mpd_command(returns=None)
    def load(self, name):pass

    # The music database
    @mpd_command(returns=list)
    def find(self, type, what): pass
    
    @mpd_command(returns=list)
    def search(self, type, what): pass

if __name__ == "__main__":
    client = MPDClient('carmen')
    print client.version
    print client.listplaylists()
    print client.currentsong()
    print client.status()
    stats = client.stats()
    playtime = stats['db_playtime']
    print stats
    client.socket.close()

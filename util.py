import time
import ConfigParser
import os

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


def get_config():
    CFG_FILE = 'jive.cfg'
    config = ConfigParser.RawConfigParser()
    config.add_section('jive')
    config.set('jive', 'port', 5000)
    config.add_section('mpd')
    config.set('mpd', 'host', 'localhost')
    config.set('mpd', 'port', 6600)
    if os.path.exists(CFG_FILE):
        config.read(CFG_FILE)
    else:
        print "No config file found.  Creating '%s' with the defaults." % CFG_FILE
        with open(CFG_FILE, 'w') as fp:
            config.write(fp)
    return config

class Timer(object):
    '''
    This is a timer used for debugging.  Use it like this:
    
    with Timer():
        do_some_work()

    When the code inside the with block finishes executing, the time elapsed
    will be printed to stdout.  A name may be optionally specified to indicate
    what is being timed.  If greater_than is specified, the timer will only
    print the elapsed time if it is greater than the value specified (in seconds)
    Similar for less_than.
    '''
    def __init__(self, name='', greater_than=None, less_than=None):
        self.name = name
        self.greater_than = greater_than
        self.less_than = less_than
    def __enter__(self):
        self.t1 = time.time()
    def __exit__(self, ex_type, ex_value, ex_tb):
        self.t2 = time.time()
        diff = self.t2-self.t1
        display = True
        if self.greater_than:
            if diff < self.greater_than:
                display = False
        if self.less_than:
            if diff > self.less_than:
                display = False
        
        if display:
            s = ("Time for %s: " % self.name) if self.name else ''
            if diff < 1.0:
                print "%s%g ms" % (s, round(diff*1000,1))
            else:
                print "%s%g s" % (s, round(diff, 2))
            return bool(ex_value)

if __name__ == "__main__":
    get_config()

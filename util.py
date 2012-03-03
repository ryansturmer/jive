import time

class Timer(object):
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
            s = "Time for %s: " if name else ''
            if diff < 1.0:
                print "%s%g ms" % (s, round(diff*1000,1))
            else:
                print "%s%g s" % (s, round(diff, 2))
            return bool(ex_value)

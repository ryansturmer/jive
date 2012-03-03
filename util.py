import time

class Timer(object):
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.t1 = time.time()
    def __exit__(self, ex_type, ex_value, ex_tb):
        self.t2 = time.time()
        diff = self.t2-self.t1
        if diff < 1.0:
            print "Time for %s: %g ms" % (self.name, round(diff*1000,1))
        else:
            print "Time for %s: %g s" % (self.name, round(diff, 2))
        return bool(ex_value)

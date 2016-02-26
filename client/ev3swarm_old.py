import rpyc
import marshal
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
import multiprocessing
from multiprocessing import Manager
import warnings

def mytask(bot):
    print "initializing"
    import random
    import time
    for n in range(0, 10):
        val = random.random() * n
        print str(val)
        bot.service.message(val)
        time.sleep(0.5)

class Ev3SwarmService(rpyc.Service):
    queue = multiprocessing.Queue()
    def exposed_message(self, val):
        queue.put(val)

c = rpyc.connect('192.168.43.68', port=12345, config = rpyc.core.protocol.DEFAULT_CONFIG, service=Ev3SwarmService)

import time
func = marshal.dumps(mytask.func_code)
print "about to start remote run"
c.root.run('10.0.0.1', func)
print "about to start queue dump"
for n in range(0, 40):
    print "dumping"
    while not Ev3SwarmService.queue.empty():
        print str(Ev3SwarmService.queue.get())
    time.sleep(0.25)

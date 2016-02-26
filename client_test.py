from ev3swarm import Swarm
import time
from multiprocessing import Process

def mytask(bot):
    import time
    import random
    print "hello from the outside"
    for n in range(0, 100):
        bot.log(random.random() * n)
        time.sleep(0.25)

def queueLogger():
    global s
    for n in range(0, 100):
        while not s.queue.empty():
            print str(s.queue.get())
        time.sleep(1)


print "Initializing swarm connection to broker"
s = Swarm('localhost')

print "Starting logger"
p = Process(target=queueLogger)
p.start()

print "Connecting to swarm"
s.connect(['localhost'])

print "Waiting for swarm acknowledgement"
time.sleep(2)

print "Sending task to swarm"
s.load_task(mytask)

print "Starting swarm"
s.go()


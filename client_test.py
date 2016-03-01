from ev3swarm import Swarm
import time
from multiprocessing import Process

def mytask(bot):
    print "Test task"

def queueLogger():
    global s
    for n in range(0, 100):
        while not s.queue.empty():
            print str(s.queue.get())
        time.sleep(1)


print "Initializing swarm connection to broker"
s = Swarm('192.168.43.106', 'robot', 'maker')

print "Starting logger"
p = Process(target=queueLogger)
p.start()

print "Connecting to swarm"
s.connect(['192.168.43.68', '192.168.43.149'])

print "Waiting for swarm acknowledgement"
time.sleep(2)

print "Sending task to swarm"
s.load_task(mytask)

print "Starting swarm"
s.go()

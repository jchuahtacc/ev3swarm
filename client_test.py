from ev3swarm import Swarm
import time
from multiprocessing import Process

def mytask(bot):
    import time
    import ev3dev.ev3 as ev3
    import os
    print "task process: " + str(os.getpid())
    m = ev3.LargeMotor('outA')
    m.run_timed(time_sp=3000, duty_cycle_sp=75)
    time.sleep(3000)

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
s.connect(['192.168.43.68'])

print "Waiting for swarm acknowledgement"
time.sleep(2)

print "Sending task to swarm"
s.load_task(mytask)

print "Starting swarm"
s.go()

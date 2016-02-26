import ev3swarm
import time

def mytask(bot):
    print "hello from the outside"
    for n in range(0, 10):
        bot.log("log " + str(n))

print "Connecting to swarm"
ev3swarm.connect(['localhost'], 'localhost')

print "Waiting for swarm acknowledgement"
time.sleep(2)

print "Init"
ev3swarm.init()
ev3swarm.load_task(mytask)
ev3swarm.go()

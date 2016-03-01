"""
simpleRobot.py
Author: jchuah@tacc.utexas.edu

An example of how to define a simple task, connect to a swarm and run the task on the swarm
"""

from ev3swarm import Swarm
import time

# Task to run on each host
def mytask(bot):
    # Assume that the method must do all of its own imports
    import ev3dev.ev3 as ev3
    import time
    m = ev3.LargeMotor('outA')
    m.run_forever(duty_cycle_sp=100)
    time.sleep(3)
    m.stop()

# Connect to a RabbitMQ broker. The address should be accessible to
# each ev3 robot host, so 'localhost' as an address is not a good option
print "Initializing swarm connection to broker"
s = Swarm('192.168.43.106')

# Connect to all of the hosts by IP address
print "Connecting to swarm"
s.connect(['192.168.43.68', '192.168.43.149'])

# Wait for acknowledgements
print "Waiting for swarm acknowledgement"
time.sleep(2)

# Broadcast the task to the swarm, and then wait again
print "Sending task to swarm"
s.load_task(mytask)
time.sleep(2)

# Trigger the swarm
print "Starting swarm"
s.go()

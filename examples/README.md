# ev3swarm examples

Make sure that you've completed the setup before you get started. Some basic concepts:

### RabbitMQ

RabbitMQ will be the message broker between your computer that is running `ev3swarm` and each `ev3host`. RabbitMQ is probably running on the machine you're coding on. That's fine. However, the hostname used when you create a Swarm object should be the IP address that you expect your robots to be able to connect to. So the following code is *bad*:

```python
from ev3swarm import Swarm

mySwarm = Swarm('localhost')
```

Instead, use your computer's IP address. Assuming it was `192.168.0.100`:

```python
from ev3swarm import Swarm
import time

mySwarm = Swarm('192.168.0.100')
```

### Tasks

A task is a method definition that will run simultaneously on each robot in the Swarm. It must accept one parameter called `bot` which provides access to logging. It needs to be completely self contained code, including imports. The good news is that you can nest methods in Python, so you won't even need globals. So you can have code that looks like this:

```python
def mySwarmTask(bot):
	import ev3dev.ev3 as ev3
	import time
	
	leftMotor = ev3.LargeMotor('outA')
	rightMotor = ev3.LargeMotor('outB')
	
	def spin():
		leftMotor.run_forever(duty_cycle_sp=100)
		rightMotor.run_forever(duty_cycle_sp=100)
		time.sleep(3)
		
	spin()
```

### Running your task on the Swarm

You can connect to a list of hostnames from your Swarm. After that, you can load the task, then make activate the Swarm. I recommend waiting a little between each step.

```python

hosts = ['192.168.0.101', '192.168.0.102', '192.168.0.103']
mySwarm.connect(hosts)

time.sleep(2)

mySwarm.load_task(mySwarmTask)

time.sleep(2)

mySwarm.go()

time.sleep(10)
```

### Messaging

The `bot` object passed to your swarm can log messages of any type that can be marshaled. They can be retrieved from the Swarm's message queue as a series of dictionaries with hostname and execution timestamp. I don't suggest getting doing this except for when you are testing a small number of robots. The queue can fill up quickly and you will miss messages if you don't get them fast enough.

```python

def myLoggingTask(bot):
	import random
	while True:
		val = random.random()
		bot.log(val)
		time.sleep(1)

mySwarm.connect(hosts)
mySwarm.load_task(myLoggingTask)
mySwarm.go()

while True:
	if not mySwarm.queue.empty():
		print(str(mySwarm.queue.get())


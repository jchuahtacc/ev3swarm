# ev3swarm

## Code in Python once, deploy to many robots, execute simultaneously

### Summary

`ev3swarm` is a Python swarm robotics framework for Lego Mindstorms EV3 units running [ev3dev](http://www.ev3dev.org/), using [RabbitMQ](http://www.rabbitmq.com/) as the message broker. 

### What is a Swarm

A robot swarm is a collection of many physically identical robots executing the same set of simplistic behaviors. Individually, they may not do much. As a large group, they exhibit emergent behavior. Think of them like ants. Ants aren't particularly intelligent on their own, but achieve much by simply leaving and following pheromones. Some simple rules for a robot swarm:

- Every individual is the same as every other individual, both physically and logically.
- There is no centralized control to achieve teamwork.
- The swarm is scalable, in that if you add more units it should accomplish more.

There are plenty of academic papers on robot swarms that you can Google.

### How it works

Each EV3 unit has to run a Python service called `ev3host`. `ev3host` will wait for connections from `ev3swarm.Swarm`, receive serialized Python code (broadcast over RabbitMQ) and then execute it when `Swarm.go()` is called.

### Is it difficult to use?

Hopefully not! If you can think of ways that this can be easier, please let me know. The intended audience is Middle and High School students. You may have to get your hands a little dirty with configuration, but these instructions should be pretty complete. If you know how to find your IP address, then you should be in good shape.

## Setup

First things first, download this repo.

### Setup RabbitMQ

1. Download and install [RabbitMQ](http://www.rabbitmq.com/). For my OSX install, I had to install XCode tools, install brew, then run a brew command to install it. Check for details on their website for your specific platform.
2. Make sure it's running.
2. Open up a browser and navigate to your RabbitMQ server's management page at [http://localhost:15672](http://localhost:15672)
3. At the bottom of the page, you should see a section called *Paths*, with one that says *Config File.* Don't worry if it's not found, just open up that folder.
4. Open the `rabbitmq-env.conf` file for editing.
5. Remove any line that says `NODE_IP_ADDRESS`
6. Add a new line that simply says `RABBITMQ_NODE_IP_ADDRESS=`
7. This should allow your RabbitMQ server to run on all of your interfaces. Restart RabbitMQ
8. If you have telnet, you should be able to telnet to your ip address on port 5672 and get some kind of response.

### Setup a RabbitMQ user account

1. Open up the management page in the browser and go to the **Admin** page.
2. Hit the **Add user** button at the bottom of the page. Create a new user called **robot** with password **maker** - these are the defaults that ev3swarm will connect with. (You can use your own username and password with a little more Python code.)
3. When you return to the **Admin** page, the **robot** user should be there with no access to anything. Click on the **robot** user's name in the table.
4. There's a **Set permission** button. The defaults are fine. Click on that.

### Setup ev3host on your EV3 CPU

This is a whole separate section. Go to the [ev3host](./ev3host) directory and check the README there.

### Setup ev3swarm

1. Run the setup script with `python setup.py`. 
2. You should now be able to use it with `from ev3swarm import Swarm`. 
3. Try the [examples](./examples).
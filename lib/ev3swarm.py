"""

ev3swarm.py
author: jchuah@tacc.utexas.edu

Manages connections to a swarm of ev3 robots through AMQP. Allows for remote code push and messaging.

"""

import pika
import marshal
from multiprocessing import Process, Queue
import warnings
import rpyc

class Swarm:
    # This message multiprocessing queue receives messages from the ev3host service
    queue = Queue()

    __channel = None
    __process = None
    __connection = None
    __connectionProcess = None
    __broker = None
    __credentials = None

    # Constructor accepts the hostname of an AMQP broker. The hostname will be passed on to each
    # connected ev3host, so don't use "localhost". Also, we assume that the AMQP username
    # and password will be robot:maker (the same as ev3dev)
    def __init__(self, broker, username='robot', password='maker'):
        self.__broker = broker
        self.__credentials = pika.PlainCredentials(username, password)
        self.__connection = self.__pikaConnect()
        print "finished connection"
        self.__channel = self.__connection.channel()
        # Make task exchange
        self.__channel.exchange_declare(exchange='tasks', type='fanout')

    # Connect to a list of hostnames belonging to ev3dev hosts
    def connect(self, hostnames):
        if not self.__connectionProcess is None:
            self.__connectionProcess.terminate()
        self.__connectionProcess = Process(target=self.__connect_handler, args=(hostnames,))
        self.__connectionProcess.start()

    # Serializes and broadcasts a method to the ev3host swarm
    def load_task(self, task):
        task_code = marshal.dumps(task.func_code)
        self.__channel.basic_publish(exchange='tasks', routing_key='', body=task_code)

    # Brodacasts a message to the ev3host swarm causing it to execute the broadcast task
    def go(self):
        self.__process = Process(target=self.__go_handler)
        self.__process.start()
        self.__send_control("run")

    def __pikaConnect(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.__broker, port=5672, virtual_host='/', credentials=self.__credentials))


    def __alive_callback(self, ch, method, properties, body):
        print "Ev3 Host connection on " + body

    def __connect_handler(self, hostnames):
        connection = self.__pikaConnect()
        channel = connection.channel()
        channel.queue_declare(queue='alive')
        channel.basic_consume(self.__alive_callback, queue='alive', no_ack=True)
        print "hostnames " + str(hostnames)
        for h in hostnames:
            print "Connecting to host " + h
            c = rpyc.connect(host=h, port=12345)
            c.root.start(h, self.__broker)
        channel.start_consuming()

    def __log_callback(self, ch, method, properties, body):
        try:
            self.queue.put(marshal.loads(body))
        except BaseException:
            warnings.warn("Could not store logged message in queue: " + str(body))

    def __send_control(self, message):
        print "Sending control message: " + message
        self.__channel.basic_publish(exchange='control', routing_key='', body=message)

    def __go_handler(self):
        print "Starting connection"
        # Each process needs its own pika Connection
        connection = self.__pikaConnect()
        channel = connection.channel()
        channel.queue_declare(queue='logs')
        channel.basic_consume(self.__log_callback, queue='logs', no_ack=True)
        channel.start_consuming()

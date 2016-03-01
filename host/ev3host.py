#!/usr/bin/python

import pika
import marshal
from multiprocessing import Process
from multiprocessing import Pool
import time
#import ev3dev.ev3 as ev3
import rpyc
import os
import signal

class Bot:
    def __init__(self, channel, host):
        self.__channel = channel
        self.__start_time = time.time()
        self.host = host

    def log(self, obj):
        message = dict()
        message["host"] = self.host
        message["time"] = time.time() - self.__start_time
        message["obj"] = obj
        self.__channel.basic_publish(exchange='', routing_key='logs',body=marshal.dumps(message))

def dummy(bot):
    print "dummy code"
    pass

class Rabbit:
    host = None
    broker = None
    def __init__(self, host, broker, username, password):
        self.host = host
        self.broker = broker
        self.username = username
        self.password = password
    def work(self):
        print "Starting rabbit connection to broker " + self.broker
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.broker,
                        credentials=pika.PlainCredentials(username=self.username, password=self.password)))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='logs')
        self.make_exchange('tasks', self.channel, self.task_callback)
        self.make_exchange('control', self.channel, self.control_callback)
        self.channel.queue_declare(queue='alive')
        self.channel.basic_publish(exchange='', routing_key='alive', body=self.host)
        self.channel.start_consuming()
        print "Should not reach here!"
    def task_callback(self, ch, method, properties, body):
        print "Task received"
        dummy.func_code = marshal.loads(body)
    def control_callback(self, ch, method, properties, body):
        print "Control message received: " + body
        if body == "run":
            print "Control message: Run"
            bot = Bot(self.channel, self.host)
            dummy(bot)
    def make_exchange(self, name, channel, callback):
        channel.exchange_declare(exchange=name, type ='fanout')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=name, queue=queue_name)
        channel.basic_consume(callback, queue=queue_name, no_ack=True)
    def close(self):
        self.connection.close()

class Ev3HostService(rpyc.Service):
    __rabbit = None
    __process = None

    def exposed_start(self, host, broker, username='robot', password='maker'):
        if not self.__rabbit is None:
            self.__rabbit.close()
        print "Rabbit start request on " + host + " for broker " + broker
        if not self.__process is None:
            self.__process.terminate()
        self.__rabbit = Rabbit(host, broker, username, password)
        self.__process = Process(target=self.__rabbit.work)
        self.__process.start()

if __name__ == "__main__":
    from rpyc.utils.server import ForkingServer
    f = ForkingServer(Ev3HostService, port=12345)
    print "Starting rpyc Ev3HostService"
    f.start()
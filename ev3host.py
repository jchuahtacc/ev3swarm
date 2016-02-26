import pika
import marshal
from multiprocessing import Process
import time
#import ev3dev.ev3 as ev3
import rpyc

class Bot:
    def __init__(self, channel, host):
        self.__channel = channel
        self.__start_time = time.time()
 #       self.ev3 = ev3

    def log(self, obj):
        print "logging object: " + str(obj)
        self.__channel.basic_publish(exchange='', routing_key='logs',body=marshal.dumps(obj))



def dummy(bot):
    print "dummy code"
    pass


class Rabbit:
    host = None
    broker = None
    def __init__(self, host, broker):
        self.host = host
        self.broker = broker
    def work(self):
        print "Starting rabbit connection to broker " + self.broker
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.broker))
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
            self.__process = Process(target=dummy, args=(bot,))
            self.__process.start()
    def make_exchange(self, name, channel, callback):
        channel.exchange_declare(exchange=name, type ='fanout')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=name, queue=queue_name)
        channel.basic_consume(callback, queue=queue_name, no_ack=True)



class Ev3HostService(rpyc.Service):
    __channel = None
    __rabbits = list()
    __processes = list()
    __host = None

    def exposed_start(self, host, broker):
        print "Rabbit start request on " + host + " for broker " + broker
        self.__host = host
        r = Rabbit(host, broker)
        self.__rabbits.append(r)
        p = Process(target=r.work)
        self.__processes.append(p)
        p.start()

if __name__ == "__main__":
    from rpyc.utils.server import ForkingServer
    f = ForkingServer(Ev3HostService, port=12345)
    print "Starting rpyc Ev3HostService"
    f.start()
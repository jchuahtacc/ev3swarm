import pika
import marshal
from multiprocessing import Process, Queue
import warnings
import rpyc
from matplotlib import pyplot

class Swarm:
    __channel = None
    __process = None
    __connection = None
    queue = Queue()
    __connectionProcess = None
    __broker = None
    __credentials = None

    def __init__(self, broker, username='robot', password='maker'):
        self.__broker = broker
        self.__credentials = pika.PlainCredentials(username, password)
        self.__connection = self.__pikaConnect()
        print "finished connection"
        self.__channel = self.__connection.channel()
        # Make task exchange
        self.__channel.exchange_declare(exchange='tasks', type='fanout')

    def __pikaConnect(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.__broker, port=5672, virtual_host='/', credentials=self.__credentials))


    def __alive_callback(self, ch, method, properties, body):
        print "Ev3 Host connection on " + body

    def __connect_handler(self, hostnames):
        connection = self.__pikaConnect()
        channel = connection.channel()
        channel.queue_declare(queue='alive')
        channel.basic_consume(self.__alive_callback, queue='alive', no_ack=True)
        for h in hostnames:
            c = rpyc.connect(host=h, port=12345)
            c.root.start(h, self.__broker)
        channel.start_consuming()

    def connect(self, hostnames):
        if not self.__connectionProcess is None:
            self.__connectionProcess.terminate()
        self.__connectionProcess = Process(target=self.__connect_handler, args=(hostnames,))
        self.__connectionProcess.start()

    def __log_callback(self, ch, method, properties, body):
        try:
            self.queue.put(marshal.loads(body))
        except BaseException:
            warnings.warn("Could not store logged message in queue: " + str(body))

    def load_task(self, task):
        print "Broadcasting task"
        task_code = marshal.dumps(task.func_code)
        self.__channel.basic_publish(exchange='tasks', routing_key='', body=task_code)

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

    def go(self):
        self.__process = Process(target=self.__go_handler)
        self.__process.start()
        self.__send_control("run")
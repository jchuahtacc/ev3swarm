import pika
import marshal
from multiprocessing import Process, Queue
import warnings
import rpyc

__channel = None
__process = None
__connection = None
__logQueue = Queue()
__connectionProcess = None


def alive_callback(ch, method, properties, body):
    print "Ev3 Host connection on " + body

def connect_handler(hostnames, broker):
    connection = pika.BlockingConnection(pika.ConnectionParameters(broker))
    channel = connection.channel()
    channel.queue_declare(queue='alive')
    channel.basic_consume(alive_callback, queue='alive', no_ack=True)
    for host in hostnames:
        c = rpyc.connect(host='localhost', port=12345)
        c.root.start(host, broker)
    channel.start_consuming()

def connect(hostnames, broker):
    global __connectionProcess
    if not __connectionProcess is None:
        __connectionProcess.terminate()
    __connectionProcess = Process(target=connect_handler, args=(hostnames,broker))
    __connectionProcess.start()

def log_callback(ch, method, properties, body):
    try:
        __logQueue.put(marshal.loads(body))
    except BaseException:
        warnings.warn("Could not store logged message in queue: " + str(body))

def load_task(task):
    print "Broadcasting task"
    task_code = marshal.dumps(task.func_code)
    __channel.basic_publish(exchange='tasks', routing_key='', body=task_code)

def send_control(message):
    print "Sending control message: " + message
    __channel.basic_publish(exchange='control', routing_key='', body=message)

def go_handler():
    print "Starting connection"
    # Each process needs its own pika Connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logs')
    channel.basic_consume(log_callback, queue='logs', no_ack=True)
    channel.start_consuming()

def go():
    __process = Process(target=go_handler)
    __process.start()
    send_control("run")

def init():
    global __channel
    __connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    __channel = __connection.channel()
    # Make task exchange
    __channel.exchange_declare(exchange='tasks', type='fanout')

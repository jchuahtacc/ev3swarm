import rpyc
import multiprocessing
from rpyc.utils.server import ThreadedServer
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
import marshal

def dummy(x):
    pass

class Ev3Service(rpyc.Service):
    def on_connect(self):
        print "rpyc connection established"
    def on_disconnect(self):
        print "rpyc connection terminated"
    def exposed_echo(self):
        print "ev3 swarm echo"
    def exposed_run(self, task_code, args):
        print task_code
        dummy.func_code = marshal.loads(task_code)
        pool = multiprocessing.Pool(processes = 8)
        result = pool.map(dummy, args)
        pool.close()
        return result

if __name__ == "__main__":
    server = ThreadedServer(Ev3Service, hostname='10.0.0.1', port = 12345, protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)
    server.start()

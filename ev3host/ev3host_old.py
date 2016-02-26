import rpyc
import multiprocessing
from rpyc.utils.server import ThreadedServer
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
import marshal

def dummy(bot):
    "DUMMY CODE"
    pass

class Ev3Bot:
    def __init__(self, host, service):
        self.host = host
        self.service = service
    def message(self, value):
        self.service.put(value)

class Ev3Service(rpyc.Service):
    def on_connect(self):
        print "rpyc connection established"
    def on_disconnect(self):
        print "rpyc connection terminated"
    def exposed_echo(self):
        print "ev3 swarm echo"
    def exposed_run(self, host, task_code):
        dummy.func_code = marshal.loads(task_code)
        bot = Ev3Bot(host,self._conn.root)
        process = multiprocessing.Process(target=dummy, args=(bot,))
        print "starting process"
        process.start()
#        process.join()
        print "joining process"

if __name__ == "__main__":
    server = ThreadedServer(Ev3Service, hostname='10.0.0.1', port = 12345, protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)
    server.start()

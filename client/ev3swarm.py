import rpyc
import marshal
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True


def mytask(x):
    print "hello from the outside " + str(x)

c = rpyc.connect('10.0.0.1', port=12345, config = rpyc.core.protocol.DEFAULT_CONFIG)
func = marshal.dumps(mytask.func_code)
c.root.run(func, [1,2,3,4,5])

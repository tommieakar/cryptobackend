import zmq

port = '40032'

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://52.193.146.32:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, '')

while True:
	string = socket.recv()
	print 'client receive' + '\t' + string

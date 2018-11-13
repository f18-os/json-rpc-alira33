import socket
from bsonrpc import JSONRpc
from bsonrpc import request, service_class
from node import *

# Class providing functions for the client to use:
@service_class
class ServerServices(object):

  @request
  def swapper(self, txt):
    return txt

  @request
  def increment(self, graph):
    graph['val'] += 1
    for c in graph['children']:
        increment(c)
    return graph

# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 6000))
ss.listen(10)

while True:
  s, _ = ss.accept()
  # JSONRpc object spawns internal thread to serve the connection.
  JSONRpc(s, ServerServices())
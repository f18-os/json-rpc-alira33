import socket
from bsonrpc import JSONRpc
import json
import pickle
from collections import namedtuple

class node:
    def __init__(self, name, children = []):
        self.name = name
        self.children = children
        self.val = 0
    def show(self, level=0):
        print("%s%s val=%d:" % (level*"  ", self.name, self.val))
        for c in self.children: 
            c.show(level + 1)

def serialize_json(instance=None, path=None):
    dt = {}
    dt.update(vars(instance))

    with open(path, "w") as file:
        json.dump(dt, file)

# Cut-the-corners TCP Client:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 6000))

rpc = JSONRpc(s)
server = rpc.get_peer_proxy()

leaf1 = node("leaf1")
leaf2 = node("leaf2")

root = node("root", [leaf1, leaf1, leaf2])

print("graph before increment")
root.show()

# open a file, where you ant to store the data
file = open('request.json', 'wb')

encode_root = json.dumps(root)
#encode_root = json.dumps(root, default=lambda o: o.__dict__)

print("input graph dumped to request.json")
# dump information to that file
with open('request.json', 'w') as outfile:
    json.dump(encode_root, outfile)

res = json.loads(encode_root)

d = json.dumps(res)
json_acceptable_string = d.replace("'", "\"")
datastore = json.loads(json_acceptable_string)
response = server.increment(res)

print("graph after increment")

# d = json.dumps(response)
# json_acceptable_string = d.replace("'", "\"")
# datastore = json.loads(json_acceptable_string)

# py_obj = pyjsonrpc.parse_response_json(response)

# print(py_obj.result)

# final_root = json.loads(encoded_root)

# final_root.show()

# "!dlroW olleH"
# print(result)

# close the file
file.close()

# Closes the socket 's' also
rpc.close() 
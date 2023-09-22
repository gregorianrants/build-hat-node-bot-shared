import zmq
import json


class Publisher:
    def __init__(self, context, address, node, topic):
        self.context = context
        self.publicationAddress = None
        self.socket = None
        self.address = address
        self.node = node
        self.topic = topic
        self.register()

    def register(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://192.168.178.47:3000")
        socket.send_json(
            {
                "action": "register",
                "register_as": "publisher",
                "topic": self.topic,
                "node": self.node,
                "address": self.address,
            }
        )

        message = socket.recv_json()
        # print(message)
        self.publicationAddress = message["data"]["fullAddress"]
        self.socket = self.context.socket(zmq.PUB)
        print(f"subscribing to {self.publicationAddress}")
        self.socket.bind(self.publicationAddress)

    def send_json(self, py_dict):
        as_json = json.dumps(py_dict)
        self.socket.send_string(as_json)

    def send_bytes(self, data):
        message = [bytes(self.node, "UTF-8"), bytes(self.topic, "UTF-8"), data]
        # print(message)
        self.socket.send_multipart(message)


def registerPublisher(context, address, node, topic):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.178.47:3000")
    socket.send_json(
        {
            "action": "register",
            "register_as": "publisher",
            "topic": topic,
            "node": node,
            "address": address,
        }
    )

    message = socket.recv_json()
    # print(message)
    return message["data"]["fullAddress"]

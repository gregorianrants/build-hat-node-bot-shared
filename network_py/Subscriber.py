import zmq
import time


# TODO add a flag to change mode so that iterator can deal with different kinds of data
# currently recieveing bytes but we also will have subscribers that recieve json.
class Subscriber:
    def __init__(self, context, subscribe_to_topic, subscribe_to_node="any"):
        self.context = context
        self.socket = None
        self.publishserAddress = None
        self.subscribe_to_node = subscribe_to_node
        self.subscribe_to_topic = subscribe_to_topic
        self.register()
        self.connect()

    def register(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://192.168.178.47:3000")
        success = False

        while not success:
            socket.send_json(
                {
                    "action": "register",
                    "register_as": "subscriber",
                    "subscribe_to_node": self.subscribe_to_node,
                    "subscribe_to_topic": self.subscribe_to_topic,
                }
            )

            message = socket.recv_json()
            if message["result"] == "success":
                success = True
                print("connected")
                self.publishserAddress = message["data"]["fullAddress"]
                return message["data"]["fullAddress"]
            time.sleep(0.1)

    def connect(self):
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(self.publishserAddress)
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.socket.setsockopt(zmq.CONFLATE, 1)

    def __next__(self):
        received_bytes = self.socket.recv_multipart()
        return received_bytes

    def __iter__(self):
        return self


def register(context):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.178.47:3000")

    success = False

    while not success:
        socket.send_json(
            {
                "action": "register",
                "register_as": "subscriber",
                "subscribe_to_node": "camera",
                "subscribe_to_topic": "frame",
            }
        )

        message = socket.recv_json()
        if message["result"] == "success":
            success = True
            print("connected")
            return message["data"]["fullAddress"]
        time.sleep(0.1)
        # print('still in loop')

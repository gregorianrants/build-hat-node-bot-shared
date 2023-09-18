import zmq


def registerPublisher(context,address):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.178.47:3000")
    socket.send_json(
        {
            "action": "register",
            "register_as": "publisher",
            "topic": "frame",
            "node": "camera",
            "address": address,
        }
    )

    message = socket.recv_json()
    return message["data"]["fullAddress"]

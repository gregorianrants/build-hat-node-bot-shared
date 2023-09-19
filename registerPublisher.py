import zmq


def registerPublisher(context,address,node,topic):
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
    #print(message)
    return message["data"]["fullAddress"]



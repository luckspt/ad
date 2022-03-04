import socket as s


def create_tcp_server_socket(address, port, queue_size):
    pass


def create_tcp_client_socket(address, port):
    pass


def receive_all(socket: s.socket, length: int) -> bytearray | None:
    data = bytearray()
    try:
        for _ in range(length):
            packet = socket.recv(1)
            data.extend(packet)
        return data
    except:
        return None

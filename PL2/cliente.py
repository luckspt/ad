import pickle
import socket as s
import struct
import sys

# Para ficar no root da pasta, por causa do sock_utils
sys.path.insert(0, '..')

from sock_utils import receive_all

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 9999
while True:
    msg = str(input('Mensagem: '))
    if msg == 'EXIT':
        break

    # Estabelecer connexão
    conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    conn_sock.connect((HOST, PORT))

    msg_list = msg.split()

    # Serializar a mensagem
    msg_bytes = pickle.dumps(msg_list, -1)
    size_bytes = struct.pack('i', len(msg_bytes))

    # Enviar a mensagem
    conn_sock.sendall(size_bytes)
    conn_sock.sendall(msg_bytes)

    # Receber uma resposta
    size_bytes = receive_all(conn_sock, 4)
    size = struct.unpack('i', size_bytes)[0]

    # Desserializar a resposta
    msg_bytes = receive_all(conn_sock, size)
    msg = pickle.loads(msg_bytes)

    print('Recebi: %s' % msg)
    conn_sock.close()
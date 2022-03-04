import pickle
import socket as s
import struct
import sys

# Para ficar no root da pasta, por causa do sock_utils
sys.path.insert(0, '..')

from sock_utils import receive_all

HOST = ''
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 9999

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)

msg_list = []
while True:
    try:
        (conn_sock, addr) = sock.accept()

        # Opter mensagem
        size_bytes = receive_all(conn_sock, 4)
        size = struct.unpack('i', size_bytes)[0]

        # Desserializar mensagem
        msg_bytes = receive_all(conn_sock, size)
        msg = pickle.loads(msg_bytes)

        # Processar mensagem
        resp = ['Ack']

        if 'LIST' == msg[0]:
            resp = msg_list
        elif 'CLEAR' == msg[0]:
            msg_list.clear()
            resp = ['Lista apagada']
        elif 'REMOVE' == msg[0]:
            try:
                pos = msg[1]
                msg_list.pop(pos)
            except Exception as e:
                msg_list.append(e)
        else:
            print(msg)
            msg_list.append(' '.join(msg))

        # Serializar resposta
        resp_bytes = pickle.dumps(resp, -1)
        size_bytes = struct.pack('i', len(resp_bytes))

        # Enviar resposta
        conn_sock.sendall(size_bytes)
        conn_sock.sendall(resp_bytes)

        print('list= %s' % msg_list)
        conn_sock.close()
    except Exception as e:
        print('Vou encerrar!', e)
        break
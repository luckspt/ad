import sys, socket as s
#import sock_utils
HOST = ''
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 9999
#sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1):
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
list = []
while True:
    try:
        (conn_sock, addr) = sock.accept()
        msg = conn_sock.recv(1024)
        resp = 'Ack'

        if msg.decode() == 'LIST':
            resp = str(list)
        elif msg.decode() == 'CLEAR':
            list = []
            resp = 'Lista apagada'
        else:
            list.append(msg.decode('utf-8'))

        conn_sock.sendall(resp.encode('utf-8'))
        print('list= %s' % list)
        conn_sock.close()
    except:
        print('Vou encerrar!')
        break
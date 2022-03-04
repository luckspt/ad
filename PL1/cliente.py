import sys, socket as s
#import sock_utils
if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 9999
while True:
    msg = str(input('Mensagem: '));
    if msg == 'EXIT':
        break

    #conn_sock = sock_utils.create_tcp_client_socket(HOST, PORT)
    conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    conn_sock.connect((HOST, PORT))

    conn_sock.sendall(msg.encode('utf-8'))
    resposta = conn_sock.recv(1024)
    print('Recebi: %s' % resposta.decode())
    conn_sock.close()
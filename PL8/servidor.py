import ssl
import sys
import socket as s

HOST = 'localhost'
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 9999

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)

context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
# context.verify_mode = ssl.CERT_NONE # ex 3
context.verify_mode = ssl.CERT_REQUIRED # ex 5
context.load_verify_locations(cafile='root.pem') # ex 5
context.load_cert_chain(certfile='serv.crt', keyfile='serv.key')

list = []
while True:
    (conn_sock, addr) = sock.accept()
    sslsock = context.wrap_socket(conn_sock, server_side=True)

    try:
        tmp = sslsock.recv(1024)
        msg = tmp.decode()
        resp = 'Ack'

        if msg == 'LIST':
            resp = str(list)
        elif msg == 'CLEAR':
            list = []
            resp = "Lista apagada"
        else:
            list.append(msg)

        sslsock.sendall(resp.encode())

        print('list= %s' % list)
        sslsock.close()
    except:
        print('socket fechado!')
        sslsock.close()
sock.close()

import ssl
import sys
import socket as s

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = 'localhost'
    PORT = 9999

context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations(cafile='root.pem')
context.load_cert_chain(certfile='cli.crt', keyfile='cli.key') # ex 5

while True:
    msg = input('Mensagem: ')

    if msg == 'EXIT':
        break

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    sslsock = context.wrap_socket(sock, server_hostname=HOST)

    sslsock.sendall(msg.encode())
    resposta = sslsock.recv(1024)

    print(f'Recebi: {resposta.decode()}')

sslsock.close()

import http.client
import resource

while True:
    cmdinp = input('comando > ')

    cmd, *args = cmdinp.split();

    op = None
    req = None
    body = None
    headers = {}

    if cmd == 'EXIT':
        break
    elif cmd == 'LIST':
        op = 'GET'
        req = '/lista/list'
    elif cmd == 'CLEAR':
        op = 'POST'
        req = '/lista/clear'
    elif cmd == 'APPEND':
        op = 'POST'
        req = f'/lista/append/{args[0]}'
    elif cmd == 'UPDATE':
        op = 'PUT'
        req = f'/lista/update/{args[0]}'
        body = args[1]
        headers = {'Content-Length': len(body.encode())}
    elif cmd == 'REMOVE':
        op = 'DELETE'
        req = f'/lista/remove/{args[0]}'

    if op is not None and req is not None:
        con = http.client.HTTPConnection("localhost", 8080)
        con.request(op, req, body, headers)
        res = con.getresponse()

        print(f'{res.status}, {res.reason}\n{res.read().decode()}\n')
        con.close()

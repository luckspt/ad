import http.server
import socketserver
PORT = 8080
HOST = ""

lst = []

class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self, http_code=200):
        self.send_response(http_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global lst

        paths = [p for p in self.path.split('/') if p != '']
        if paths[0] == 'lista':
            if paths[1] == 'list':
                self._set_headers(200)
                self.wfile.write(f'{lst}'.encode())
            elif paths[1] == 'contains':
                self._set_headers(200)
                self.wfile.write(f'{paths[2] in lst}'.encode())
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

    def do_POST(self):
        global lst

        paths = [p for p in self.path.split('/') if p != '']

        if paths[0] == 'lista':
            if paths[1] == 'clear':
                lst.clear()
                self._set_headers(204)
            elif paths[1] == 'append':
                lst.append(paths[2])
                self._set_headers(201)
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

    def do_PUT(self):
        global lst

        paths = [p for p in self.path.split('/') if p != '']

        if paths[0] == 'lista':
            if paths[1] == 'update':
                content_length = int(self.headers['Content-Length'])

                if content_length == 0:
                    self._set_headers(400)
                elif paths[2] not in lst:
                    self._set_headers(404)
                else:
                    new_word = self.rfile.read(content_length).decode()

                    idx = lst.index(paths[2])
                    lst.pop(idx)
                    lst.insert(idx, new_word)

                    self._set_headers(204)
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

    def do_DELETE(self):
        global lst

        paths = [p for p in self.path.split('/') if p != '']

        if paths[0] == 'lista':
            if paths[1] == 'remove':
                if paths[2] not in lst:
                    self._set_headers(404)
                else:
                    lst.remove(paths[2])
                    self._set_headers(204)
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

def main():
    HTTP_server = socketserver.TCPServer((HOST, PORT), MyHTTPHandler, True)
    HTTP_server.allow_reuse_address = True

    try:
        HTTP_server.serve_forever()
    except KeyboardInterrupt:
        pass
    HTTP_server.server_close()

if __name__ == '__main__':
    main()
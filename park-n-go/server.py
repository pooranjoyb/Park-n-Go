import http.server
import socketserver
import webbrowser

# Class to generate a server instance and openHTML instance
class start_serv:
    def __init__(self, filename):
        self.filename = filename
    def start_server(self, stop_event):
        PORT = 4000
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            while not stop_event.is_set():
                httpd.handle_request()
                exit()
                
    
    def open_file(self):
        print()
        url = 'http://localhost:4000/' + self.filename
        browser = webbrowser.get('windows-default')
        browser.open(url)


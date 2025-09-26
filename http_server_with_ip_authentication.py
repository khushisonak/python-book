import http.server
import socketserver
import socket
import base64

PORT = 50850
USERNAME = "admin"      # Change to your desired username
PASSWORD = "password"   # Change to your desired password

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Test"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        key = f"{USERNAME}:{PASSWORD}".encode()
        encoded_key = base64.b64encode(key).decode()
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith("Basic "):
            self.do_AUTHHEAD()
            self.wfile.write(b'No auth header received')
        elif auth_header.split(" ")[1] != encoded_key:
            self.do_AUTHHEAD()
            self.wfile.write(b'Invalid credentials')
        else:
            super().do_GET()

    def do_HEAD(self):
        # Optionally protect HEAD requests as well
        self.do_GET()

    def do_POST(self):
        # Optionally protect POST requests if needed
        self.do_GET()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ip_address = get_local_ip()

with socketserver.TCPServer(('', PORT), AuthHandler) as httpd:
    print(f"Serving HTTP with authentication on {ip_address} port {PORT} (http://{ip_address}:{PORT}/) ...")
    httpd.serve_forever()
import http.server
import socketserver
import socket

PORT = 50850
Handler = http.server.SimpleHTTPRequestHandler

# Get the local IP address of the device
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable, just needs to be a valid IP
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ip_address = get_local_ip()

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f"Serving HTTP on {ip_address} port {PORT} (http://{ip_address}:{PORT}/) ...")
    httpd.serve_forever()
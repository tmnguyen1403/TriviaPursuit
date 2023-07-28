import http.server
import socketserver

# Define the request handler class
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, world! This is the response from the server.')

# Set the server address and port
server_address = ('', 8000)




# Create an instance of the HTTP server
httpd = socketserver.TCPServer(server_address, MyRequestHandler)

# Start the server
print('Server running at http://localhost:8000')
httpd.serve_forever()
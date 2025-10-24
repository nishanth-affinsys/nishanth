# app.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

HOST_NAME = '0.0.0.0'
SERVER_PORT = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Simple Python App</title></head>", "utf-8"))
        self.wfile.write(bytes(f"<body><h1>Hello from Python inside a Docker Container!</h1>", "utf-8"))
        self.wfile.write(bytes(f"<p>The current time is: {time.ctime()}</p></body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print(f"Server started http://{HOST_NAME}:{SERVER_PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

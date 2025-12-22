import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8000))
GREETING = os.environ.get("GREETING", "Hello from MinPaas")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(GREETING.encode())

HTTPServer(("", PORT), Handler).serve_forever()

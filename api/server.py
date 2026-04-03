import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in {"/", "/health"}:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        payload = json.dumps({"status": "ok", "service": "plagiarism-checker"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        return


def start_server(config):
    host = config.get("server.host", "127.0.0.1")
    port = int(config.get("server.port", 8080))
    server = HTTPServer((host, port), _HealthHandler)
    print(f"Server running at http://{host}:{port} (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

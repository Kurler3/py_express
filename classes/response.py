import json

class Response:

    def __init__(self, server, path, headers, method):
        self.server = server
        self.path = path
        self.method = method
        self.headers = headers
        self.body = None
        self.status_code = 200
        self.is_sent = False

    def send(self, body=None):

        if self.is_sent:
            raise Exception('Response was already sent to client.')
        
        if body is not None:
            self.body = body
        
        # Send the status code
        self.server.send_response(self.status_code)

        # Send the headers.
        for header_name, header_value in self.headers.items():
            self.server.send_header(header_name, header_value)

        self.server.send_header('Content-Type', 'application/json')
        self.server.end_headers()

        # Send the body
        self.server.wfile.write(
            json.dumps(self.body).encode() if isinstance(self.body, (dict, list)) else str(self.body).encode()
        )

        self.server.is_sent = True

    def status(self, status_code):
        self.status_code = status_code
        return self
    
    # JSON
    def json(self, body):

        if not body:
            raise ValueError('Invalid body')

        self.send(body)
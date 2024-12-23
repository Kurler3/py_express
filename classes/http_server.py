from http.server import BaseHTTPRequestHandler
from classes.response import Response
from classes.request import Request
import json
from urllib.parse import parse_qs
import re
import tempfile



class CustomHandler(BaseHTTPRequestHandler):

    """Custom HTTP handler for the MinimalFramework."""

    def __init__(self, framework, *args, **kwargs):
        """
        Initialize the handler with a reference to the framework.
        """
        self.framework = framework
        super().__init__(*args, **kwargs)

    # Override the GET handler.
    def do_GET(self):

        """Handle GET requests."""

        # Handle the request
        self._handle_request('GET')

    # Override the POST handler.
    def do_POST(self):

        """Handle POST requests."""

        # Handle the request
        self._handle_request('POST')

    # Override the PUT handler.
    def do_PUT(self):
        """Handle PUT requests."""

        # Handle the request
        self._handle_request('PUT')

    # Override the PATCH handler.
    def do_PATCH(self):
        """Handle PATCH requests."""

        # Handle the request
        self._handle_request('PATCH')

    # Override the DEL handler.
    def do_DEL(self):
        """Handle DEL requests."""

        # Handle the request
        self._handle_request('DEL')

    # Function that handles requests.
    def _handle_request(self, method):

        body = None

        # Parse body (if method is not GET)
        if method != 'GET':
            body = self._parse_body()

        # Create the request instance.
        request = Request(
            path=self.path,
            method=method,
            headers=self.headers,
            body=body,
        )

        # Create response instance
        response = Response(
            server=self,
            path=self.path,
            method=method,
            headers=self.headers,
        )

        try:



            # Need to use regex to find a match in the routes.
            route = self._find_route_match(
                path=request.path_without_query, method=request.method)

            # If found the route
            if route:

                # Parse the params, now that the route is found.
                request.parse_params(route)

                handlers = self.framework.global_middlewares + \
                    self.framework.routes[route][method]

                # Function to process the middleware chain
                def next_handler(index=0):
                    if index < len(handlers):
                        current_handler = handlers[index]

                        # Call the handler and provide `next_handler` to control flow

                        # If on the last, aka the handler, don't pass the next argument.
                        if index == len(handlers) - 1:
                            current_handler(request, response)
                        else:
                            current_handler(request, response,
                                            lambda: next_handler(index + 1))

                # Start the middleware chain
                next_handler()

                return

            if not route:
                response.status(404).send({"error": "Not Found"})

        except Exception as e:

            if self.framework.debug_mode:
                print(f"Error: {e}")

            if response:

                # If there is an error middleware, send the error there.
                if self.framework.error_midleware:

                    self.framework.error_midleware(request, response, None, e)

                    return

                response.status(500).json({"error": "Something went wrong"})

    def _find_route_match(self, path, method):
        for route in self.framework.routes.keys():
            # Check match and if method is in the routes dict.
            if self._check_route_match(route, path) and method in self.framework.routes[route]:
                return route
        return None

    def _check_route_match(self, route, path):

        # Split both the route and the path by /
        route_split = route.split('/')
        path_split = path.split('/')

        if len(route_split) != len(path_split):
            return False

        for i in range(len(route_split)):

            if route_split[i].startswith(':') and path_split[i] != '':
                continue

            if route_split[i] != path_split[i]:
                return False

        return True

    # Parse body
    def _parse_body(self):

        # Read the content length to determine how many bytes to read from the input stream
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(
            content_length) if content_length > 0 else None

        if not raw_body:
            return None

        # Retrieve the Content-Type header
        content_type = self.headers.get(
            'Content-Type', '').split(';')[0]  # Split to ignore charset

        # Handle different content types
        try:

            if content_type == "application/json":
                # Parse JSON body
                return json.loads(raw_body.decode('utf-8'))

            elif content_type == "application/x-www-form-urlencoded":

                # Parse form-encoded body
                return parse_qs(raw_body.decode('utf-8'))

            elif content_type == "text/plain":
                # Decode plain text
                return raw_body.decode('utf-8')

            elif content_type.startswith("multipart/"):
                return self._parse_multipart()
            else:
                # Return raw body for unsupported types
                return raw_body.decode('utf-8')

        except Exception as e:

            # Log parsing errors and re-raise if necessary
            if self.framework.debug_mode:
                print(f"Error parsing body: {e}")
            raise ValueError("Unable to parse body")

    # Parse multipart
    def _parse_multipart(self):
        """Parse a multipart/form-data body."""

        content_type = self.headers.get('Content-Type')
        if not content_type or 'multipart/form-data' not in content_type:
            return None  # Return None if not multipart

        # Extract the boundary from the Content-Type header
        boundary = re.search(
            r'boundary=(.*)', content_type).group(1).encode('utf-8')
        if not boundary:
            raise ValueError("Boundary not found in Content-Type header")

        # Read the raw body
        raw_body = self.rfile.read(int(self.headers.get('Content-Length', 0)))

        if not raw_body:
            return None

        # Split the body into parts based on the boundary!
        parts = raw_body.split(b'--' + boundary)

        # Init the parsed data (dict)
        parsed_data = {}

        # For each part
        for part in parts:

            # If empty part or beginning of body or end of body => continue
            if not part or part == b'--' or part == b'--\r\n':
                continue

            # Get the headers and the content.
            headers, content = part.split(b'\r\n\r\n', 1)

            # Decode the headers and split.
            headers = headers.decode('utf-8').split('\r\n')

            # Parse Content-Disposition header to get field name and filename
            disposition = [h for h in headers if h.lower().startswith('content-disposition')][0]

            # Try to find a match for the specified disposition
            match = re.search(r'form-data; name="(.*?)"(; filename="(.*?)")?', disposition)
            
            if not match:
                continue
            
            field_name = match.group(1)
            
            filename = match.group(3)
            
            # Handle files
            if filename:

                # Save file content to a temporary file (will be deleted after the request is over)
                temp_file = tempfile.NamedTemporaryFile(delete=True)
                temp_file.write(content.strip())
                temp_file.seek(0)  # Reset the file pointer to read later if needed

                parsed_data[field_name] = {
                    "filename": filename,
                    "filepath": temp_file.name,
                    "content": None, # Could add an option to read this directly and store in memory instead of storing the file temporarily.
                }

            # Just a text field.
            else:

                # Treat as a regular field
                parsed_data[field_name] = content.decode('utf-8').strip()

        return parsed_data
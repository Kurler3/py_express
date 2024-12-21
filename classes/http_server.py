from http.server import BaseHTTPRequestHandler
from classes.response import Response
from classes.request import Request


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

        # Create the request instance.
        request = Request(
            path=self.path,
            method='GET',
            headers=self.headers,
            body=None,
        )

        # Create response instance
        response = Response(
            server=self,
            path=self.path,
            method="GET",
            headers=self.headers,
        )

        # Handle the request
        self._handle_request(request, response, 'GET')

    # TODO Override the POST handler.
    def do_POST(self):
        """Handle POST requests."""

        print(repr(self))

        # Create the request instance.
        request = Request(
            path=self.path,
            method='POST',
            headers=self.headers,
            body=self.body,
        )

        # Create response instance
        response = Response(
            server=self,
            path=self.path,
            method="POST",
            headers=self.headers,
        )

        # Handle the request
        self._handle_request(request, response, 'POST')

    # TODO Override the PUT handler.

    # TODO Override the PATCH handler.

    # TODO Override the DEL handler.

    # Function that handles requests.
    def _handle_request(self, request, response, method):

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

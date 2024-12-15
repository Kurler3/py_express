from http.server import BaseHTTPRequestHandler
from classes.response import Response
from classes.request import Request
import re

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

        request = Request(
            path=self.path,
            method='GET',
            headers=self.headers,
            body=None,
        )

        response = Response(
            server=self,
            path=self.path,
            method="GET",
            headers=self.headers,
        )

        try: 
            # Need to use regex to find a match in the routes.
            route = self._find_route_match(path=request.path_without_query, method=request.method)

            # If found the route
            if route:

                handlers = self.framework.global_middlewares + self.framework.routes[route]["GET"]

                # Function to process the middleware chain
                def next_handler(index=0):
                    if index < len(handlers):
                        current_handler = handlers[index]

                        # Call the handler and provide `next_handler` to control flow

                        # If on the last, aka the handler, don't pass the next argument.
                        if index == len(handlers) - 1:
                            current_handler(request, response)
                        else:
                            current_handler(request, response, lambda: next_handler(index + 1))

                # Start the middleware chain
                next_handler()

                return

            if not route:
                response.status(404).send({"error": "Not Found"})
        except Exception as e:
            print(f"Error: {e}")
            if response:
                response.status(500).json({ "error": "Something went wrong" })
        

    #TODO Override the POST handler.

    #TODO Override the PUT handler.

    #TODO Override the PATCH handler.

    #TODO Override the DEL handler.


    def _find_route_match(self, path, method):
        for route in self.framework.routes.keys():
            route_regex = self._build_route_regex(route)
            is_route_match = route_regex.match(path)
            if is_route_match and method in self.framework.routes[route]:
                return route
        return None

    
    def _build_route_regex(self, route):
        
        """Converts a route pattern with dynamic params into a regex."""
        
        # Match dynamic params like :id and replace them with a capturing group in regex
        route = route.replace("/", r"\/")  # Escape slashes

        # Use regex to find all :param-style placeholders in the route
        # and replace them with corresponding regex patterns

        #TODO Need to figure this out
        route = re.sub(r":(\w+)", r"(?P<\1>[\w-]+)", route)  # Match dynamic params
    
        # Return the compiled regex pattern
        return re.compile(f"^{route}$")
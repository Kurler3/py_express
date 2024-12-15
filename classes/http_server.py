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

        route_found = False

        if self.path in self.framework.routes and "GET" in self.framework.routes[self.path]:

            route_found = True

            handlers = self.framework.global_middlewares + self.framework.routes[self.path]["GET"]

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

        if not route_found:
            response.status(400).send("Not Found")

    #TODO Override the POST handler.

    #TODO Override the PUT handler.

    #TODO Override the PATCH handler.

    #TODO Override the DEL handler.

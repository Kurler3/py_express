import inspect

# Core Concepts:

# HTTP routing (with support for dynamic paths).
# Handling HTTP methods and paths.
# Middlewares for pre- and post-processing.
# Error handling and returning meaningful status codes and responses.

# Main components you’ll need:

# An HTTP request handling system (request and response abstractions).
# A routing system that maps URLs (with HTTP methods) to functions.
# Middleware support (global and route-specific).
# Static file support.
# Server loop to listen on a port and handle requests.

class PyExpress:
    
    def __init__(self):
        self.global_middlewares = []
        
        # Map from (resource) to method to functions (middleware, then controller)
        self.routes = {}
    
    #TODO Listen
    def listen(self, port=3000):
        
        # Start the server on the specified port.

        # Listen for any http requests and map them through the global middleware and then the specific middleware for the route chosen. Finally, map it to the controller.

            #TODO - Create request and response objects.
            #TODO - Should be able to respond to the client with the response object.

        pass

    # Use
    def use(self, middleware):

        """
            Pushes a global middleware in order, to run before every specific middleware.
            Each middleware should have 3 arguments. req, res, next. If this is not matched, there will be an error.
        """

        if not self._is_valid_middleware(middleware):
            raise ValueError("Invalid middleware provided. Middleware should have args: req, res, next")
        self.global_middlewares.push(middleware)

    #TODO Get
    def get(self, resource, middlewares, controller):

        """
            Creates a new GET route for a specific resource, with specific middlewares that run in order, and a controller.
        """


    #TODO Put

    #TODO Post

    #TODO Delete

    #TODO Patch

    def _add_route(self, resource, method, middlewares, controller):

        if not middlewares:
            raise ValueError(f'Missing controller for resource: {resource}')

        # If the middlewares is callable, that means its just one function. Which means it could be the controller, or there's only one middleware.
        if callable(middlewares):
            # If there's no controller, then the controll is actually just the middlewares.
            if not controller:
                controller = middlewares
                middlewares = []
            # There's a controller, so the middlewares is just ONE middleware.
            else:
                middlewares = [middlewares]

        if resource not in self.routes:
            self.routes[resource] = {}
        
        if method not in self.routes[resource]:
            self.routes[resource][method] = []

        

        pass

    def _is_valid_middleware(self, middleware):
        """
        Check if the middleware function has three arguments: req, res, and next.
        """
        
        signature = inspect.signature(middleware)
        
        # Check if there are exactly 3 parameters (req, res, next)
        parameters = signature.parameters
        if len(parameters) != 3:
            return False
        
        # For instance, ensure the names match 'req', 'res', 'next'
        param_names = list(parameters.keys())
        if param_names != ['req', 'res', 'next']:
            return False
        
        return True
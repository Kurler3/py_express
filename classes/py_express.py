import inspect
from typing import Callable, Optional, List
from http.server import HTTPServer
import threading
from classes.http_server import CustomHandler 


class PyExpress:
    
    def __init__(self, debug_mode=False):
        
        self.debug_mode = debug_mode
        
        self.global_middlewares = []
        
        # Error middleware.
        self.error_midleware = None

        # Map from (resource) to method to functions (middleware, then controller)
        self.routes = {}
    
    # Listen
    def listen(self, host="localhost", port=3000):
        
        # Start the server on the specified port.
        # Function to create the server on the desired host and port
        server_address = (host, port)

        # Init the custom handler.
        httpd = HTTPServer(server_address, lambda *args, **kwargs: CustomHandler(self, *args, **kwargs))

        print(f"Server running on {host}:{port}")
        
        if self.debug_mode:
            print(f"Global middlewares length: {len(self.global_middlewares)}")
            print(f"Routes: {list(self.routes.keys())}")

        # Start the HTTP server in a separate thread to avoid blocking
        threading.Thread(target=httpd.serve_forever, daemon=True).start()

        try:
            while True:  # Run the server indefinitely
                pass
        except KeyboardInterrupt:
            print("Server stopped.")
            httpd.shutdown()

    # Use
    def use(self, middleware):

        """
            Pushes a global middleware in order, to run before every specific middleware.
            Each middleware should have 3 arguments. req, res, next. If this is not matched, there will be an error.
        """

        if not self._is_valid_middleware(middleware):
            raise ValueError("Invalid middleware provided. Middleware should have args: req, res, next")
        
        
        # If the middleware takes 4 args, use it as an error middleware.
        if len(inspect.signature(middleware).parameters) == 4:

            if self.error_midleware:
                raise ValueError("Error middleware already defined.")

            self.error_midleware = middleware

            if self.debug_mode:
                print(f'Added error middleware to server.')
            
        # Otherwise, use it as a normal global middleware.
        else:
            self.global_middlewares.append(middleware)
            if self.debug_mode:
                print(f'Added global middleware to server. Current global middlewares length: {len(self.global_middlewares)}')

    # Get
    def get(self, resource: str, middlewares: Callable | List[Callable], controller: Optional[Callable]=None) -> None:

        """
            Creates a new GET route for a specific resource, with specific middlewares that run in order, and a controller.
        """

        self._add_route(resource, 'GET', middlewares, controller)

    # Put
    def put(self, resource: str, middlewares: Callable | List[Callable], controller: Optional[Callable]=None) -> None:

        """
            Creates a new PUT route for a specific resource, with specific middlewares that run in order, and a controller.
        """

        self._add_route(resource, 'PUT', middlewares, controller)

    # Post
    def post(self, resource: str, middlewares: Callable | List[Callable], controller: Optional[Callable]=None) -> None:

        """
            Creates a new POST route for a specific resource, with specific middlewares that run in order, and a controller.
        """

        self._add_route(resource, 'POST', middlewares, controller)


    # Delete
    def delete(self, resource: str, middlewares: Callable | List[Callable], controller: Optional[Callable]=None) -> None:

        """
            Creates a new DEL route for a specific resource, with specific middlewares that run in order, and a controller.
        """

        self._add_route(resource, 'DEL', middlewares, controller)


    # Patch
    def patch(self, resource: str, middlewares: Callable | List[Callable], controller: Optional[Callable]=None) -> None:

        """
            Creates a new PATCH route for a specific resource, with specific middlewares that run in order, and a controller.
        """

        self._add_route(resource, 'PATCH', middlewares, controller)


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

        # Check each middleware.
        for middleware in middlewares:
            if not self._is_valid_middleware(middleware):
                raise ValueError('Invalid middleware. Middleware must accept args: req, res, next')

        # Check the controller.
        if not self._is_valid_controller(controller):
            raise ValueError('Invalid controller. Controller must accept args: req, res')

        if resource not in self.routes:
            self.routes[resource] = {}
        
        if method not in self.routes[resource]:
            self.routes[resource][method] = []

        self.routes[resource][method] = middlewares + [controller]

        if self.debug_mode:
            print(f'Added new route. Current routes: {list(self.routes.keys())}')

        pass

    def _is_valid_middleware(self, middleware: Callable) -> bool:
        """
        Check if the middleware function has three arguments: req, res, and next.
        """

        return self._is_valid_function(
            function=middleware, 
            required_num_args=3,
            max_num_args=4, # In case of being an error middleware.
            required_arg_names=['req', 'res', 'next'],
            exact=False
        )
    
    def _is_valid_controller(self, controller: Callable) -> bool:

        """
        Check if the middleware function has three arguments: req, res, and next.
        """

        return self._is_valid_function(
            function=controller,
            required_arg_names=['req', 'res'],
            required_num_args=2,
            exact=True
        )
        
    def _is_valid_function(
            self, 
            function: Callable, 
            required_num_args: int,
            max_num_args: int=None,
            required_arg_names: Optional[List[str]]=None,
            exact:bool=True
    ) -> bool:

        if not function:
            return False

        signature = inspect.signature(function)

        parameters = signature.parameters

        if exact and len(parameters) != required_num_args:
            return False
        
        if not exact and len(parameters) < required_num_args:
            return False
        
        if max_num_args and len(parameters) > max_num_args:
            return False

        if required_arg_names:

            param_names = list(parameters.keys())

            if exact and param_names != required_arg_names:
                return False

            if not exact:
                for required_arg in required_arg_names:
                    if required_arg not in param_names:
                        return False 
                
                    

        return True
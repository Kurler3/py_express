from urllib.parse import urlparse, parse_qs
from time import time

class Request:

    def __init__(
        self,
        path,
        method,
        headers,
        body=None,
        params=None
    ):
        self.path = path
        self.method = method
        self.headers = headers,
        self.body = body
        self.query = self._parse_query_params(path)
        self.params = params or {}
        self.path_without_query = urlparse(path).path
        self.timestamp = time()

    def _parse_query_params(self, path):
        """Parse the query string parameters and return them as a dictionary."""
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)
        return {key: value[0] for key, value in query_params.items()}

    def __repr__(self):
        return f"Request(path={self.path}, method={self.method}, query={self.query}, params={self.params}, body={self.body})"
    
    # Parse the params.
    def parse_params(self, route):

        # Split both the route and the path by /
        route_split = route.split('/')
        
        path_split = self.path_without_query.split('/')

        params = {}

        for i in range(len(route_split)):
            if route_split[i].startswith(':') and path_split[i] != '':
                params[route_split[i][1:]] = path_split[i]

        self.params = params




class Request:

    def __init__(
        self,
        path,
        method,
        headers,
        body,
    ):
        self.path = path
        self.method = method
        self.headers = headers,
        self.body = body
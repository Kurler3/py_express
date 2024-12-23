
# Python Express-Like Framework

This project is a Python framework inspired by the simplicity and power of Express.js. It provides a lightweight HTTP server for handling incoming requests, routing, middleware, and response management, making it an excellent choice for building REST APIs or web applications in Python.

## Features

- Express-like API: Simple and intuitive design modeled after Express.js.

- Routing: Define routes for GET, POST, PUT, PATCH, and DELETE methods.

- Middleware Support: Add global and route-specific middleware for extensibility.

- Request and Response Management: Simplified handling of request data and response content.

- File Uploads: Supports parsing multipart/form-data with file upload capability.

- Error Handling: Centralized error handling middleware for robust applications.

- Debug Mode: Optionally enable debug mode for enhanced error logs.

## Instalation

Clone the repo and run it. No extra libraries required.

`git clone https://github.com/Kurler3/py_express`

`python3 -m main`

## Key Components

### Request Object

The Request class wraps information about the incoming HTTP request:

- path: The requested URL path.

- method: The HTTP method (e.g., GET, POST).

- headers: Dictionary of HTTP headers.

- body: Parsed body content (e.g., JSON, form, or plain text).

- files: Uploaded files parsed from multipart/form-data requests.

### Response Object

The Response class provides methods to send responses back to the client:

- status(code: int): Set the HTTP status code.

- send(data: dict | str): Send JSON or text data.

- json(data: dict): Send JSON responses explicitly.

### Middleware

Middleware functions execute sequentially before hitting the final route handler. Middleware can perform tasks like logging, authentication, and request validation:

`def log_middleware(req, res, next):
    print(f"Received request {repr(req)}")
    next()
`
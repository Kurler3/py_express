from classes.py_express import PyExpress
from classes.request import Request

def log_middleware(req, res, next):
    print(f"Received request {repr(req)}")

    next()

def hello_word(req: Request, res):

    res.status(200).json({
        "message": f"Echo from {req.path} {req.method}. Query params: {req.query}. "
    })

def error_catcher(req, res, next, err):
    print(f"Error: {err}")

    # Convert error to string to ensure it can be displayed
    error_message = str(err)
    
    res.status(400).json({
        "message": "CUSTOM ERROR: " + error_message,
        "error": error_message,
        "path": req.path,
        "timestamp": req.timestamp
    })

if __name__ == "__main__":
     
    server = PyExpress(debug_mode=True)

    server.use(log_middleware)

    server.use(error_catcher)

    server.get('/hello',  hello_word)
    server.get('/hello/:id', hello_word)
    server.get('/hello/:id/:name/aaaaaaaaaa/:no', hello_word)

    


    server.listen('localhost', 3000)





# Apply global middleware.

# Define routes.
    # Static routes
    # Dynamic routes with req params

# Define error middleware.

# Start listening for requests.
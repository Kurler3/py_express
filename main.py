from classes.py_express import PyExpress
from classes.request import Request

def log_middleware(req, res, next):
    print(f"Received request")
    next()

def hello_word(req: Request, res):

    res.status(201).json({
        "message": f"Echo from {req.path} {req.method}"
    })

if __name__ == "__main__":
     
    server = PyExpress(debug_mode=True)

    server.get('/hello', log_middleware,  hello_word)

    server.listen('localhost', 3000)





# Apply global middleware.

# Define routes.
    # Static routes
    # Dynamic routes with req params

# Define error middleware.

# Start listening for requests.
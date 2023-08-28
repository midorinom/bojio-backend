from __main__ import app

@app.route('/')
def index():
    return {
        "id": 101,
        "name": "lalalala",
        "test": False,
    }
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import auth, events

if __name__ == "__main__":
    app.run(port=8000, debug=True)
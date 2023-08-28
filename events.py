from __main__ import app

@app.route('/test2')
def test2():
    return {
        "id": 102,
        "name": "hello",
        "test": False,
    }
import json


def test_event_controller(client):
    response = client.get('/event/test')
    assert response.status_code == 200

def test_retrieve_all_events(client):
    response = client.get('/event/all-events')
    assert response.status_code == 200

def test_register(client):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"username": "wala3", "password": "162534", "email": "abcd@outlook.com"})
    response = client.post('/register', data=data, headers=headers)
    assert response.status_code == 200

def test_login(client):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"username": "wala3", "password": "162534"})
    response = client.post('/login', data=data, headers=headers)
    assert response.status_code == 200
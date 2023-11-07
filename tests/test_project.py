def test_event(client):
    response = client.get('/demo/test')
    assert response.status_code == 200
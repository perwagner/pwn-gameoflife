import json


def test_index_status_return_value_is_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login_status_return_value_is_200(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_signup_status_return_value_is_200(client):
    response = client.get('/signup')
    assert response.status_code == 200    
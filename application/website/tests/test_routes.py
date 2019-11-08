import json

from application.tests.factories import UserFactory


def login(client, username, password):
    return client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

def signup(client, username, email, password):
    return client.post(
        '/signup', 
        data=dict(username=username, email=email, password=password, password2=password),
        follow_redirects=True,
        )

def test_index_status_return_value_is_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login_status_return_value_is_200(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_signup_status_return_value_is_200(client):
    response = client.get('/signup')
    assert response.status_code == 200    

def test__login__success(client, db):
    user = UserFactory()
    user.set_password("abcde")

    r = login(client, user.username, "abcde")

    assert r.status_code, 200
    assert b"Logged in successfully." in r.data

def test__login__unsuccessful(client, db):
    user = UserFactory()
    user.set_password("abcde")

    r = login(client, user.username, "fffff")

    assert r.status_code, 200
    assert b"Invalid username or password" in r.data

def test__login__user_does_not_exist(client, db):
    r = login(client, "noname", "fffff")

    assert r.status_code, 200
    assert b"User does not exist, please create one" in r.data 

def test__signup__success(client, db):
    r = signup(client, 'tester', 'tester@test.com', 'abcde')

    assert r.status_code, 200
    assert b"Congratulations, you are now a registered user!" in r.data 

def test__signup__no_password__failure(client, db):
    r = signup(client, 'tester', 'tester@test.com', '')

    assert r.status_code, 200
    assert b"Congratulations, you are now a registered user!" not in r.data

def test__signup__user_with_username_already_exists__failure(client, db):
    UserFactory(username='tester')
    r = signup(client, 'tester', 'tester@test.com', '')

    assert r.status_code, 200
    assert b"Please use a different username." in r.data


def test__signup__user_with_email_already_exists__failure(client, db):
    UserFactory(email='tester@test.com')
    r = signup(client, 'tester', 'tester@test.com', '')

    assert r.status_code, 200
    assert b"Please use a different email address." in r.data
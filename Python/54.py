import pytest


def add(a, b):
    return a + b


@pytest.mark.parametrize("input, input1, expected_result", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -3, 7),
    (-1, -1, -2),
    (0, 0, 0),
])
def test_addition(input, input1, expected_result):
    result = add(input, input1)
    assert result == expected_result


@pytest.fixture
def additional_data():
    return {'config_param': 'value', 'other_param': 42}

def test_config_param(additional_data):
    assert additional_data['config_param'] == 'value'

def test_other_param(additional_data):
    assert additional_data['other_param'] == 42


@pytest.fixture
def users_data():
    users = {
        'user1': {'username': 'Jasur_bek', 'email': 'jasurbek@gmail.com', 'age': 15},
        'user2': {'username': 'Zokirov', 'email': 'zokirov@gmail.com', 'age': 16},
        'user3': {'username': 'Jasur', 'email': 'zokirovjasurbek@gmail.com', 'age': 22}
    }
    return users

def test_user_data(users_data):
    assert len(users_data) == 3
    assert 'user1' in users_data
    assert 'user2' in users_data
    assert 'user3' in users_data
    assert users_data['user1']['username'] == 'Jasur_bek'
    assert users_data['user2']['age'] == 16
    assert users_data['user3']['email'] == 'zokirovjasurbek@gmail.com'
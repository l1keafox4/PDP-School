import pytest
def add(x, y) -> None:
    return x + y


@pytest.mark.parametrize("input,expected", [(2, 4), (4, 8), (7, 14)])
def test_add(input, expected):
    result = add(input, input)
    assert result == expected

# @pytest.fixture
# def setup_data():
#     data = {"name": "John", "age": 24}
#     return data


# def test_empty(setup_data):
#     assert setup_data["name"] == "John"

import pytest
from guess import create_app  # Import your Flask app here


@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_create_game(client):
    """Test game creation endpoint."""
    response = client.post('/create', json={'password': 'testpassword'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'game_id' in data
    assert len(data['game_id']) == 8


def test_guess(client):
    """Test guessing endpoint."""
    create_response = client.post('/create', json={'password': 'test'})
    game_id = create_response.get_json()['game_id']

    guess_response = client.post(f'/guess/{game_id}', json={'guess': 'test'})
    assert guess_response.status_code == 200
    assert guess_response.get_json()['result'] == "Correct"

    wrong_guess_response = client.post(f'/guess/{game_id}', json={'guess': 'wrong'})
    assert wrong_guess_response.status_code == 200
    assert wrong_guess_response.get_json()['result'].startswith("Incorrect")

    wrong_game_id = client.post('/guess/xxxxxx', json={'guess': 'test'})
    assert wrong_game_id.status_code == 404

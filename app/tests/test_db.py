import pytest
import app.db as db

@pytest.fixture
def mock_db(mocker):
    mock_get_user_birthdate = mocker.patch("app.db.get_user_birthdate")
    mock_upsert_user = mocker.patch("app.db.upsert_user")
    return mock_get_user_birthdate, mock_upsert_user

def test_upsert_user(mock_db):
    # Arrange
    mock_get_user_birthdate, mock_upsert_user = mock_db

    # Mocking DB call
    mock_upsert_user.return_value = None  # Simulate DB action, return nothing

    # Act
    db.upsert_user("fernando", "2000-01-01")

    # Assert
    mock_upsert_user.assert_called_once_with("fernando", "2000-01-01")

def test_get_user_birthdate(mock_db):
    # Arrange
    mock_get_user_birthdate, _ = mock_db

    # Mocking DB call to return a sample date
    mock_get_user_birthdate.return_value = "2000-01-01"

    # Act
    result = db.get_user_birthdate("jose")

    # Assert
    assert result == "2000-01-01"
    mock_get_user_birthdate.assert_called_once_with("jose")

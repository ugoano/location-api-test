import pytest
from unittest import mock

from localistico import location
from localistico.location import (
    resolve_location, Location, SearchError,
    google_places_search, places_search_stub_url,
    google_places_detail, places_detail_stub_url,
    validate_response, APIError,
)


@pytest.yield_fixture
def mock_places_search():
    with mock.patch.object(location, "google_places_search") as _places_search:
        _places_search.return_value = {'results': [{'place_id': '123'}]}
        yield _places_search


@pytest.yield_fixture
def mock_places_detail():
    with mock.patch.object(location, "google_places_detail") as _places_detail:
        _places_detail.return_value = {'result': {
            'name': "Stark Industries",
            'id': "abc123",
            'international_phone_number': "+44 1234 567 890",
        }}
        yield _places_detail


@pytest.fixture
def mock_response():
    response = mock.Mock()
    response.status_code = 200
    response.json.return_value = {'status': "OK"}
    return response


@pytest.yield_fixture
def mock_requests(mock_response):
    with mock.patch.object(location, "requests") as _requests:
        _requests.get.return_value = mock_response
        yield _requests


def test_google_places_search(mock_requests):
    # Arrange
    query = "Localistico"
    location = None
    expected_url = places_search_stub_url.format(
        "query=Localistico&key=AIzaSyDEy58qwyPvic8sF5vlqOFFNZDgqmlS4Qw")

    # Act
    google_places_search(query, location)

    # Assert
    mock_requests.get.assert_called_once_with(expected_url)


def test_google_places_detail(mock_requests):
    # Arrange
    place_id = "abcd"
    expected_url = places_detail_stub_url.format(
        "placeid=abcd&key=AIzaSyDEy58qwyPvic8sF5vlqOFFNZDgqmlS4Qw")

    # Act
    google_places_detail(place_id)

    # Assert
    mock_requests.get.assert_called_once_with(expected_url)


def test_validate_response(mock_response):
    # Arrange
    expected_response = {'status': "OK"}

    # Act
    validated_response = validate_response(mock_response)

    # Assert
    assert validated_response == expected_response


def test_validate_response_error(mock_response):
    # Arrange
    mock_response.status_code = 404

    # Act Assert
    with pytest.raises(APIError):
        validate_response(mock_response)

def test_resolve_location_online():
    # Arrange
    name = "Localistico"

    # Act
    place = resolve_location(name=name)

    # Assert
    assert place == {
        'name': "Localistico",
        'place_id': "bc1ae69dbba7e2c983fd02d2f9a44b3ed33a76b1",
        'international_phone_number': "+44 20 3808 1169",
    }


def test_resolve_location(mock_places_search, mock_places_detail):
    # Arrange
    name = "Stark Industries"
    location = Location(latitude=51.376163, longitude=-0.098234)

    # Act
    place = resolve_location(name=name, location=location)

    # Assert
    assert place == {
        'name': "Stark Industries",
        'place_id': "abc123",
        'international_phone_number': "+44 1234 567 890",
    }


def test_resolve_location_error():
    # Arrange
    name = "Supercalafragelisticexplialidocious"
    location = Location(latitude=51.012312, longitude=0.082123)


    # Act Assert
    with pytest.raises(SearchError):
        assert resolve_location(name, location)

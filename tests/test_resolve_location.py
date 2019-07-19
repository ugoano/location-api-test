import pytest
from unittest import mock

from localistico import location
from localistico.location import resolve_location, Location, APIError


@pytest.yield_fixture
def mock_places_search():
    with mock.patch.object(location, "google_places_search") as _places_search:
        _places_search.return_value = {'results': [{'place_id': '123'}]}
        yield _places_search


@pytest.fixture
def mock_places_detail():
    with mock.patch.object(location, "google_places_detail") as _places_detail:
        _places_detail.return_value = {'results': [{
            'name': "Stark Industries",
            'id': "abc123",
            'international_phone_number': "+44 1234 567 890",
        }]}
        yield _places_detail


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
    with pytest.raises(APIError):
        assert resolve_location(name, location)

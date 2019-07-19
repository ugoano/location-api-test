import pytest

from location import resolve_location, Location, APIError


def test_resolve_location():
    # Arrange
    name = "Stark Industries"
    location = Location(51.376163, -0.098234)

    # Act
    place = resolve_location(name, location)

    # Assert
    assert place == {
        "name": "Stark Industries",
        "place_id": "abc123",
        "international_phone_number": "+44 1234 567 890",
    }

def test_resolve_location_error():
    # Arrange
    name = "Daily Bugle"
    location = Location(51.012312, 0.082123)

    # Act Assert
    with pytest.raises(APIError):
        assert resolve_location(name, location)


class APIError(Exception):
    pass


class Location:

    def __init__(self, *, latitude:float, longitude:float):
        self.latitude = latitude
        self.longitude = longitude


def resolve_location(name:str, location:Location):
    pass

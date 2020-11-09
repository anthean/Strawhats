# TODO: COMPLETE CHARACTER IMPLEMENTATION


# Base class for entities
class Character:
    def __init__(self, dimensions, location):
        self._width, self._height = (None, None)
        self._x, self._y = (None, None)
        self.set_dimensions(dimensions)
        self.set_location(location)
        self._health_points = None
        self._attack_points = None

    # Setters
    def set_dimensions(self, dimensions):
        self._width, self._height = dimensions

    def set_location(self, location):
        self._x, self._y = location

    def set_hp(self, hp):
        self._health_points = hp

    def set_ap(self, ap):
        self._attack_points = ap

    # Getters
    def dimensions(self) -> tuple:
        return self._width, self._height

    def location(self) -> tuple:
        return self._x, self._y

    def hp(self) -> int:
        return self._health_points

    def ap(self) -> int:
        return self._attack_points

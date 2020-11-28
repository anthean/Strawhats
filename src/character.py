# TODO: COMPLETE CHARACTER IMPLEMENTATION


# Base class for entities
class Character:
    def __init__(self):
        self.width, self.height = (None, None)
        self.x, self.y = (None, None)
        self.dimensions = (self.width, self.height)
        self.location = (self.x, self.y)
        self.health_points = None
        self.attack_points = None

    # Setters
    def set_dimensions(self, dimensions):
        self.width, self.height = dimensions

    def set_location(self, location):
        self.x, self.y = location

    def set_hp(self, hp):
        self.health_points = hp

    def set_ap(self, ap):
        self.attack_points = ap

    # Getters
    def dimensions(self) -> tuple:
        return self.width, self.height

    def location(self) -> tuple:
        return self.x, self.y

    def hp(self) -> int:
        return self.health_points

    def ap(self) -> int:
        return self.attack_points

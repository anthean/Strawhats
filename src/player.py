# TODO: COMPLETE PLAYER IMPLEMENTATION
from character import Character


# Player inherits from character class
class Player(Character):
    def __init__(self, dimensions, location):
        super().__init__(dimensions, location)
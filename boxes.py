import pygame, random, pokebase
import pokebase.interface
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
from boundaries import Segment, Door, Point
from typing import List, Tuple


class Box(Sprite):
    def __init__(self, rect: Rect, image: Surface):
        super().__init__()
        self.rect = rect
        self.points = Box.get_points(self.rect)
        self.image = pygame.transform.scale(image, self.rect.size)

    @staticmethod
    def get_points(rect: Rect):
        return [
            Point(rect.x, rect.y),
            Point((rect.x + rect.width), rect.y),
            Point((rect.x + rect.width), (rect.y + rect.height)),
            Point(rect.x, (rect.y + rect.height))
        ]


class Building(Box):
    def __init__(self, rect: Rect, image: Surface, door: Door):
        super().__init__(rect, image)
        self.door = door
        self.boundaries = Building.get_segments(self.points)

    @staticmethod
    def get_segments(points: List[Point]):
        boundaries = []
        prev = points[0]
        for point in points[1:]:
            boundaries.append(Segment(prev, point))
        return boundaries


class WildArea(Box):
    rand = 100
    def __init__(self, rect: Rect, image: Surface, levels: Tuple[int, int], types: list, pokebase: list):
        super().__init__(rect, image)
        self.levels = list(range(levels[0], levels[1]))
        self.types = types
        self.pokebase = pokebase

    def update(self, game: Game):
        num = random.randrange(0, WildArea.rand)
        if num == WildArea.rand / 2:
            type_adherent = True
            while type_adherent:
                type_adherent = True
                id = random.choice(self.pokebase).pokemon_species.id
                pokemon = pokebase.pokemon(id)
                for type in self.types:
                    if type not in pokemon.types:
                        type_adherent = False
                if type_adherent:
                    game.update(pokemon, random.choice(self.levels))

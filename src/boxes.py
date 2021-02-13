"""The module which holds all of the sprite classes, except
for the player sprite, like boxes, building, and wild area"""

import random
from typing import List, Tuple
import pygame
import pokebase
import pokebase.interface
from pygame import Rect, Surface
from pygame.sprite import Sprite
from src.boundaries import Segment


class Box(Sprite):
    """A sprite with a background image, contains all points, and has no boundaries"""

    def __init__(self, rect: Rect, image: Surface):
        super().__init__()
        self.rect = rect
        self.points = Box.get_points(self.rect)
        self.image = pygame.transform.scale(image, self.rect.size)

    @staticmethod
    def get_points(rect: Rect):
        """Static method that takes in a rect and
        returns all points (corners) in that rect"""
        return [
            (rect.x, rect.y),
            ((rect.x + rect.width), rect.y),
            ((rect.x + rect.width), (rect.y + rect.height)),
            (rect.x, (rect.y + rect.height))
        ]


class Building(Box):
    """A box but with boundaries and at least one door,
    so a player cannot walk inside it but can walk into another map"""

    def __init__(self, rect: Rect, image: Surface, doors: list):
        super().__init__(rect, image)
        self.boundaries = Building.get_segments(self.points)
        self.doors = doors

    @staticmethod
    def get_segments(points: List[Tuple[int, int]]):
        """Static method that takes in list of points and
        returns all segments connecting them"""
        boundaries = []
        prev = points[-1]
        for point in points:
            boundaries.append(Segment(prev, point))
            prev = point
        return [
            [boundaries[0], boundaries[2]],
            [boundaries[1], boundaries[3]]
        ]

    def update(self, game):
        player = game.player
        for i in range(2):
            old_pos = player.pos[i]
            new_pos = player.pos[i] + game.move[i]
            for j in range(2):
                mid = self.boundaries[i][j].get_mid()
                if mid - old_pos < 0 is not mid - new_pos < 0:
                    game.move[i] = 0


class WildArea(Box):
    """A box but whenever a player walks over it,
    it calculates whether/what pokemon will battle"""

    rand = 100
    def __init__(self, rect: Rect, image: Surface, levels: Tuple[int, int], types: list, all_pokemon: list):
        super().__init__(rect, image)
        self.levels = list(range(levels[0], levels[1]))
        self.types = types
        self.all_pokemon = all_pokemon

    def update(self, game):
        """
        1. Checks whether to have an encounter
        2. Sends back random pokemon if yes
        """
        num = random.randrange(0, WildArea.rand)
        if num == WildArea.rand / 2:
            type_adherent = True
            while type_adherent:
                type_adherent = True
                species_id = random.choice(self.all_pokemon).pokemon_species.id
                pokemon = self.all_pokemon.pokemon(species_id)
                for pokemon_type in self.types:
                    if pokemon_type not in pokemon.types:
                        type_adherent = False
                if type_adherent:
                    game.update(pokemon, random.choice(self.levels))

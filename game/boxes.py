"""The module which holds all of the sprite classes, except
for the player sprite, like boxes, building, and wild area"""

import random
from typing import List, Tuple
import pygame
import pokebase
import pokebase.interface
from pygame import Rect, Surface
from pygame.sprite import Sprite, collide_rect
from game.boundaries import Segment


class Box(Sprite):
    """A sprite with a background image, contains all points, and has no boundaries"""

    def __init__(self, rect: Rect, image: Surface, *args):
        super().__init__()
        self.rect = rect
        self.image = pygame.transform.scale(image, self.rect.size)


class Building(Box):
    """A box but with boundaries and at least one door,
    so a player cannot walk inside it but can walk into another map"""

    def __init__(self, rect: Rect, image: Surface, doors: list):
        super().__init__(rect, image)
        self.doors = doors

    def update(self, game):
        radius = game.player.radius
        player_pos = [game.player.get_pos()[i] + game.move[i] + radius[i]
                      for i in range(2)]
        pos = (self.rect.y, self.rect.x)
        bools = [player_pos[i] > pos[i] and player_pos[i] < pos[i] + self.rect.size[i] + radius[i]
                 for i in range(2)]
        if bools[0] and bools[1]:
            game.move = [0, 0]


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
        1. Checks whether to have an encounter based on random chance
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

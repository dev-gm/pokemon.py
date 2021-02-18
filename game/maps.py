"""The module which holds the player and map,
it attaches the rest of the sprites together"""

from typing import List
import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
from game.boxes import Box, Building
from game.boundaries import Door

class Player(Sprite):
    """The player class, holds player sprite, pos, and size"""

    def __init__(self, name: str, image: Surface, rect: Rect = Rect((0, 0), (50, 50))):
        self.name = name
        self.rect = rect
        self.image = pygame.transform.scale(image, self.rect.size)
        self.radius = self.rect.size
        super().__init__()

    def get_pos(self):
        """Returns position of the player"""
        return (self.rect.y, self.rect.x)

    def draw(self, screen: Surface):
        """Draws player to screen"""
        screen.blit(self.image, self.get_pos())

    def update(self, game):
        """Moves the player rect based on collision detection"""
        self.rect.move_ip(game.move[1], game.move[0])


class Map(Group):
    """The map class, holds all of the sprites in the map and its own background"""

    def __init__(self, image: Surface, rect: Rect, sprites: List[Sprite], doors: List[Door], caption: str):
        self.caption = caption
        self.rect = rect
        self.image = pygame.transform.scale(image, self.rect.size)
        super().__init__(sprites)
        self.doors = doors
        self.entrance = self.doors[0] if self.doors else (0, 0)
        self.points = []
        for sprite in sprites:
            if sprite is Building:
                self.doors.extend(sprite.doors)

    def draw(self, screen: Surface):
        """Draws background and sprites to screen"""
        screen.blit(self.image, self.rect)
        super().draw(screen)

    def update(self, game):
        """Updates sprites boundaries and map
        boundaries but passes in game as well"""
        radius = game.player.radius
        old_pos = game.player.get_pos()
        new_pos = [old_pos[i] + game.move[i] + radius[i] for i in range(2)]
        size = self.rect.size
        if (new_pos[0] < 0 or new_pos[0] > size[0]) or (new_pos[1] < 0 or new_pos[1] > size[1]): # Checks if new_pos is out of boundaries
            game.reset_next_turn = True
            for i in range(2):
                if game.move[i] < 0: # Checks if move is negative
                    game.move[i] -= (new_pos[i] - radius[i])
                elif game.move[i] > 0: # Checks if move is positive
                    game.move[i] -= (new_pos[i] - size[i])
        super().update(game)

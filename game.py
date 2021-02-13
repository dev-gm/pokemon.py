"""The module which holds the player, map, and game classes;
Main module which attaches the rest of the objects together"""

import json
import sys
import os
from typing import List
import pygame
from pygame.locals import *
from pygame import Rect, Surface, Color
from pygame.sprite import Sprite, Group
from boxes import Box, Building
from boundaries import Door

class Player(Sprite):
    """The player class, holds player sprite, pos, and size"""

    def __init__(self, name: str, image: Surface, rect: Rect = Rect((0, 0), (50, 50))):
        self.name = name
        self.rect = rect
        self.image = pygame.transform.scale(image, self.rect.size)
        self.radius = (self.rect.size[0], 0)
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

    def __init__(self, image: Surface, rect: Rect, sprites: List[Sprite], doors: List[Door]):
        self.rect = rect
        self.image = pygame.transform.scale(image, self.rect.size)
        super().__init__(sprites)
        self.doors = doors
        if self.doors:
            self.entrance = self.doors[0]
        else:
            self.entrance = (0, 0)
        self.points = []
        self.boundaries = Building.get_segments(Box.get_points(self.rect))
        for sprite in sprites:
            self.points.extend(sprite.points)
            if sprite is Building:
                self.doors.extend(sprite.doors)
                self.boundaries.extend(sprite.boundaries)

    def draw(self, screen: Surface):
        """Draws background and sprites to screen"""
        screen.blit(self.image, self.rect)
        super().draw(screen)

    def update(self, game):
        """Updates sprites boundaries and map
        boundaries but passes in game as well"""
        player = game.player
        radius = player.radius
        for i in range(2):
            new = player.get_pos()[i] + game.move[i]
            if new - radius[i] > self.rect.size[i] or new + radius[i] < 0:
                game.move[i] = 0
        super().update(game)


class Game:
    """Controls the entire game, holds all maps and player, and game loop"""

    def __init__(self, save: str = json.load(open("save.json", 'r+')).get("save")):
        """Initialized pygame and parses json file -
        pass in save name (saves/{save}/)"""
        pygame.init()
        self.map = None
        if not save:
            sys.exit()
        self.save = save
        self.path = os.path.join('./', "saves/", self.save)
        os.chdir(self.path)
        with open("data.json", 'r+') as file:
            self.parse(json.load(file))
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.move = [0, 0]
        self.movement = 50

    def start(self) -> int:
        """Game loop detects the button clicks, changes
        move var, and updates & draws all sprites on map"""
        while True:
            self.map.draw(self.screen)
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                i, movement = self.get_movement(event)
                if i is not None:
                    self.move[i] = movement
            self.update(self.map)
            self.update(self.player)
            pygame.display.update()
        return 0

    def get_movement(self, event):
        """Gets movement index (0 or 1) and movement val (50/-50),
        so if it returned (0, 50), then the game.move var would be
        turned into (x, 50). If None returns, then it stays the same"""
        i, movement = None, None
        possible_keys = (K_w, K_COMMA, K_a, K_d, K_e, K_s, K_o)
        if event.type in (KEYDOWN, KEYUP): # Check if event has key attribute
            movement = 0
            key = event.key
            if key in possible_keys: # Check if key is in possible keys
                if key in possible_keys[2:5]: # left or right
                    i = 0
                else: # top or bottom
                    i = 1
                if event.type == KEYDOWN:
                    if key in possible_keys[:3]: # forward or left (+)
                        movement = -self.movement
                    else: # backward or right (-)
                        movement = self.movement
        return i, movement

    def update(self, obj):
        """Updates and draws the map or player"""
        obj.update(self)
        obj.draw(self.screen)

    def change_map(self, new_map: Map):
        """Changes map another map"""
        self.map = new_map
        self.player.rect.pos = self.map.entrance

    def parse(self, data: dict):
        """Parses data from json, including
        size, caption, maps, and player"""
        self.size = data.get("size")
        self.caption = data.get("caption")
        self.maps = []
        print(os.listdir("./img"))
        for raw_map in data.get("maps"): # Gets maps from raw maps
            sprites = []
            for raw_sprite in raw_map.get("sprites"): # Gets sprites for map from raw sprites
                try:
                    globals().get(raw_sprite.get("type"))(
                        Rect(raw_sprite.get("pos"), raw_sprite.get("size")),
                        pygame.image.load(os.path.join('.', "img", raw_sprite.get("image"))),
                        [Door(
                            tuple(door.get("pos")[0]),
                            tuple(door.get("pos")[1]),
                            door.get("dest")
                        ) for door in raw_sprite.get("doors")]
                    )
                except TypeError:
                    print(f"{raw_sprite.get('type')} sprite type does not exist")
            self.maps.append(Map(
                pygame.image.load(os.path.join('.', "img", raw_map.get("image"))),
                Rect(raw_map.get("pos"), raw_map.get("size")),
                sprites,
                [Door(
                    tuple(door.get("pos")[0]),
                    tuple(door.get("pos")[1]),
                    door.get("dest")
                ) for door in raw_map.get("doors")]
            ))
        raw_player = data.get("player")
        self.map = self.maps[raw_player.get("current").get("map")]
        self.player = Player(
            raw_player.get("name"),
            pygame.image.load(os.path.join('.', "img", raw_player.get("image"))),
            Rect(raw_player.get("current").get("pos"), raw_player.get("size"))
        )
